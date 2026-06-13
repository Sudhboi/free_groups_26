from typing import override

from free_groups_26.morphism import Morphism
from free_groups_26.word import Word

type Log = list[LogItem]


class LogItem:
    """
    Initializing this class manually is never recommended. Use :py:func:`new_log` to generate a :py:type:`Log` to pass where it is required.
    Manual access of the instance variables is encouraged, however.
    """

    word: Word
    """
    The current word in the log.
    """
    morphism: Morphism
    """
    The morphism that led to the current word.
    """

    def __init__(self, word: Word, morphism: Morphism) -> None:
        self.word = word
        self.morphism = morphism

    @override
    def __repr__(self) -> str:
        return str(self.word) + " : " + str(self.morphism.morphism_map)


def new_log() -> Log:
    """
    Generates a new :py:type:`Log`. Recommended over using ``[]`` for readability.
    """
    return []


def display_log(log: Log) -> None:
    """
    Prints out a :py:type:`Log` in a human readable fashion.
    """
    print("\n".join([str(log_item) for log_item in log]))
