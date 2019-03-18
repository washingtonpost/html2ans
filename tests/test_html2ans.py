# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(params=[
    '',
    '<div></div>',
    '<body></body>',
    '<body><!-- This is a comment --></body>',
    '\n<body><p></p></body>\n',
    '\n<body><p><script>Script stuff</script></p></body>\n',
    '<body><audio></audio></body'
])
def test_empty(body_html, test_html2ans):
    assert test_html2ans.generate_ans(body_html) == []


@pytest.mark.parametrize('test_html', [
    "<body><!-- test comment 1 --><div><!-- test comment 2 --></div></body>",
    "<body><div><p><!-- test comment 3 --></p></div></body>",
    "<body><!-- test comment 4 --></body>",
    '<body><div><p><!-- <a href="#test">test link</a> --></p></div></body>'
    '<body><p><!-- uuid: \"002051cc-8f7a-11e8-9774-c7a7ea8e16e4\"--></p></body>',
    "<body><!-- <div><p>Commented out</p></div> --></body>",
    "<!-- test comment 1 --><div><!-- test comment 2 --></div>",
    "<div><p><!-- test comment 3 --></p></div>",
    "<!-- test comment 4 -->",
    '<div><p><!-- <a href="#test">test link</a> --></p></div>'
    '<p><!-- uuid: \"002051cc-8f7a-11e8-9774-c7a7ea8e16e4\"--></p>',
    "<!-- <div><p>Commented out</p></div> -->"
])
def test_comments(test_html, test_html2ans):
    assert test_html2ans.generate_ans(test_html) == []


@pytest.mark.parametrize('test_html', [
    '<body>This is a navigable string</body>',
    'This is a navigable string',
])
def test_empty_except_navigable_string(test_html, test_html2ans):
    parsed = test_html2ans.generate_ans(test_html)
    assert len(parsed) == 1
    assert parsed[0].get('content') == 'This is a navigable string'


def test_non_p_text(test_html2ans):
    parsed = test_html2ans.generate_ans(
        '<body><em><strong>Related: <a href=\"http://www.google.com\">'
        'Google</a></strong></em></body>')
    assert parsed[0].get('content') == (
        '<em><strong>Related: '
        '<a href=\"http://www.google.com\">Google</a></strong></em>')
    assert parsed[0].get('type') == 'text'


def test_wrapped_image(test_html2ans):
    parsed = test_html2ans.generate_ans(
        '<body><p><img height=\"150\" src=\"https://s3.amazonaws.com/'
        'Owen-Boyle-3x2-150x150.jpg\" width=\"150\"/>  </p></body>')
    assert parsed[0].get('type') == 'image'


def test_linked_image(test_html2ans):
    parsed = test_html2ans.generate_ans(
        '<body><p><a href="somelink"><img height=\"80\" '
        'src=\"imgsrc\" width=\"40\"/></a></p></body>')
    assert parsed[0].get('type') == 'image'
    assert parsed[0].get('url') == 'imgsrc'
    assert parsed[0].get('width') == 40
    assert parsed[0].get('height') == 80
    assert parsed[0].get('additional_properties').get('image_link') == "somelink"


def test_nested_paragraphs(test_html2ans):
    parsed = test_html2ans.generate_ans('<p><p>Text</p><p>Text</p><p>Text</p></p>')
    assert parsed == [
        {
            "type": "text",
            "content": "Text"
        },
        {
            "type": "text",
            "content": "Text"
        },
        {
            "type": "text",
            "content": "Text"
        }
    ]


def test_script(test_html2ans):
    html = (
        '<body><!--{{{--><script minified="true">var meterExcludeFlag '
        '= "false";</script><!--}}}--></body>')
    parsed = test_html2ans.generate_ans(html)
    assert parsed[0].get('type') == 'raw_html'
    assert parsed[0].get('additional_properties').get('minified') == 'true'
    assert parsed[0].get(
        'content') == '<script minified="true">var meterExcludeFlag = "false";</script>'


@pytest.mark.parametrize('html', [
    ('<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Crazy turbulence '
     'and injuries, but the <a href="https://twitter.com/Delta?ref_src=twsrc%5Etfw">'
     '@delta</a> crew handled it perfectly, even the emergency landing. '
     '<a href="https://t.co/NoJWLp5GUv">pic.twitter.com/NoJWLp5GUv</a></p>&mdash; '
     'joe justice (@JoeJustice0) <a href="https://twitter.com/JoeJustice0/status/'
     '1095792526609371136?ref_src=twsrc%5Etfw">February 13, 2019</a></blockquote> '
     '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'),
    ('<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Crazy turbulence '
     'and injuries, but the <a href="https://twitter.com/Delta?ref_src=twsrc%5Etfw">'
     '@delta</a> crew handled it perfectly, even the emergency landing. '
     '<a href="https://t.co/NoJWLp5GUv">pic.twitter.com/NoJWLp5GUv</a></p>&mdash; '
     'joe justice (@JoeJustice0) <a href="https://twitter.com/JoeJustice0/status/'
     '1095792526609371136?ref_src=twsrc%5Etfw">February 13, 2019</a></blockquote> '
     '<div><script async src="https://platform.twitter.com/widgets.js" charset="utf-8">'
     '</div></script>')
])
def test_embed_parser_script_removal(html, test_html2ans):
    parsed = test_html2ans.generate_ans(html)
    assert len(parsed) == 1
    assert parsed[0].get('referent').get('type') == "twitter"
