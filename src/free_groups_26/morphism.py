from sortedcontainers import SortedDict
from .letter import Symbol
from .word import Word, MutableWord


class Morphism:
    morphism_map: dict[Symbol, Word]
    """
    Implemented using a SortedDict from sortedcontainers.
    """

    def __init__(self, map: SortedDict | dict[Symbol, Word]):
        """
        This class represents a morphism.

        :param map: The mapping of the morphism.
        :type map: sortedcontainers.SortedDict or dict[Symbol, Word]

        If a python dictionary is passed, it is automatically converted into a SortedDict. The SortedDict must be a mapping of :py:type:`Symbol` s to :py:class:`Word` s.
        """
        self.morphism_map = SortedDict(map)

    def map(self, word: Word) -> Word:
        """
        Applies the morphism to a given word. If a symbol in the word has a map in :py:attr:`morphism_map`, then the corresponding mapping takes place, otherwise, the symbol is mapped to itself.

        >>> d = SortedDict({'a' : wfs("a b^-1")})
        >>> phi = Morphism(d)
        >>> w = wfs("a^2 b^3")
        >>> phi.map(w)
        ab⁻¹ab²

        """
        newWord = MutableWord([])
        for letter in word.word:
            if letter.sym not in self.morphism_map:
                newWord.word.append(letter)
            else:
                newWord.word.extend((self.morphism_map[letter.sym] ** letter.exp).word)
        return newWord.immutable().reduced()
