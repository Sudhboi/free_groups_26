type Symbol = str
type Exponent = int


class Letter:
    sym: Symbol
    exp: Exponent

    def __init__(self, symbol: Symbol, exponent: Exponent) -> None:
        self.sym = symbol
        self.exp = exponent
