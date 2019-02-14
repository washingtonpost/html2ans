# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import YoutubeEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe src="https://www.youtube.com/embed/7IBERQ9abkk?feature=oembed"></iframe>',
     "https://www.youtube.com/watch?v=7IBERQ9abkk"),
    ('<iframe src=\"http://www.youtube.com/embed/gZnNmCf2Zok\"></iframe>',
     "https://www.youtube.com/watch?v=gZnNmCf2Zok"),
    ('<iframe src=\"http://www.youtube.com/embed/OVK-tGUZy9A?rel=0\"></iframe>',
     "https://www.youtube.com/watch?v=OVK-tGUZy9A"),
    ('<iframe src="https://www.youtube.com/embed/3TqLNkLdpGY"></iframe>',
     "https://www.youtube.com/watch?v=3TqLNkLdpGY"),
    ('<iframe src="https://www.youtube.com/embed/4I86iz4X4jM"></iframe>',
     "https://www.youtube.com/watch?v=4I86iz4X4jM")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = YoutubeEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "youtube"
        assert result["referent"]["provider"] == YoutubeEmbedParser.provider
