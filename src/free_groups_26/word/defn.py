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

    def __init__(self, word: Iterable[Letter], cyclically_reduce: bool = False) -> None:
        """
        This class represents a word.

        :param word: Any :py:type:`Iterable` containing :py:class:`Letter` s is accepted.
        """
        super().__init__()
        m_word: list[Letter] = []
        for letter in word:
            reduce_word_helper(m_word, letter)
        if cyclically_reduce:
            reduce_cyclic(m_word)
        self.word = tuple(m_word)
        self.length = sum(abs(x.exp) for x in self.word)

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

    def inv(self) -> Word:
        return Word(
            Letter(element.sym, -1 * element.exp) for element in self.word[::-1]
        )

    @override
    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Word) and self.word == value.word

    @override
    def __hash__(self) -> int:
        return hash(self.word)

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
        :return: whether the word is cyclically reduced. Assumes that the given word is reduced linearly.
        """
        if len(self.word) <= 1:
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

    @override
    def __repr__(self) -> str:
        """
        Words are represented with unicode characters by default.
        """
        if self.length == 0:
            return "ε"
        return " ".join([repr(elem) for elem in self.word])

    @override
    def __str__(self) -> str:
        """
        Words are represented with unicode characters by default.
        """
        if self.length == 0:
            return "ε"
        return "".join([str(elem) for elem in self.word])


def reduce_word_helper(stack: list[Letter], letter: Letter) -> None:
    if letter.exp == 0:
        return
    elif len(stack) == 0:
        stack.append(letter)
    elif stack[-1].sym == letter.sym:
        reduce_word_helper(stack, Letter(letter.sym, stack.pop().exp + letter.exp))
    else:
        stack.append(letter)


def reduce_cyclic(stack: list[Letter]) -> None:
    while len(stack) > 1 and stack[0].sym == stack[-1].sym:
        reduce_word_helper(stack, stack.pop(0))


class ReducedWord(Word):
    def __init__(self, word: Iterable[Letter], cyclic: bool = False) -> None:
        m_word: list[Letter] = []
        for letter in self.word:
            reduce_word_helper(m_word, letter)
        if cyclic:
            reduce_cyclic(m_word)
        super().__init__(m_word)
