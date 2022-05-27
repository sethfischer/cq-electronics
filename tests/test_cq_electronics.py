"""CadQuery Electronics tests."""

from cq_electronics import __version__


def test_version():
    """Test version string."""
    assert __version__ == "0.1.0"
