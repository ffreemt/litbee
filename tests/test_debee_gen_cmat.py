"""Test debee."""
# pylint: disable=broad-except
from debee.gen_cmat import gen_cmat
from debee.loadparas import loadparas


def test_gen_cmat():
    """Test gen_cmat."""
    text1 = loadparas("data/sternstunden04-de.txt")
    text2 = loadparas("data/sternstunden04-en.txt")
    assert len(text1) >= 29
    assert len(text2) >= 30

    cmat = gen_cmat(text1, text2)
    cmat0 = gen_cmat(text1, text2, remove_punctuation=False)

    len_21 = (len(text2), len(text1))
    assert cmat.shape == len_21

    assert cmat.sum() > 59
    assert cmat0.sum() > 59.1
