import pytest
from free_groups_26.letter import Letter, letter_from_str


def test_from_str():
    assert letter_from_str("a") == Letter("a", 1)
    assert letter_from_str("A") == Letter("a", -1)
    with pytest.raises(ValueError):
        _ = letter_from_str("aa")
    assert letter_from_str("b^-32") == Letter("b", -32)


def test_equality_and_hash():
    assert Letter("a", 1) == Letter("a", 1)
    assert Letter("a", 1) != Letter("a", -1)
    assert hash(Letter("b", 23)) == hash(Letter("b", 23))
    assert hash(Letter("a", 1)) != hash(Letter("a", -1))


def test_ordering():
    assert Letter("a", 23) < Letter("c", 2)
    assert Letter("a", -1) > Letter("a", 2)
    assert Letter("a", -1) > Letter("a", -2)


def test_misc():
    assert Letter("a", -3).get_base() == Letter("a", -1)
    assert Letter("a", 3).get_base() == Letter("a", 1)
    assert Letter("a", 3).inv() == Letter("a", -3)
    assert Letter("a", -3).is_inverse()
    assert not Letter("a", 3).is_inverse()
