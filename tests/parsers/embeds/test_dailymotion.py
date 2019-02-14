# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import DailyMotionEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe src="https://www.dailymotion.com/embed/video/x2p99yn"></iframe>',
     "x2p99yn"),
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = DailyMotionEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "dailymotion"
        assert result["referent"]["provider"] == DailyMotionEmbedParser.provider
