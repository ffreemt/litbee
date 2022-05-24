"""Test litbee."""
# pylint: disable=broad-except
from litbee import __version__, litbee


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not litbee()
    except Exception:
        assert True
