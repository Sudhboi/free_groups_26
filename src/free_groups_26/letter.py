"""
This submodule deals with Letters. Exposes the Letter class and a method to read letters, namely :py:func:`letter_from_str`.
"""

from __future__ import annotations
from typing import override

from dataclasses import dataclass
from functools import total_ordering

__all__ = [
    "Letter",
    "Symbol",
    "Exponent",
    "letter_from_str",
    "letter_from_str_a",
    "letter_from_str_b",
]

type Symbol = str
type Exponent = int


@total_ordering
@dataclass(frozen=True, slots=True)
class Letter:
    """
    This class represents a letter. Implements a total ordering, ``__eq__`` and ``__hash__``.

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

    sym: Symbol  #:
    exp: Exponent  #:

    @override
    def __repr__(self) -> str:
        if self.exp == 1:
            return self.sym
        else:
            return self.sym + "^" + str(self.exp)

    @override
    def __str__(self) -> str:
        return abs(self.exp) * (self.sym if self.exp >= 0 else self.sym.upper())

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
            if self.sym < other.sym:
                return True
            else:
                if self.exp * other.exp > 0:
                    return self.exp < other.exp
                else:
                    return self.exp > 0

    def is_inverse(self) -> bool:
        """
        Returns ``True`` if the exponent is less than 0.
        """
        return self.exp < 0

    def inv(self) -> Letter:
        """
        Returns the inverse.
        """
        return Letter(self.sym, -self.exp)

    def get_base(self) -> Letter:
        """
        Returns the base of the letter, which is defined as :math:`a^{\\frac{b}{|b|}}` for :math:`a^b`.
        """
        return Letter(self.sym, (self.exp > 0) - (self.exp < 0))


def letter_from_str_b(raw: str) -> Letter:
    """
    Returns a letter from a string of the format ``{sym}^{exp}``.

    >>> letter_from_str_b("b^32")
    b³²

    """
    splits = raw.split("^")
    if len(splits) == 1:
        return Letter(splits[0], 1)
    return Letter(splits[0], int(splits[1]))


def letter_from_str_a(char: str) -> Letter:
    """
    Another way to generate a letter from a string. This function works exclusively on the English Alphabet, where it considers uppercase letters the inverse of lowercase letters.

    >>> letter_from_str_a("a")
    a
    >>> letter_from_str_a("A")
    a⁻¹

    """
    return Letter(
        char.lower(),
        1 if char.islower() else -1,
    )


def letter_from_str(char: str) -> Letter:
    """
    Use of this function is always recommended. Intelligently chooses between the two types of conversion.

    >>> letter_from_str("b^32")
    b³²
    >>> letter_from_str("a")
    a
    >>> letter_from_str("A")
    a⁻¹

    """
    return letter_from_str_b(char) if "^" in char else letter_from_str_a(char)
