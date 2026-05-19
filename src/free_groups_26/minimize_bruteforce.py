from collections.abc import Iterable
from .morphism import Morphism
from .whitehead_automorphism import generate_all_t2_whitehead_automorphisms
from .word import Word

def minimize_once_bruteforce(word : Word, morphism_list : Iterable[Morphism], /, log : list[str] | None = None) -> tuple[Word, bool]:
    """
    Minimizes a word once, if possible.

    :param word: The word to be minimized.
    :param morphism_list: The list of all morphisms to try while minimizing the word.
    :param log: (*keyword argument only*) If there exists a morphism that reduces a word, its string and the new word is appended to the log, if passed.
    :return: Returns a tuple of (:py:class:`Word`, ``bool``). The second element specifies whether the word was reduced.

    """
    has_log : bool = log is not None
    current_length  = word.length
    for morphism in morphism_list:
        new_word = morphism.map(word)
        if new_word.length < current_length:
            if has_log:
                log.append(str((morphism.morphism_map, new_word)))
            return (new_word, True)
    if has_log:
        log.append("False")
    return (word, False)

def minimize_bruteforce(word : Word, morphism_list : Iterable[Morphism] | None = None, /, log : list[str] | None = None) -> Word:
    """
    Returns the minimized form of the word, which might be the same word.

    :param morphism_list: If an iterable of morphisms is not provided, :py:func:`generate_all_t2_whitehead_automorphisms` is used to generate all possible Whitehead automorphisms for the given word. It is recommended that the list is generated and passed if working with multiple words from the same free group.
    :param log: *(keyword argument only)* All mimization operations are appended as strings to the log, if passed.

    >>> log = []
    >>> minimize_bruteforce(wfs("a b^2 c"), log=log), log
    (c,
     ["(SortedDict({'a': ab⁻¹}), abc)",
      "(SortedDict({'b': a⁻¹b}), bc)",
      "(SortedDict({'c': b⁻¹c}), c)",
      'False'])

    """
    if morphism_list is None:
        morphism_list = generate_all_t2_whitehead_automorphisms(word.infer_free_group())
    new_word = word
    while True:
        new_word, reduced_in_cycle = minimize_once_bruteforce(new_word, morphism_list, log)
        if not reduced_in_cycle:
            break
    return new_word

