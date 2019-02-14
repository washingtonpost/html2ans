import pytest
from html2ans.parsers.base import BaseElementParser, ElementParser


def test_interface_is_applicable():
    with pytest.raises(NotImplementedError):
        ElementParser().is_applicable("fake")


def test_interface_parse():
    with pytest.raises(NotImplementedError):
        ElementParser().parse("fake")


def test_base_construct_output():
    assert BaseElementParser().construct_output(None, ans_type="image", version="0.6.2") == {
        "type": "image",
        "version": "0.6.2"
    }
