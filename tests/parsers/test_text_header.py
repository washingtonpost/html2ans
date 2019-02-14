import pytest

from html2ans.parsers.text import HeaderParser


@pytest.fixture
def parser():
    return HeaderParser()


def test_basic_header(parser, make_tag):
    parsed_result = parser.parse(make_tag('<h6>Here is a headline</h6>', 'h6'))
    assert parsed_result.output.get('content') == 'Here is a headline'
    assert parsed_result.output.get('type') == 'header'
    assert parsed_result.output.get('level') == 6


def test_empty_header(parser, make_tag):
    parsed_result = parser.parse(make_tag('<h6></h6>', 'h6'))
    assert parsed_result.output is None
    assert parsed_result.match is True
