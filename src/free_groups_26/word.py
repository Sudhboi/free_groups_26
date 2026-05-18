from __future__ import annotations
from collections.abc import Iterable
from typing import override
from .letter import Letter, Exponent, Symbol, letter_from_str
from .free_group import FreeGroup
from sortedcontainers import SortedSet


class MutableWord:
    word: list[Letter]

    def __init__(self, letters: list[Letter]) -> None:
        self.word = letters

    def immutable(self) -> Word:
        return Word(self.word)


class Word:
    """
    This class represents a word.
    """
    word: tuple[Letter, ...] #:
    length: int #: The mathematical length of the word. This is inferred from :py:attr:`word`.

    def __init__(self, word: Iterable[Letter]) -> None:
        self.word = tuple(word)
        self.length = 0
        for letter in word:
            self.length += abs(letter.exp)

    def reduced(self, cyclic: bool = False) -> Word:
        """
        Reduces the word. Uses a stack to perform reduction in :math:`O(n)`.

        :param cyclic: If the word is to be cyclically reduced.
        """
        m_word = MutableWord([])
        for letter in self.word:
            _reduce_word_helper(m_word.word, letter)
        if cyclic:
            _reduce_cyclic(m_word.word)
        return m_word.immutable()

    def concat(self, other: Word) -> Word:
        """
        Returns the result of concatenating the given word with ``self``. The result is **not** reduced.
        """
        addedWord: MutableWord = MutableWord([])
        addedWord.word.extend(self.word)
        addedWord.word.extend(other.word)
        return addedWord.immutable()

    def __iter__(self) -> Iterable[Letter]:
        for i in self.word:
            yield i

    def __mul__(self, other: object) -> Word:
        """
        Words can be multiplied with both letters and words (aliased to concatenation). Unlike :py:meth:`concat`, the result is reduced.
        Right multiplication is also implemented. 

        >>> wfs("a^2") * wfs("b")
        a²b
        >>> wfs("a^2") * wfs("a")
        a³

        See :py:func:`wfs`.
        """
        if isinstance(other, Word):
            return self.concat(other).reduced()
        if isinstance(other, Letter):
            return self * Word((other,))
        else:
            return NotImplemented

    def __rmul__(self, other: object) -> Word:
        if isinstance(other, Word):
            return other.concat(self).reduced()
        if isinstance(other, Letter):
            return Word((other,)) * self
        else:
            return NotImplemented

    def inv(self) -> Word:
        """
        :return: the inverse of the word.
        """
        return MutableWord([Letter(element.sym, -1 * element.exp) for element in self.word[::-1]]).immutable()

    def __pow__(self, exp: Exponent) -> Word:
        """
        Words can be exponentiated.

        >>> wfs("a^3 b^2 c^-3") ** 4
        a³b²c⁻³a³b²c⁻³a³b²c⁻³a³b²c⁻³
        >>> wfs("a^3 b^-2") ** -2
        b²a⁻³b²a⁻³

        """
        if exp < 0:
            return (self**-exp).inv()
        elif exp == 0:
            return Word(())
        else:
            newWord: MutableWord = MutableWord([])
            for _ in range(exp):
                newWord.word.extend(self.word)
            return newWord.immutable()


    @override
    def __repr__(self) -> str:
        """
        Words are represented with unicode characters by default. (LaTeX support coming soon.)
        """
        if self.length == 0:
            return "ε"
        return "".join([str(elem) for elem in self.word])

    @override
    def __eq__(self, other: object, /) -> bool:
        """
        Checks equality of words. Equality is checked between the reduced form of both words. (For strict equality, see :py:meth:`strict_equality`.)

        >>> wfs("a^2 b") == wfs("a^2 b")
        True
        >>> wfs("a^2 b") == wfs("a^2")
        False

        """
        return isinstance(other, Word) and self.reduced().strict_equality(
            other.reduced()
        )

    def strict_equality(self, other: Word) -> bool:
        """
        Checks strict (unreduced) equality.

        >>> wfs("a^2").strict_equality(wfs("a^2"))
        True
        >>> wfs("a^2 b b^-1").strict_equality(wfs("a^2"))
        False

        """
        if len(self.word) != len(other.word):
            return False
        else:
            for i in range(len(self.word)):
                if self.word[i] != other.word[i]:
                    return False
            return True

    @override
    def __hash__(self) -> int:
        return hash(self.word)

    def __len__(self) -> int:
        return self.length

    def infer_free_group(self) -> FreeGroup:
        """
        Infers the :py:class:`FreeGroup` ``self`` is an element of.

        >>> wfs("a^2 b k^3 b^-2").infer_free_group().basis
        SortedSet(['a', 'b', 'k'])

        """
        basis: set[Symbol] = SortedSet()
        for letter in self.word:
            if letter.sym not in basis:
                basis.add(letter.sym)
        return FreeGroup(basis)

    def get_copyable(self) -> str:
        """
        :return: A string that can be read by :py:func:`word_from_str`.
        """
        return " ".join([letter.get_copyable() for letter in self.word])


def _reduce_word_helper(stack: list[Letter], letter: Letter) -> None:
    if letter.exp == 0:
        return
    elif len(stack) == 0:
        stack.append(letter)
    elif stack[-1].sym == letter.sym:
        _reduce_word_helper(stack, Letter(letter.sym, stack.pop().exp + letter.exp))
    else:
        stack.append(letter)


def _reduce_cyclic(stack: list[Letter]) -> None:
    while len(stack) > 1 and stack[0].sym == stack[-1].sym:
        _reduce_word_helper(stack, stack.pop(0))


def word_from_str(raw: str) -> Word:
    """
    Generates a word from a string of the format ``"{sym}^{exp} {letter} ...``. This is consistent with :py:func:`letter_from_str`.
    Use of :py:func:`wfs` is recommended.

    :param str raw: The string to be parsed.
    """
    return Word([letter_from_str(i) for i in raw.split(" ")])

wfs = word_from_str
"""
Alias for :py:func:`word_from_str`.
"""

def _word_from_str_alphabet_helper(char : str) -> Letter:
    return Letter(chr((ord(char) & 0b00001111) | 0b01100000), 1 if (0b00100000 & ord(char)) else -1)

def word_from_str_alphabet(raw : str) -> Word:
    """
    Another way to generate a :py:type:`word` from a string, when your letters are exclusively from the English alphabet. 
    Uppercase letters are considered the inverses of lowercase letters. See below for examples.
    Use of :py:func:`wfsa` is recommended.

    .. warning::
        
        This function does not work properly with non-alphabetic symbols.

    :param str raw: The string to be parsed.
    :return: The returned word is reduced by default.

    >>> word_from_str_alphabet("aaaAbBCCccccc")
    a²c³
    >>> word_from_str_alphabet("AAAABBBBHHHHMMMkk")
    a⁻⁴b⁻⁴h⁻⁴m⁻³k²

    """
    return Word(map(_word_from_str_alphabet_helper, raw)).reduced()

wfsa = word_from_str_alphabet
"""
Alias for :py:func:`word_from_str_alphabet`.
"""

