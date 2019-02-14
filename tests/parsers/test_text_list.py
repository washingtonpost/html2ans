import pytest
from html2ans.parsers.text import ListParser

parser = ListParser()


@pytest.fixture(params=[
    '<ol></ol>',
    '<ul></ul>',
])
def valid_list_tag(request):
    return request.param


def test_empty(make_tag):
    tag = make_tag('<ol></ol>', 'ol')
    assert not parser.parse(tag).output.get('items')
    tag = make_tag('<ul></ul>', 'ul')
    assert not parser.parse(tag).output.get('items')


def test_is_applicable(valid_list_tag, make_tag):
    tag = make_tag('<ol></ol>', 'ol')
    assert parser.is_applicable(tag)
    tag = make_tag('<ul></ul>', 'ul')
    assert parser.is_applicable(tag)


def test_nested_list(make_tag):
    tag = make_tag(
        '<ol><li><ul><li><p>level two item</p></li></ul></li><li><p>level one item</p></li></ol>',
        'ol')
    parsed = parser.parse(tag).output
    assert parsed.get('type') == 'list'
    assert parsed.get('list_type') == 'ordered'
    assert parsed.get('items') == [
        {
            'items': [
                {
                    'content': 'level two item',
                    'type': 'text'
                }
            ],
            'list_type': 'unordered',
            'type': 'list'
        },
        {
            'content': 'level one item',
            'type': 'text'
        }
    ]


def test_link_in_list(make_tag):
    tag = make_tag('<ul><li><a href="http://www.rcinet.ca">Canada article</a></li></ul>', 'ul')
    parsed = parser.parse(tag).output
    assert parsed.get('type') == 'list'
    assert parsed.get('list_type') == 'unordered'
    assert parsed.get('items') == [
        {
            'type': 'text',
            'content': 'Canada article',
            'additional_properties': {
                'href': "http://www.rcinet.ca"
            }
        }
    ]


def test_basic_list(make_tag):
    tag = make_tag(
        '<ol><li>Item one</li><li>Item two</li></a></li></ol>', 'ol')
    parsed = parser.parse(tag).output
    assert parsed.get('type') == 'list'
    assert parsed.get('list_type') == 'ordered'
    assert parsed.get('items') == [
        {
            'type': 'text',
            'content': 'Item one'
        },
        {
            'type': 'text',
            'content': 'Item two'
        }
    ]


def test_empty_list(make_tag):
    tag = make_tag(
        '<ol><li></li><li></li></ol>', 'ol')
    parsed = parser.parse(tag).output
    assert parsed.get('type') == 'list'
    assert parsed.get('list_type') == 'ordered'
    assert parsed.get('items') == []
