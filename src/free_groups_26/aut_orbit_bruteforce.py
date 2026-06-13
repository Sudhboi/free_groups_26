from warnings import warn
from free_groups_26.morphism import Morphism
from free_groups_26.whitehead_automorphism import generate_t2_wh_aut_lazy
from free_groups_26.whitehead_minimization import is_minimal
from free_groups_26.word import Word


def find_minimal_automorphic_orbit(word: Word) -> list[tuple[Morphism, Word]]:
    aut_list: list[tuple[Morphism, Word]] = []
    if not is_minimal(word):
        warn("Finding automorphic orbit of non-minimal word.")
    for phi in generate_t2_wh_aut_lazy(word.infer_free_group()):
        new_word = phi(word)
        if new_word.length == word.length:
            aut_list.append((phi, new_word))
    return aut_list
