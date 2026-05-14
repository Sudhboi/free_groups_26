from __future__ import annotations
from collections.abc import Iterable
from typing import override
from .letter import Letter, Exponent, Symbol, letter_from_str
from .free_group import FreeGroup


class MutableWord:
    word: list[Letter]

    def __init__(self, letters: list[Letter]) -> None:
        self.word = letters

    def immutable(self) -> Word:
        return Word(tuple(self.word))


class Word:
    word: tuple[Letter, ...]
    length: int = 0
    free_group: FreeGroup

    def __init__(self, word: tuple[Letter, ...], fg: FreeGroup | None = None) -> None:
        self.word = word
        for letter in word:
            self.length += abs(letter.exp)
        if fg == None:
            self.free_group = _infer_free_group(self)
        else:
            self.free_group = fg

    def reduced(self, cyclic: bool = False) -> Word:
        m_word = MutableWord([])
        for letter in self.word:
            _reduce_word_helper(m_word.word, letter)
        if cyclic:
            _reduce_cyclic(m_word.word)
        return m_word.immutable()

    def concat(self, other: Word) -> Word:
        addedWord: MutableWord = MutableWord([])
        addedWord.word.extend(self.word)
        addedWord.word.extend(other.word)
        return addedWord.immutable()

    def __iter__(self) -> Iterable[Letter]:
        for i in self.word:
            yield i

    def __mul__(self, other: object) -> Word:
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

    def __pow__(self, exp: Exponent) -> Word:
        if exp < 0:
            return (self**-exp).inv()
        elif exp == 0:
            return Word(())
        else:
            newWord: MutableWord = MutableWord([])
            for _ in range(exp):
                newWord.word.extend(self.word)
            return newWord.immutable()

    def inv(self) -> Word:
        return self**-1

    @override
    def __repr__(self) -> str:
        if self.length == 0:
            return "ε"
        return "".join([str(elem) for elem in self.word])

    def strictEquality(self, other: Word) -> bool:
        if len(self.word) != len(other.word):
            return False
        else:
            for i in range(len(self.word)):
                if self.word[i] != other.word[i]:
                    return False
            return True

    @override
    def __eq__(self, other: object, /) -> bool:
        return isinstance(other, Word) and self.reduced().strictEquality(
            other.reduced()
        )

    @override
    def __hash__(self) -> int:
        return hash(self.word)

    def __len__(self) -> int:
        return self.length

    def get_copyable(self) -> str:
        return " ".join([letter.get_copyable() for letter in self.word])


def word_from_str(raw: str) -> Word:
    return Word(tuple([letter_from_str(i) for i in raw.split(" ")]))


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


def _infer_free_group(word: Word) -> FreeGroup:
    basis: list[Symbol] = []
    for letter in word.word:
        if letter.sym not in basis:
            basis.append(letter.sym)
    return FreeGroup(tuple(basis))
