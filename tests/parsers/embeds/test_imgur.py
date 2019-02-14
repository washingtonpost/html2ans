# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import ImgurEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<blockquote class="imgur-embed-pub" lang="en" data-id="w7zCp">'
     '<a href="https://imgur.com/w7zCp">View post on imgur.com</a></blockquote>',
     "https://imgur.com/w7zCp"),
    ('<blockquote class="imgur-embed-pub" lang="en" data-id="a/6EDKIHH">'
     '<a href="https://imgur.com/6EDKIHH">Bedtime story</a></blockquote>'
     '<script async src="//s.imgur.com/min/embed.js"></script>',
     "https://imgur.com/6EDKIHH"),
    ('<blockquote class="imgur-embed-pub" lang="en" data-id="a/PZp6FQm">'
     '<a href="http://imgur.com/PZp6FQm">We all got our own thing.</a></blockquote>',
     "https://imgur.com/PZp6FQm")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "blockquote")
        result, match = ImgurEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "imgur"
        assert result["referent"]["provider"] == ImgurEmbedParser.provider
