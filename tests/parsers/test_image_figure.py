import pytest
from html2ans.parsers.image import FigureParser

parser = FigureParser()


@pytest.fixture(params=[
    '<figure></figure>',
])
def valid_figure_tag(request):
    return request.param


def test_empty(make_tag):
    tag = make_tag('<figure />', 'figure')
    assert (None, True) == parser.parse(tag)


def test_is_applicable(valid_figure_tag, make_tag):
    assert parser.is_applicable(make_tag(valid_figure_tag, 'figure'))


def test_figure(make_tag):
    tag = make_tag(
        '<figure><img src=imgsrc width=80 height=40></img><figcaption>'
        'My marvelous caption</figcaption></figure>', 'figure')
    parsed = parser.parse(tag)[0]
    assert parsed.get('url') == 'imgsrc'
    assert parsed.get('width') == 80
    assert parsed.get('height') == 40
    assert parsed.get('caption') == 'My marvelous caption'
    assert parsed.get('type') == 'image'
