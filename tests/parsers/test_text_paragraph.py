# -*- coding: utf-8 -*-

import pytest
from bs4 import NavigableString

from html2ans.parsers.text import ParagraphParser


@pytest.fixture
def parser():
    return ParagraphParser()


def test_empty(parser, make_p_tag):
    tag = make_p_tag('<p></p>')
    parsed_result = parser.parse(tag)
    assert parsed_result.output is None
    assert parsed_result.match


def test_string(parser):
    tag = NavigableString('My lovely text')
    parsed_result = parser.parse(tag)
    assert parsed_result.output.get('content') == 'My lovely text'


def test_special_formatting(parser, make_p_tag):
    tag = make_p_tag(
        '<p>I <strong>strongly</strong> feel that '
        '<i>italics</i> are the <ins>best</ins> format.</p>')
    parsed_result = parser.parse(tag)
    assert parsed_result.output.get('content') == (
        'I <strong>strongly</strong>'
        ' feel that <i>italics</i> are the <ins>best</ins> format.')


def test_wrapped_special_formatting(parser, make_p_tag):
    tag = make_p_tag(
        "<p><em><strong>Related: "
        "<a href=\"http://www.wweek.com/culture/2016/06/28/"
        "im-a-californian-and-im-here-to-stay/\" target=\"_blank\">"
        "I'm a Californian, and I'm Here to Stay</a></strong></em></p>")
    parsed_result = parser.parse(tag)
    assert parsed_result.output.get('content') == (
        "<em><strong>Related: "
        "<a href=\"http://www.wweek.com/culture/2016/06/28/"
        "im-a-californian-and-im-here-to-stay/\" target=\"_blank\">"
        "I'm a Californian, and I'm Here to Stay</a></strong></em>")
    assert parsed_result.output.get('type') == 'text'


def test_link_in_text(parser, make_p_tag):
    parsed_result = parser.parse(make_p_tag(
        '<p>Look at <a href="google.com">this</a> '
        'amazing page! And <a href="google.com">this</a> one too!</p>'))
    assert parsed_result.output.get('content') == (
        'Look at <a href="google.com">this</a> amazing page!'
        ' And <a href="google.com">this</a> one too!')
    assert parsed_result.output.get('type') == 'text'


def test_mdash(parser, make_p_tag):
    assert u'—' in parser.parse(make_p_tag('<p>&mdash;</p>')).output.get('content')


def test_single_quote(parser, make_p_tag):
    assert "'" in parser.parse(make_p_tag('<p>quote&rsquo;</p>')).output.get('content')


def test_double_quote(parser, make_p_tag):
    assert '"' in parser.parse(make_p_tag('<p>&ldquo; &rdquo;</p>')).output.get('content')
