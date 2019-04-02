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
                    'content': '<p>level two item</p>',
                    'type': 'text'
                }
            ],
            'list_type': 'unordered',
            'type': 'list'
        },
        {
            'content': '<p>level one item</p>',
            'type': 'text'
        }
    ]


def test_complex_list(make_tag):
    tag = make_tag('<ul><li>Post Reports, '
                   '<a href="/podcast/">a daily podcast</a> '
                   'from The Washington Post.</li>'
                   '<li><ol><li>Unparalleled reporting.</li>'
                   '<li>Expert insight.</li></ol>'
                   '<li>Clear analysis.</li></ul>', 'ul')
    parsed = parser.parse(tag).output
    assert parsed.get('type') == 'list'
    assert parsed.get('list_type') == 'unordered'
    list_items = parsed.get("items")
    assert len(list_items) == 3
    assert list_items[0].get("type") == "text"
    assert list_items[0].get("content") == 'Post Reports, ' \
                                           '<a href="/podcast/">a daily podcast</a> ' \
                                           'from The Washington Post.'
    assert list_items[1].get("type") == "list"
    assert list_items[1].get("list_type") == "ordered"
    assert len(list_items[1].get("items")) == 2
    assert list_items[1].get("items")[0].get("type") == "text"
    assert list_items[2].get("type") == "text"


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
