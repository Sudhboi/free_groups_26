from src.free_groups_26 import *

def test_conversion():
    w = word_from_str("a^2 b^3")
    assert w == Word((Letter("a", 2), Letter("b", 3)), FreeGroup(("b", "a")))

def test_reduction():
    w = word_from_str("a^3 b^-2 b^2 a^-2 c^0")
    assert w.reduced() == word_from_str("a")
