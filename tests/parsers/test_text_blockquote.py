import pytest
from bs4 import NavigableString

from html2ans.parsers.text import BlockquoteParser


@pytest.fixture
def parser():
    return BlockquoteParser()


@pytest.fixture(params=[
    '<blockquote></blockquote>',
])
def valid_quote_tag(request):
    return request.param


def test_is_applicable(parser, valid_quote_tag, make_tag):
    assert parser.is_applicable(make_tag(valid_quote_tag, 'blockquote'))


@pytest.mark.parametrize('html', [
    '<blockquote><p>This is a blockquote.</p></blockquote>',
    '<blockquote class="something"><p>This is a blockquote.</p></blockquote>',
    '<blockquote>This is a blockquote.</blockquote>'
])
def test_blockquote_with_p(html, parser, make_tag):
    tag = make_tag(html, 'blockquote')
    parsed = parser.parse(tag).output
    assert parsed.get('content_elements')[0]["content"] == 'This is a blockquote.'


def test_blockquote_with_multi_p(parser, make_tag):
    tag = make_tag('<blockquote><p>This is a blockquote.</p><p>And then some.</p></blockquote>', 'blockquote')
    parsed = parser.parse(tag).output
    assert parsed.get('content_elements')[0]["content"] == 'This is a blockquote.'
    assert parsed.get('content_elements')[1]["content"] == 'And then some.'


def test_blockquote_with_multi_p_empty(parser, make_tag):
    tag = make_tag('<blockquote><p>This is a blockquote.</p><p>And then some.</p><p></p></blockquote>', 'blockquote')
    parsed = parser.parse(tag).output
    assert len(parsed["content_elements"]) == 2


def test_blockquote_with_multi_p_and_image(parser, make_tag):
    tag = make_tag('<blockquote><p>This is a blockquote.</p><img src="google.com"/></blockquote>', 'blockquote')
    parsed_result = parser.parse(tag)
    assert parsed_result.output is None
    assert not parsed_result.match
