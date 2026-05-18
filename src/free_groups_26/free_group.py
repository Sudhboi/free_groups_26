from .letter import Symbol, Letter
from sortedcontainers import SortedSet


class FreeGroup:

    basis: set[Symbol]  #: Implemented using a SortedSet from sortedcontainers.
    alphabet: set[Letter]
    """
    Also implemented using a SortedSet. Represented by :math:`X^{\\pm}`.

    Automatically inferred from :py:attr:`basis`. For :math:`x \\in X`, :math:`x, x^{-1} \\in X^{\\pm}`.
    """
    rank: int  #: Automatically inferred from :py:attr:`basis`.

    def __init__(self, basis: set[Symbol]) -> None:
        """
        This class represents a Free Group.

        :param basis: The basis of the free group.
        :type basis: set[Symbol]
        """
        self.basis = SortedSet(basis)
        self.rank = len(basis)
        temp_alphabet: set[Letter] = SortedSet()
        for sym in basis:
            temp_alphabet.add(Letter(sym, 1))
            temp_alphabet.add(Letter(sym, -1))
        self.alphabet = temp_alphabet

    def _get_hash_dict(self) -> dict[int, Letter]:
        hash_dict: dict[int, Letter] = dict()
        for elem in self.alphabet:
            hash_dict[hash(elem)] = elem
        return hash_dict


def get_free_group(rank: int) -> FreeGroup:
    """
    Generates a free group of the given rank. The basis of the free group will be the symbols from the English Alphabet from ``a`` (in unicode order).

    :param int rank: The rank of the free group.
    """
    basisSet: set[Symbol] = SortedSet()
    for i in range(97, 97 + rank):
        basisSet.add(chr(i))
    return FreeGroup(basisSet)
