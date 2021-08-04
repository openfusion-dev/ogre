"""Tests for ogre.exceptions"""

import ogre.exceptions


def test_ogreerror__str__():
    """Test the __str__ method of OGReError."""
    assert isinstance(str(ogre.exceptions.OGReError()), str)
