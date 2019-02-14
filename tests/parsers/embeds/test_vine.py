# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import VineEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe class="vine-embed" src="https://vine.co/v/'
     'M6gbIOedZ5X/embed/postcard?audio=1"></iframe>',
     "https://vine.co/v/M6gbIOedZ5X/embed/postcard?audio=1"),
    ('<iframe class="vine-embed" src="http://vine.co/v/'
     'bgLaVYdjWZH/embed/postcard?audio=1"></iframe>',
     "https://vine.co/v/bgLaVYdjWZH/embed/postcard?audio=1"),
    ('<iframe class="vine-embed" src="http://vine.co/v/'
     'bgLaVYdjWZH/embed/simple"></iframe>',
     "https://vine.co/v/bgLaVYdjWZH/embed/simple"),
    ('<iframe src="https://vine.co/v/imPIVvJ6E5j/embed/simple"></iframe>',
     "https://vine.co/v/imPIVvJ6E5j/embed/simple")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = VineEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "vine"
        assert result["referent"]["provider"] == VineEmbedParser.provider
