from collections.abc import Iterable, MutableSet, Sequence
from symtable import Symbol
from typing import overload, override

from sortedcontainers import SortedSet

from free_groups_26.free_group import FreeGroup
from free_groups_26.letter import Exponent, Letter

__all__ = ["Word"]


class Word(Sequence[Letter]):
    word: tuple[Letter, ...]
    length: int

    def __init__(self, word: Iterable[Letter]) -> None:
        """
        This class represents a word.

        :param word: Any :py:type:`Iterable` containing :py:class:`Letter` s is accepted.
        """
        super().__init__()
        self.word = tuple(word)
        self.length = sum(abs(l.exp) for l in self.word)

    @override
    def __len__(self) -> int:
        return self.length

    @overload
    def __getitem__(self, index: int) -> Letter: ...

    @overload
    def __getitem__(self, index: slice) -> Word: ...

    @override
    def __getitem__(self, index: int | slice) -> Letter | Word:
        if isinstance(index, int):
            return self.word[index]
        else:
            return Word(self.word[index])

    def reduced(self, cyclic: bool = False) -> Word:
        """
        Reduces the word. Uses a stack to perform reduction in :math:`O(n)`.

        :param cyclic: If the word is to be cyclically reduced.
        """
        m_word: list[Letter] = []
        for letter in self.word:
            _reduce_word_helper(m_word, letter)
        if cyclic:
            _reduce_cyclic(m_word)
        return Word(m_word)

    def __mul__(self, other: object) -> Word:
        if isinstance(other, Word):
            return Word(self.word + other.word)
        elif isinstance(other, Letter):
            return Word(self.word + (other,))
        else:
            return NotImplemented

    def __rmul__(self, other: object) -> Word:
        if isinstance(other, Word):
            return other * self
        elif isinstance(other, Letter):
            return Word((other,) + self.word)
        else:
            return NotImplemented

    def strict_equals(self, other: Word) -> bool:
        """
        Checks strict (unreduced) equality.

        >>> read("aa").strict_equality(read("aa"))
        True
        >>> read("aabB").strict_equality(read("aa"))
        False

        """
        return self.word == other.word

    def inv(self) -> Word:
        return Word(
            Letter(element.sym, -1 * element.exp) for element in self.word[::-1]
        )

    @override
    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Word) and self.reduced().strict_equals(value.reduced())

    @override
    def __hash__(self) -> int:
        return hash(self.reduced().word)

    def __pow__(self, exp: Exponent) -> Word:
        """
        Words can be exponentiated.

        >>> read("a^3 b^2 c^-3") ** 4
        a³b²c⁻³a³b²c⁻³a³b²c⁻³a³b²c⁻³
        >>> read("a^3 b^-2") ** -2
        b²a⁻³b²a⁻³

        """
        if exp < 0:
            return (self**-exp).inv()
        elif exp == 0:
            return Word(())
        else:
            newWord: list[Letter] = []
            for _ in range(exp):
                newWord.extend(self.word)
            return Word(newWord)

    def is_cyclically_reduced(self) -> bool:
        """
        :return: whether the word is cyclically reduced.
        """
        if self.length <= 1:
            return True
        return self.word[0].sym != self.word[-1].sym

    def infer_free_group(self) -> FreeGroup:
        """
        Infers the :py:class:`FreeGroup` ``self`` is an element of.

        >>> wfs("a^2 b k^3 b^-2").infer_free_group().basis
        SortedSet(['a', 'b', 'k'])

        """
        basis: MutableSet[Symbol] = SortedSet()
        for letter in self.word:
            if letter.sym not in basis:
                basis.add(letter.sym)  # pyright: ignore[reportUnknownMemberType]
        return FreeGroup(basis)


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
