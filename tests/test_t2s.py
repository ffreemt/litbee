"""Test t2s."""
from litbee.t2s import t2s


def test_t2s1():
    """Test trivial t2s."""
    assert t2s(["", ""]) == ["", ""]
    assert t2s(["a\nb", ""]) == ["a\nb", ""]
    assert t2s(["a\n\nb\n", ""]) == ["a\n\nb\n", ""]


def test_t2s2():
    """Test t2s."""
    assert t2s(["需攜帶", "需攜帶"]) == ["需携带", "需携带"]
    assert t2s(["需攜帶\n\n需攜帶\n", "需携带\n"]) == ["需携带\n\n需携带\n", "需携带\n"]
