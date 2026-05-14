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
        self.sym = symbol
        self.exp = exponent

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Letter):
            return NotImplemented
        return self.sym == other.sym and self.exp == other.exp

    @override
    def __repr__(self) -> str:
        if self.exp == 1:
            return self.sym
        else:
            return self.sym + "".join([format_map[i] for i in str(self.exp)])

    @override
    def __hash__(self) -> int:
        return hash((self.sym, self.exp))

    def get_copyable(self) -> str:
        return "{}^{}".format(self.sym, self.exp)

    def isInverse(self) -> bool:
        return self.exp < 0


def letter_from_str(raw: str) -> Letter:
    splits = raw.split("^")
    if len(splits) == 1:
        return Letter(splits[0], 1)
    return Letter(splits[0], int(splits[1]))
