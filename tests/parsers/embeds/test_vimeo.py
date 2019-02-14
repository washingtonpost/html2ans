# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import VimeoEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe src="https://player.vimeo.com/video/76979871"></iframe>',
     "https://player.vimeo.com/video/76979871"),
    ('<iframe src="https://player.vimeo.com/video/256978777"></iframe>',
     "https://player.vimeo.com/video/256978777"),
    ('<iframe src="http://player.vimeo.com/video/74420814"></iframe>',
     "https://player.vimeo.com/video/74420814"),
    ('<iframe src="https://player.vimeo.com/video/289502328"></iframe>',
     "https://player.vimeo.com/video/289502328"),
    ('<iframe src="https://player.vimeo.com/video/301951994"></iframe>',
     "https://player.vimeo.com/video/301951994"),
    ('<iframe src="https://player.vimeo.com/video/204029471?title=0&byline=0&portrait=0"></iframe>',
     "https://player.vimeo.com/video/204029471")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = VimeoEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "vimeo"
        assert result["referent"]["provider"] == VimeoEmbedParser.provider
