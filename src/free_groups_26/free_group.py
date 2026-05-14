from .letter import Symbol, Letter


class FreeGroup:

    basis: tuple[Symbol, ...]
    alphabet: tuple[Letter, ...]
    rank: int

    def __init__(self, basis: tuple[Symbol, ...]) -> None:
        self.basis = basis
        self.rank = len(basis)
        temp_alphabet: list[Letter] = []
        for sym in basis:
            temp_alphabet.extend([Letter(sym, power) for power in [-1, 1]])
        self.alphabet = tuple(temp_alphabet)

    def get_hash_dict(self) -> dict[int, Letter]:
        hash_dict: dict[int, Letter] = dict()
        for elem in self.alphabet:
            hash_dict[hash(elem)] = elem
        return hash_dict


def get_free_group(rank: int) -> FreeGroup:
    basisList: list[str] = []
    for i in range(97, 97 + rank):
        basisList.append(chr(i))
    return FreeGroup(tuple(basisList))
