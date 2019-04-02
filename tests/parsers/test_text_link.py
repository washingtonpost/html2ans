import pytest
from html2ans.parsers.text import InterstitialLinkParser

parser = InterstitialLinkParser()


@pytest.mark.parametrize('tag_string', [
    '<a />',
    '<a href="">Google</a>',
    '<a href="google.com"></a>'
])
def test_empty_link(tag_string, make_tag):
    tag = make_tag(tag_string, 'a')
    result = parser.parse(tag)
    assert result.match
    assert not result.output


def test_is_applicable(make_tag):
    assert parser.is_applicable(make_tag('<a></a>', 'a'))


def test_basic_link(make_tag):
    tag = make_tag('<a href="google.com">Google</a>', 'a')
    result = parser.parse(tag)
    assert result.match
    assert result.output.get('url') == "google.com"
    assert result.output.get("content") == "Google"
    assert result.output.get("type") == "interstitial_link"
