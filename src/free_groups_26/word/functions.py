from free_groups_26.free_group import FreeGroup
from free_groups_26.letter import Letter, Symbol, letter_from_str_a, letter_from_str_b
from .defn import Word, reduce_cyclic
import random

__all__ = ["generate_random_word"]


def generate_random_word(group: FreeGroup, length: int, variation: int) -> Word:
    """
    Generates a cyclically reduced pseudo-random word from the given free group.

    :param group: The free group of the generated word.
    :type group: :py:class:`FreeGroup`
    :param int length: The length of the generated word will be roughly around ``length`` :math:`\\pm` ``variation``.
    :param int variation: The absolute value of the highest power of a letter in the free group. For example, if ``variation = 4``, the exponents of
                          the letters in the word are guaranteed to be between 4 and -4.
    """
    newWord: list[Letter] = []
    prevSym: Symbol = ""
    count = 0
    while count <= length:
        sym: Symbol = tuple(group.basis)[random.randint(0, group.rank - 1)]
        if sym == prevSym:
            continue
        prevSym = sym
        expo = 0
        while expo == 0:
            expo = random.randint(-variation, variation)
        newWord.append(Letter(sym, expo))
        count += abs(expo)
    reduce_cyclic(newWord)
    return Word(newWord)


def word_from_str_b(raw: str) -> Word:
    """
    Generates a word from a string of the format ``"{sym}^{exp} {letter} ...``. This is consistent with :py:func:`letter_from_str_b`.
    Use of :py:func:`read` is recommended.

    :param str raw: The string to be parsed.

    >>> word_from_str("a^2 b^3")
    a^2 b^3

    """
    return Word(letter_from_str_b(i) for i in raw.split(" "))


def word_from_str_a(raw: str) -> Word:
    """
    Another way to generate a :py:type:`word` from a string, when your letters are exclusively from the English alphabet.
    Uppercase letters are considered the inverses of lowercase letters. See below for examples.
    Use of :py:func:`read` is recommended.

    See :py:func:`letter_from_str_alphabet`.

    :param str raw: The string to be parsed.
    :return: The returned word is reduced by default.

    >>> str(word_from_str_alphabet("aaaAbBCCccccc"))
    aaaAbBCCccccc
    >>> str(word_from_str_alphabet("AAAABBBBHHHHMMMkk"))
    AAAABBBBHHHHMMMkk

    """
    return Word(map(letter_from_str_a, raw))


def word_from_str(inp: str) -> Word:
    """
    Parses a word from a string. Guesses the correct function to use from :py:func:`word_from_str_alphabet` and :py:func:`word_from_str` based on whether there is a
    caret ``^`` in the input. Recommended in most cases.
    """
    if "^" in inp:
        return word_from_str_b(inp)
    else:
        return word_from_str_a(inp)


read = word_from_str
"""
Alias to :py:func:`word_from_str`. Recommended when brevity is desired.
"""
