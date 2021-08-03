# coding: utf-8

"""Tests for ogre.cli"""

from __future__ import absolute_import

import random

import pytest

import ogre.cli


@pytest.fixture
def source():
    """Return a valid source."""
    return random.choice(["twitter"])


# pylint: disable=redefined-outer-name


def test___main__():
    """Test python -m functionality."""
    with pytest.raises(SystemExit) as excinfo:
        __import__("ogre.__main__")
    assert excinfo.value != 0


def test_empty():
    """Test invocation with no arguments."""
    with pytest.raises(SystemExit) as excinfo:
        ogre.cli.main()
    assert excinfo.value != 0


def test_no_credentials(source):
    """Test an invocation without API keys."""
    with pytest.raises(ValueError) as excinfo:
        ogre.cli.main(["-s", source])
    assert excinfo.value != 0


def test_invalid_keys(source):
    """Test an invocation with invalid API keys."""
    with pytest.raises(ValueError) as excinfo:
        ogre.cli.main(["-s", source, "--keys", "invalid"])
    assert excinfo.value != 0


def test_invalid_location(source):
    """Test an invocation with an invalid location."""
    with pytest.raises(ValueError) as excinfo:
        ogre.cli.main(["-s", source, "-l", "0", "0", "invalid", "km"])
    assert excinfo.value != 0


def test_invalid_interval(source):
    """Test an invocation with an invalid interval."""
    with pytest.raises(ValueError) as excinfo:
        ogre.cli.main(["-s", source, "-i", "0", "invalid"])
    assert excinfo.value != 0


def test_invalid_limit(source):
    """Test an invocation with an invalid limit."""
    with pytest.raises(ValueError) as excinfo:
        ogre.cli.main(["-s", source, "--limit", "invalid"])
    assert excinfo.value != 0


def test_invalid_log(source):
    """Test an invocation with an invalid log."""
    with pytest.raises(AttributeError) as excinfo:
        ogre.cli.main(["-s", source, "--log", "invalid"])
    assert excinfo.value != 0
