from __future__ import annotations
from typing import override

_format_map = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³"}
for i in range(4, 10):
    _format_map[str(i)] = chr(0x2070 + i)

type Symbol = str
type Exponent = int


class Letter:
    sym: Symbol
    exp: Exponent

    def __init__(self, symbol: Symbol, exponent: Exponent) -> None:
        """
        This class represents a letter.

        .. note::

            Public access of both instance variables (:py:attr:`sym` and :py:attr:`exp`) is encouraged.

        :param symbol: The symbol of the letter. All strings are valid symbols.
        :type symbol: :py:type:`Symbol`
        :param exponent: The exponent of the letter.
        :type exponent: :py:type:`Exponent`

        >>> Letter("a", 1)
        a
        >>> Letter("x", 3)
        x³
        """
        self.sym = symbol  #:
        self.exp = exponent  #:

    @override
    def __eq__(self, other: object) -> bool:
        """
        Checks for equality between two letters. Two letters are equal :math:`\\iff` the symbol and the exponent are equal.
        Returns ``NotImplemented`` if ``other`` is not a :py:type:`Letter`.

        :param other: The letter to compare against.
        :type other: :py:type:`object`

        >>> Letter("a", 4) == Letter("a", 4)
        True
        >>> Letter("a", 2) == Letter("b", 3)
        False

        """
        if not isinstance(other, Letter):
            return NotImplemented
        return self.sym == other.sym and self.exp == other.exp

    @override
    def __repr__(self) -> str:
        if self.exp == 1:
            return self.sym
        else:
            return self.sym + "".join([_format_map[i] for i in str(self.exp)])

    def __lt__(self, other: object) -> bool:
        """
        Checks if ``self < other``. The following ordering is followed:

        .. math::

            a < a^2 < \\ldots < a^{-2} < a^{-1} < b < \\ldots

        :param object other: The object to compare against.

        Returns ``NotImplemented`` if ``other`` is not a :py:type:`Letter`.

        """
        if not isinstance(other, Letter):
            return NotImplemented
        else:
            return (self.sym < other.sym) and (self.exp < other.exp)

    @override
    def __hash__(self) -> int:
        return hash((self.sym, self.exp))

    def get_copyable(self) -> str:
        """
        :return: A string that can be read by :py:func:`letter_from_str`.
        """
        return "{}^{}".format(self.sym, self.exp)

    def is_inverse(self) -> bool:
        return self.exp < 0

    def inv(self) -> Letter:
        return Letter(self.sym, -self.exp)

    def get_base(self) -> Letter:
        return Letter(self.sym, (self.exp > 0) - (self.exp < 0))


def letter_from_str(raw: str) -> Letter:
    """
    Returns a letter from a string of the format ``{sym}^{exp}``.

    .. hint::

        :py:func:`lfs` is a concise alias for :py:func:`letter_from_str`.

    >>> letter_from_str("b^32")
    b³²

    """
    splits = raw.split("^")
    if len(splits) == 1:
        return Letter(splits[0], 1)
    return Letter(splits[0], int(splits[1]))


lfs = letter_from_str
"""
Alias for :py:func:`letter_from_str`.

.. seealso::

    https://www.linuxfromscratch.org/

"""


def letter_from_str_alphabet(char: str) -> Letter:
    """
    Another way to generate a letter from a string. This function works exclusively on the English Alphabet, where it considers uppercase letters the inverse of lowercase letters.

    .. warning::

        This function does not work properly with non-alphabetic symbols as it involves bitwise operations.

    >>> letter_from_str_alphabet("a")
    a
    >>> letter_from_str_alphabet("A")
    a⁻¹

    """
    return Letter(
        chr((ord(char) & 0b00001111) | 0b01100000),
        1 if (0b00100000 & ord(char)) else -1,
    )


lfsa = letter_from_str_alphabet
"""
Alias for :py:func:`letter_from_str_alphabet`.
"""
