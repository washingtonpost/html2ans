# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import IFrameParser


@pytest.mark.parametrize('html,tag_name', [
    (
        '<iframe src="http://www.test.com?var=value" height="315" scrolling="no"></iframe>',
        'iframe'
    ), (
        '<div><iframe src="http://www.test.com?var=value" height="315" scrolling="no">'
        '</iframe></div>',
        'div'
    ), (
        '<div height="500"><iframe src="http://www.test.com?var=value" height="315" scrolling="no">'
        '</iframe></div>',
        'div'
    )
])
def test_iframe_parser(html, tag_name, make_tag):
    embed_tag = make_tag(html, tag_name)
    result, match = IFrameParser().parse(embed_tag)
    assert match is True
    assert result["type"] == "raw_html"
    assert result["additional_properties"]["src"] == "http://www.test.com?var=value"
    assert result["additional_properties"]["height"] == 315
    assert result["additional_properties"]["scrolling"] == "no"


def test_iframe_bad_height(make_tag):
    tag = make_tag('<iframe src=iframesrc height=40px />', 'iframe')
    parsed = IFrameParser().parse(tag).output
    assert parsed.get('content') == '<iframe height="40px" src="iframesrc"></iframe>'


def test_iframe_bad_width(make_tag):
    iframe_html = (
        '<iframe height="500" src="https://scores.test.com/torneos/page.html"'
        ' width="100%"></iframe>')
    tag = make_tag(iframe_html, 'iframe')
    parsed = IFrameParser().parse(tag).output
    assert parsed.get("type") == "raw_html"
    assert parsed.get("content") == iframe_html
    assert parsed.get('additional_properties').get('height') == 500
    assert parsed.get('additional_properties').get('width') == '100%'
