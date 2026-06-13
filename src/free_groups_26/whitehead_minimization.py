from networkx import minimum_cut, NetworkXError
from networkx.algorithms.flow import edmonds_karp
from sortedcontainers import SortedDict

from free_groups_26.log import Log, LogItem

from .free_group import FreeGroup, get_free_group
from .letter import Letter, Symbol
from .morphism import Morphism
from .word import Word
from .whitehead_automorphism import generate_whitehead_automorphism_t2
from .whitehead_graph import WhiteheadGraph, generate_whg


def minimize_whitehead_once(
    word: Word, /, fg: FreeGroup | None = None, log: Log | None = None
) -> Word | None:
    """
    Performs Whitehead Minimization once.

    :param word: The word to be minimized.
    :param fg: An optional free group can be passed if you wish to avoid the overhead of inferring the free group from the word. (Recommended for large words.)
    :type fg: :py:class:`FreeGroup` or ``None``
    :param log: An optional log. If passed, all morphisms tried will be appended as strings, with some other information.
    :type log: :py:type:`Log` or ``None``.
    :return: If minimal, returns ``None``, otherwise returns the once-minimized word.

    **Current Implementation**: Iterate through the alphabet of the free group (inferred or given), if the max flow of the current alphabet to its inverse is less than its degree, try creating and applying a whitehead
    automorphism with :py:func:`generate_whitehead_automorphism_t2`. If the length of the word is less than the given word (not guaranteed by a min cut), return it, otherwise continue iterating.

    The min cut is computed using Edmonds Karp.

    >>> log = new_log()
    >>> minimize_whitehead_once(rd("a b^2 c"), log=log)
    b²c
    >>> display_log(log)
    b²c : SortedDict({'b': a⁻¹ba, 'c': a⁻¹c})

    """
    graph: WhiteheadGraph = generate_whg(word)
    if fg is None:
        fg = word.infer_free_group()

    for letter in fg.alphabet:
        try:
            value, partitions = minimum_cut(
                graph, letter, letter.inv(), capacity="weight", flow_func=edmonds_karp
            )
            partitions: tuple[set[Letter], set[Letter]]
            value: int
        except NetworkXError:
            continue
        if value < graph.degree(letter, weight="weight"):
            phi = generate_whitehead_automorphism_t2(letter, partitions[0])
            new_word = phi.map(word, True)
            if log is not None:
                log.append(LogItem(new_word, phi))
            if new_word.length < word.length:
                return new_word
    else:
        return None


def minimize_whitehead(
    word: Word, /, fg: FreeGroup | None = None, log: Log | None = None
) -> Word:
    """
    Whitehead Minimizes a word.

    :param word: The word to be minimized.
    :param fg: The optional free group. If not passed, it is inferred from the word.
    :type fg: :py:class:`FreeGroup` or ``None``
    :param log: All operations performed are appended to the log, if passed.
    :type log: :py:type:`Log` or ``None``.

    **Current Implementation**: Keep trying :py:func:`minimize_whitehead_once` on the word, reassigning the returns. If it returns a ``None``, then this function returns the minimized word.

    >>> minimize_whitehead(wfs("c^-3 b^-1 a^2"))
    c⁻¹

    """
    fg = fg if fg is not None else word.infer_free_group()
    new_word = word
    while True:
        minimized = minimize_whitehead_once(new_word, fg=fg, log=log)
        if minimized is None:
            break
        new_word = minimized
    return new_word


def is_minimal(word: Word, fg: FreeGroup | None = None) -> bool:
    """
    :return: Whether the word is already whitehead minimal.
    """
    return minimize_whitehead(word, fg=fg) == word


def type_1_minimize(word: Word) -> tuple[Word, Morphism]:
    """
    Finds a Type 1 Whitehead Automorphism that makes the word lexicographically minimal.

    >>> w = rd("k m^-1 y^-2 m y")
    >>> nw, m = type_1_minimize(w)
    >>> nw, m.morphism_map
    (abc²b⁻¹c⁻¹, SortedDict({'k': a, 'm': b⁻¹, 'y': c⁻¹}))

    """
    canonical_free_group = get_free_group(word.infer_free_group().rank)
    generator = iter(canonical_free_group.basis)
    word_iter = iter(word)
    phi_map: dict[Symbol, Word] = SortedDict()
    while len(phi_map) < canonical_free_group.rank:
        curr_letter = next(word_iter)
        if curr_letter.sym not in phi_map:
            phi_map[curr_letter.sym] = Word(
                (Letter(next(generator), curr_letter.get_base().exp),)
            )
    phi = Morphism(phi_map)
    return (phi(word), phi)
