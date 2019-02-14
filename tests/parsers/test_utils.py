import pytest
from html2ans.parsers.utils import AbstractParserUtilities


@pytest.mark.parametrize('tag_string,tag_name,num_children', [
    ('<p></p>', 'p', 0),
    ('<p><a href="somelink">Hello</a></p>', 'p', 1),
    ('<p><img src="imgsrc"/><img src="imgsrc"/></p>', 'p', 2),
])
def test_get_children(tag_string, tag_name, num_children, make_tag):
    assert len(AbstractParserUtilities.get_children(make_tag(tag_string, tag_name))) == num_children


@pytest.mark.parametrize('tag_string,tag_name,filters,num_children', [
    ('<p><a href="somelink">Hello</a></p>', 'p', ('a', ), 0),
    ('<p><img src="imgsrc"/><img src="imgsrc"/></p>', 'p', ('img', ), 0)
])
def test_get_children_with_filters(tag_string, tag_name, filters, num_children, make_tag):
    tag = make_tag(tag_string, tag_name)
    assert len(AbstractParserUtilities.get_children(tag, filters)) == num_children


@pytest.mark.parametrize('tag_string,tag_name', [
    ('<p><a href="somelink"><img height="80" src="imgsrc" width="40"/></a></p>', 'p'),
    ('<img height="80" src="imgsrc" width="40"/>', 'img'),
])
def test_is_text_only_false(tag_string, tag_name, make_tag):
    assert not AbstractParserUtilities.is_text_only(make_tag(tag_string, tag_name))


@pytest.mark.parametrize('tag_string,tag_name', [
    ('<p><a href="somelink">Hello</a></p>', 'p'),
    ('<p>Some text</p>', 'p'),
    ('Some text', None),
    ('Some <span>text</span>', None),
    (None, None),
    ('<p>I <strong>strongly</strong> feel that <i>italics</i> are the <ins>best</ins> format.</p>', 'p'),
    ('<p><p>Text</p><p>Text</p><p>Text</p></p>', 'p')
])
def test_is_text_only_true(tag_string, tag_name, make_tag):
    assert AbstractParserUtilities.is_text_only(make_tag(tag_string, tag_name))


@pytest.mark.parametrize('tag_string,tag_name', [
    ('<p><a href="somelink">Hello</a></p>', 'p'),
    ('<p>Some text</p>', 'p'),
    ('<div><img src="imgsrc"/></div>', 'div'),
    ('<p><img src="imgsrc"/><img src="imgsrc"/></p>', 'p'),
    ('<p><p>Text</p><p>Text</p><p>Text</p></p>', 'p')
])
def test_is_wrapper_true(tag_string, tag_name, make_tag):
    assert AbstractParserUtilities.is_wrapper(make_tag(tag_string, tag_name))


@pytest.mark.parametrize('tag_string,tag_name', [
    ('<img src="imgsrc"/>', 'img'),
    ('<div width="500"><img src="imgsrc"/></div>', 'div'),
    ("<p>I've got <i>something</i> to say</p>", 'p'),
])
def test_is_wrapper_false(tag_string, tag_name, make_tag):
    assert not AbstractParserUtilities.is_wrapper(make_tag(tag_string, tag_name))


@pytest.mark.parametrize('tag_string,tag_name', [
    ('<br>', 'br'),
    ('\n', None),
    ('', None)
])
def test_is_empty_true(tag_string, tag_name, make_tag):
    assert AbstractParserUtilities.is_empty(make_tag(tag_string, tag_name))
