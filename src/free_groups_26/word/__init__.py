"""
This module defines the Word Class and functions on words.
"""

from .defn import Word
from .functions import (
    generate_random_word,
    word_from_str_a,
    word_from_str_b,
    word_from_str,
    read,
)

__all__ = [
    "Word",
    "generate_random_word",
    "word_from_str_a",
    "word_from_str_b",
    "word_from_str",
    "read",
]
