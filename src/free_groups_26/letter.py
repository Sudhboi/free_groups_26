from typing import override

format_map = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³"}
for i in range(4, 10):
    format_map[str(i)] = chr(0x2070 + i)

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

        >>> fg.Letter("a", 1)
        a
        >>> fg.Letter("x", 3)
        x³
        """
        self.sym = symbol #:
        self.exp = exponent #:

    @override
    def __eq__(self, other: object) -> bool:
        """
        Checks for equality between two letters. Two letters are equal :math:`\\iff` the symbol and the exponent are equal.
        Returns ``NotImplemented`` if ``other`` is not a :py:type:`Letter`.

        :param other: The letter to compare against.
        :type other: :py:type:`object`

        >>> fg.Letter("a", 4) == fg.Letter("a", 4)
        True
        >>> fg.Letter("a", 2) == fg.Letter("b", 3)
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
            return self.sym + "".join([format_map[i] for i in str(self.exp)])

    def __lt__(self, other : object) -> bool:
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
        return "{}^{}".format(self.sym, self.exp)

    def isInverse(self) -> bool:
        return self.exp < 0


def letter_from_str(raw: str) -> Letter:
    """
    Returns a letter from a string of the format ``{sym}^{exp}``.

    .. hint::

        :py:func:`lfs` is a concise alias for :py:func:`letter_from_str`.

    >>> fg.letter_from_str("b^32")
    b³²

    """
    splits = raw.split("^")
    if len(splits) == 1:
        return Letter(splits[0], 1)
    return Letter(splits[0], int(splits[1]))

lfs = letter_from_str
"""
`Alias`_ for :py:func:`letter_from_str`.

.. _Alias: https://www.linuxfromscratch.org/
"""
