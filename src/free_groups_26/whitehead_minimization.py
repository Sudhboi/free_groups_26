from networkx import minimum_cut, NetworkXError
from networkx.algorithms.flow import edmonds_karp

from .free_group import FreeGroup
from .letter import Letter
from .word import Word
from .whitehead_automorphism import generate_whitehead_automorphism_t2
from .whitehead_graph import WhiteheadGraph, draw_graph, generate_whg


def find_min_cut_partition(
    whg: WhiteheadGraph, letter: Letter
) -> None | set[Letter]:
    value, partitions = minimum_cut(whg, letter, letter.inv(), capacity="weight", flow_func=edmonds_karp)
    if value >= whg.degree(letter, weight="weight"):
        return None
    else:
        return partitions[0]

def minimize_whitehead_once(word : Word,/,  fg : FreeGroup | None = None, log : list[str] | None = None) -> Word | None:
    graph = generate_whg(word)
    if fg is None:
        fg = word.infer_free_group()

    for letter in fg.alphabet:
        try:
            part = find_min_cut_partition(graph, letter)
        except NetworkXError:
            continue
        if part is not None:
            phi = generate_whitehead_automorphism_t2(letter, part)
            new_word = phi.map(word)
            if log is not None:
                log.append(str((phi.morphism_map, letter, part, new_word)))
            if new_word.length < word.length:
                return new_word
    else:
        if log is not None:
            log.append("Minimal")
        return None

def minimize_whitehead(word : Word, /, log : list[str] | None = None) -> Word:
    fg = word.infer_free_group()
    new_word = word
    while True:
        minimized = minimize_whitehead_once(new_word,fg=fg, log=log)
        if log is not None:
            log.append(str(minimized))
        if minimized is None:
            break
        new_word = minimized
    return new_word
