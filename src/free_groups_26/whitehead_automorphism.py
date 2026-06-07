from collections.abc import Iterable, Generator
from itertools import chain, combinations
from typing import Any

from sortedcontainers import SortedDict, SortedSet

from .free_group import FreeGroup
from .letter import Letter, Symbol
from .morphism import Morphism
from .word import Word


def _powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def generate_whitehead_automorphism_t2(x: Letter, A: Iterable[Letter]) -> Morphism:
    """
    This function generates a Type 2 Whitehead Automorphism, using the following piecewise definition. (Credit: Virning, 1988)

    .. math::

        (A, x) y = \\begin{cases} 
            yx & \\text{if } y \\in A, \\bar{y} \\notin A, y \\notin \\{x, \\bar{x}\\} \\\\ 
            \\bar{x} y & \\text{if } y \\notin A, \\bar{y} \\in A, y \\notin \\{x, \\bar{x}\\} \\\\ 
            \\bar{x} yx & \\text{if } y, \\bar{y} \\in A \\\\ 
            y & \\text{otherwise} 
        \\end{cases}

    :param x: Corresponds to :math:`x` in the definition.
    :param A: Corresponds to :math:`A` in the definition.

    Instead of iterating through all the symbols in a free group, this function only goes through the symbols in ``A`` as the rest get mapped to themselves.

    >>> wh = generate_whitehead_automorphism_t2(lfs("b"), {lfs("a"), lfs("a^-1"), lfs("b"), lfs("c^-1")})
    >>> print(wh.morphism_map)
    SortedDict({'a': b⁻¹ab, 'c': b⁻¹c})
    >>> print(wh.map(wfsa("bac")))
    ac

    """

    phi_map: dict[Symbol, Word] = SortedDict()

    for ysym in SortedSet([k.sym for k in A]):
        y = Letter(ysym, 1)

        if y not in [x, x.inv()]:
            if y in A and y.inv() in A:
                phi_map[ysym] = Word((x.inv(), y, x))
            elif y in A:
                phi_map[ysym] = Word((y, x))
            else:
                phi_map[ysym] = Word((x.inv(), y))

    return Morphism(phi_map)


def generate_all_t2_whitehead_automorphisms(
    inp: FreeGroup | set[Symbol],
) -> list[Morphism]:
    """
    This function generates all Type 2 Whitehead Automorphisms for a given set of symbols. This function has a time and space complexity of :math:`O(4^n)`.
    """
    L_n = inp.alphabet if isinstance(inp, FreeGroup) else FreeGroup(inp).alphabet
    morphism_list: list[Morphism] = []
    for A in _powerset(L_n):
        for x in A:
            if x.inv() in A:
                continue
            phi = generate_whitehead_automorphism_t2(x, A)
            if phi.morphism_map != {}:
                morphism_list.append(phi)
    return morphism_list


def generate_t2_wh_aut_lazy(
    inp: FreeGroup | set[Symbol],
) -> Generator[Morphism, Any, None]:
    """
    Lazily generates all the Type 2 Whitehead Automorphisms for the given set of symbols / :py:class:`FreeGroup`.
    Similar to :py:func:`generate_all_t2_whitehead_automorphisms`, but recommended for more efficient memory usage.
    """
    L_n = inp.alphabet if isinstance(inp, FreeGroup) else FreeGroup(inp).alphabet
    for A in _powerset(L_n):
        for x in A:
            if x.inv() in A:
                continue
            phi = generate_whitehead_automorphism_t2(x, A)
            if phi.morphism_map != {}:
                yield phi
