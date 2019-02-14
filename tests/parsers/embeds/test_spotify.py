# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import SpotifyEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe src="https://open.spotify.com/user/112389858/playlist/4E55G0GYK0CuUWZ0IQiaoD">'
     '</iframe>',
     "https://open.spotify.com/user/112389858/playlist/4E55G0GYK0CuUWZ0IQiaoD"),
    ('<iframe src="https://open.spotify.com/track/0bYg9bo50gSsH3LtXe2SQn"></iframe>',
     "https://open.spotify.com/track/0bYg9bo50gSsH3LtXe2SQn"),
    ('<iframe src="https://open.spotify.com/track/1JfHgbMH8cEB9HVqSA3Xby"></iframe>',
     "https://open.spotify.com/track/1JfHgbMH8cEB9HVqSA3Xby"),
    ('<iframe src="https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"></iframe>',
     "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"),
    ('<iframe src="https://open.spotify.com/track/3HUlnkkeg0zaDWarGpARah"></iframe>',
     "https://open.spotify.com/track/3HUlnkkeg0zaDWarGpARah"),
    ('<iframe src="https://open.spotify.com/episode/5hfRHXfPU7M5EgpKQH9NQS"></iframe>',
     "https://open.spotify.com/episode/5hfRHXfPU7M5EgpKQH9NQS"),
    ('<iframe src="https://open.spotify.com/playlist/37i9dQZF1DWXLeA8Omikj7"></iframe>',
     "https://open.spotify.com/playlist/37i9dQZF1DWXLeA8Omikj7")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = SpotifyEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "spotify"
        assert result["referent"]["provider"] == SpotifyEmbedParser.provider
