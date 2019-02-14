import pytest
from html2ans.parsers.image import LinkedImageParser


@pytest.fixture
def parser():
    return LinkedImageParser()


@pytest.fixture
def valid_wrapped_tag():
    return '<a><img src=imgsrc width=40 height=80 /></a>'


def test_empty(parser, make_tag):
    tag = make_tag('<a></a>', 'a')
    assert (None, False) == parser.parse(tag)


def test_is_applicable(parser, valid_wrapped_tag, make_tag):
    assert parser.is_applicable(make_tag(valid_wrapped_tag, 'a'))
    tag = make_tag('<a></a>', 'a')
    assert not parser.is_applicable(tag)


def test_wrapped_image(parser, valid_wrapped_tag, make_tag):
    tag = make_tag(valid_wrapped_tag, 'a')
    parsed = parser.parse(tag)[0]
    assert parsed.get('type') == 'image'
    assert parsed.get('url') == 'imgsrc'
    assert parsed.get('width') == 40
    assert parsed.get('height') == 80


def test_wrapped_image_with_link(parser, valid_wrapped_tag, make_tag):
    tag = make_tag(valid_wrapped_tag, 'a')
    tag.attrs['href'] = "somelink"
    parsed = parser.parse(tag)[0]
    assert parsed.get('type') == 'image'
    assert parsed.get('url') == 'imgsrc'
    assert parsed.get('width') == 40
    assert parsed.get('height') == 80
    assert parsed.get('additional_properties').get('image_link') == "somelink"
