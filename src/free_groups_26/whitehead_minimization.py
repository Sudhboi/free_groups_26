from networkx import minimum_cut, NetworkXError
from networkx.algorithms.flow import edmonds_karp

from .free_group import FreeGroup
from .letter import Letter
from .word import Word
from .whitehead_automorphism import generate_whitehead_automorphism_t2
from .whitehead_graph import WhiteheadGraph, generate_whg


def minimize_whitehead_once(
    word: Word, /, fg: FreeGroup | None = None, log: list[str] | None = None
) -> Word | None:
    """
    Performs Whitehead Minimization once.

    :param word: The word to be minimized.
    :param fg: An optional free group can be passed if you wish to avoid the overhead of inferring the free group from the word. (Recommended for large words.)
    :type fg: :py:class:`FreeGroup` or ``None``
    :param log: An optional log. If passed, all morphisms tried will be appended as strings, with some other information.
    :type log: ``list[str]`` or ``None``
    :return: If minimal, returns ``None``, otherwise returns the once-minimized word.

    **Current Implementation**: Iterate through the alphabet of the free group (inferred or given), if the max flow of the current alphabet to its inverse is less than its degree, try creating and applying a whitehead
    automorphism with :py:func:`generate_whitehead_automorphism_t2`. If the length of the word is less than the given word (not guaranteed by a min cut), return it, otherwise continue iterating.

    The min cut is computed using Edmonds Karp.

    >>> log = []
    >>> print(minimize_whitehead_once(wfs("c^-3 b^-1 a^2"), log=log))
    c⁻³b⁻¹a
    >>> print(log)
    ["(SortedDict({'b': ba, 'c': a⁻¹ca}), a, {a, c, b, c⁻¹}, a⁻¹c⁻³b⁻¹a²)", "(SortedDict({'b': ab}), a⁻¹, {b⁻¹, a⁻¹}, c⁻³b⁻¹a)"]

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
            new_word = phi(word)
            if log is not None:
                log.append(str((phi.morphism_map, letter, partitions[0], new_word)))
            if new_word.length < word.length:
                return new_word
    else:
        if log is not None:
            log.append("Minimal")
        return None


def minimize_whitehead(
    word: Word, /, fg: FreeGroup | None = None, log: list[str] | None = None
) -> Word:
    """
    Whitehead Minimizes a word.

    :param word: The word to be minimized.
    :param fg: The optional free group. If not passed, it is inferred from the word.
    :type fg: :py:class:`FreeGroup` or ``None``
    :param log: All operations performed are appended to the log, if passed.
    :type log: ``list[str]`` or ``None``

    **Current Implementation**: Keep trying :py:func:`minimize_whitehead_once` on the word, reassigning the returns. If it returns a ``None``, then this function returns the minimized word.

    >>> minimize_whitehead(wfs("c^-3 b^-1 a^2"))
    c⁻¹

    """
    fg = fg if fg is not None else word.infer_free_group()
    new_word = word
    while True:
        minimized = minimize_whitehead_once(new_word, fg=fg, log=log)
        if log is not None:
            log.append(str(minimized))
        if minimized is None:
            break
        new_word = minimized
    return new_word
