from collections.abc import Iterable

from free_groups_26.log import Log, LogItem
from .morphism import Morphism
from .whitehead_automorphism import (
    generate_all_t2_whitehead_automorphisms,
    generate_t2_wh_aut_lazy,
)
from .word import Word


def minimize_once_bruteforce(
    word: Word, morphism_list: Iterable[Morphism], /, log: Log | None = None
) -> tuple[Word, bool]:
    """
    Minimizes a word once, if possible.

    :param word: The word to be minimized.
    :param morphism_list: The list of all morphisms to try while minimizing the word.
    :param log: (*keyword argument only*) Optional argument. The new word and the morphism used will be appended.
    :return: Returns a tuple of (:py:class:`Word`, ``bool``). The second element specifies whether the word was reduced.

    """
    has_log: bool = log is not None
    current_length = word.length
    for morphism in morphism_list:
        new_word = morphism.map(word)
        if new_word.length < current_length:
            if has_log:
                log.append(LogItem(new_word, morphism))
            return (new_word, True)
    return (word, False)


def minimize_once_bruteforce_lazy(
    word: Word,
    morphism_list: Iterable[Morphism] | None = None,
    log: Log | None = None,
) -> tuple[Word, bool]:
    """
    Similar to :py:func:`minimize_once_bruteforce`, but lazy evaluated. This is almost always recommended.

    :param morphism_list: Passing a Morphism List has no effect.
    """
    has_log: bool = log is not None
    for morphism in generate_t2_wh_aut_lazy(word.infer_free_group()):
        new_word = morphism(word)
        if new_word.length < word.length:
            if has_log:
                log.append(LogItem(new_word, morphism))
            return (new_word, True)
    return (word, False)


def minimize_bruteforce(
    word: Word,
    lazy: bool = True,
    morphism_list: Iterable[Morphism] | None = None,
    /,
    log: Log | None = None,
) -> Word:
    """
    Returns the minimized form of the word, which might be the same word.

    :param lazy: (Recommended) Enables lazy evaluation of the automorphisms. If this is on, passing a ``morphism_list`` has no effect.
    :param morphism_list: If an iterable of morphisms is not provided, :py:func:`generate_all_t2_whitehead_automorphisms` is used to generate all possible Whitehead automorphisms for the given word. It is recommended that the list is generated and passed manually if working with multiple words from the same free group.
    :param log: *(keyword argument only)* All mimization operations are appended to the log, if passed.

    >>> log = new_log()
    >>> minimize_bruteforce(rd("a b^2 c"), log=log)
    c
    >>> display_log(log)
    abc : SortedDict({'a': ab⁻¹})
    bc : SortedDict({'b': a⁻¹b})
    c : SortedDict({'c': b⁻¹c})

    """
    if morphism_list is None and not lazy:
        morphism_list = generate_all_t2_whitehead_automorphisms(word.infer_free_group())
    new_word = word
    minimize_function = (
        minimize_once_bruteforce_lazy if lazy else minimize_once_bruteforce
    )
    while True:
        new_word, reduced_in_cycle = minimize_function(new_word, morphism_list, log=log)
        if not reduced_in_cycle:
            break
    return new_word
