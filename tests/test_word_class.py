from free_groups_26.letter import letter_from_str
from free_groups_26.word import Word

lfs = letter_from_str


def test_creation_and_display():
    assert str(Word([lfs("A"), lfs("A"), lfs("b")])) == "AAb"
    assert str(Word((lfs("A"), lfs("A"), lfs("b")))) == "AAb"
    assert str(Word((lfs("a^-4"), lfs("A"), lfs("b")))) == "AAAAAb"
    assert repr(Word((lfs("a^-4"), lfs("A"), lfs("b")))) == "a^-5 b"
    assert str(Word([lfs("A"), lfs("A"), lfs("b"), lfs("B")])) == "AA"
    assert repr(Word([lfs("A"), lfs("A"), lfs("b"), lfs("B")])) == "a^-2"
