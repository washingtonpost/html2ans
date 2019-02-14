from html2ans.parsers.raw_html import RawHtmlParser

parser = RawHtmlParser()


def test_wrapped_content(make_div_tag):
    tag = make_div_tag('<div>Headline<h6>title</h6><p>paragraph</p></div>')
    parsed = parser.parse(tag)
    assert parsed[0].get('content') == '<div>Headline<h6>title</h6><p>paragraph</p></div>'
    assert parsed[0].get('type') == 'raw_html'


def test_unwrapped_content(make_div_tag):
    tag = make_div_tag('<div>Headline<h6>title</h6>paragraph</div>')
    parsed = parser.parse(tag)
    assert parsed[0].get('content') == '<div>Headline<h6>title</h6>paragraph</div>'
    assert parsed[0].get('type') == 'raw_html'
