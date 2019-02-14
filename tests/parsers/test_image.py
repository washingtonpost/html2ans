import pytest
from html2ans.parsers.image import AbstractImageParser, ImageParser


def test_basic_image(make_tag):
    tag = make_tag('<img src="smiley.gif" alt="Smiley face" height="42" width="42">', 'img')
    parsed = AbstractImageParser().construct_output(tag)
    assert 'smiley.gif' == parsed.get('url')
    assert 'image' == parsed.get('type')
    assert 42 == parsed.get('height')
    assert 42 == parsed.get('width')


def test_percent_height_image(make_tag):
    tag = make_tag('<img src="smiley.gif" alt="Smiley face" height="42%" width="42">', 'img')
    parsed = AbstractImageParser().construct_output(tag)
    assert not parsed.get('height')


def test_percent_width_image(make_tag):
    tag = make_tag('<img src="smiley.gif" alt="Smiley face" height="42" width="42%">', 'img')
    parsed = AbstractImageParser().construct_output(tag)
    assert not parsed.get('width')


def test_image_missing_src(make_tag):
    tag = make_tag('<img alt="Smiley face" height="42%" width="42">', 'img')
    parsed_result = ImageParser().parse(tag)
    assert parsed_result.output is None
    assert parsed_result.match is True
