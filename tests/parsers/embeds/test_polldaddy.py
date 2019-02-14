# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import PollDaddyEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<noscript><b>Click here to see this poll: '
     '<a href="https://poll.fm/6514633">https://poll.fm/6514633</a></b>'
     '</noscript>',
     "https://poll.fm/6514633")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "noscript")
        result, match = PollDaddyEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "polldaddy"
        assert result["referent"]["provider"] == PollDaddyEmbedParser.provider
        assert result["referent"]["service"] == "oembed"
