# coding: utf-8

"""Tests for ogre.exceptions"""

from __future__ import absolute_import

import ogre.exceptions


def test_ogreerror__str__():
    """Test the __str__ method of OGReError."""
    assert isinstance(str(ogre.exceptions.OGReError()), str)
