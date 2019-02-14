# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import (
    FacebookPostEmbedParser,
    FacebookVideoEmbedParser,
)


@pytest.mark.parametrize('html,expected_id', [
    ('<iframe src="https://www.facebook.com/plugins/post.php?'
     'href=https%3A%2F%2Fwww.facebook.com%2Fzuck%2Fposts%2F10102883338403521&width=500"></iframe>',
     "https://www.facebook.com/zuck/posts/10102883338403521&width=500"),
    ('<iframe src="http://www.facebook.com/plugins/post.php?'
     'href=http%3A%2F%2Fwww.facebook.com%2Fzuck%2Fposts%2F10102883338403521"></iframe>',
     "https://www.facebook.com/zuck/posts/10102883338403521"),
    ('<iframe src="https://www.facebook.com/plugins/post.php?href='
     'https%3A%2F%2Fwww.facebook.com%2Fcnn%2Fposts%2F10158959666571509&width=500"></iframe>',
     "https://www.facebook.com/cnn/posts/10158959666571509&width=500"),
    ('<iframe src="https://www.facebook.com/plugins/post.php?href='
     'https%3A%2F%2Fwww.facebook.com%2FJournalistenausbildungMadsackMedienCampus'
     '%2Fposts%2F744546942555057&width=500"></iframe>',
     "https://www.facebook.com/JournalistenausbildungMadsackMedienCampus"
     "/posts/744546942555057&width=500"),
    ('<iframe src="https://www.facebook.com/plugins/post.php?href='
     'https%3A%2F%2Fwww.facebook.com%2Fleparisien%2Fposts%2F10157295731929063&width=500"></iframe>',
     "https://www.facebook.com/leparisien/posts/10157295731929063&width=500"),
    ('<iframe src="https://www.facebook.com/plugins/post.php?href='
     'https%3A%2F%2Fwww.facebook.com%2Fmexicopuntocom%2Fposts'
     '%2F764461417236549&width=500"></iframe>',
     "https://www.facebook.com/mexicopuntocom/posts/764461417236549&width=500")
])
def test_post_embed_parser(html, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(html, "iframe")
        result, match = FacebookPostEmbedParser().parse(embed_tag)
        assert match is True
        assert result["referent"]["id"] == expected_id
        assert result["type"] == "reference"
        assert result["referent"]["type"] == "facebook-post"
        assert result["referent"]["provider"] == FacebookPostEmbedParser.provider


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com'
     '%2FCircusSirenPod%2Fvideos%2F2184715485183578%2F&show_text=0&width=476"></iframe>',
     "https://www.facebook.com/CircusSirenPod/videos/2184715485183578/&show_text=0&width=476"),
    ('<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com'
     '%2Fchicagotribune%2Fvideos%2F351670322074116%2F&show_text=0&width=560"></iframe>',
     "https://www.facebook.com/chicagotribune/videos/351670322074116/&show_text=0&width=560"),
    ('<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com'
     '%2Flatimes%2Fvideos%2F249300315738761%2F&show_text=0&width=560"></iframe>',
     "https://www.facebook.com/latimes/videos/249300315738761/&show_text=0&width=560"),
    ('<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com'
     '%2Fwaposhorttakes%2Fvideos%2F1226054304199933%2F&show_text=0&width=560"></iframe>',
     "https://www.facebook.com/waposhorttakes/videos/1226054304199933/&show_text=0&width=560"),
    ('<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com'
     '%2Fwashingtonpost%2Fvideos%2F1131113343720055%2F&show_text=0&width=560"></iframe>',
     "https://www.facebook.com/washingtonpost/videos/1131113343720055/&show_text=0&width=560")
])
def test_video_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "iframe")
        result, match = FacebookVideoEmbedParser().parse(embed_tag)
        assert match is True
        assert result["referent"]["id"] == expected_id
        assert result["type"] == "reference"
        assert result["referent"]["type"] == "facebook-video"
        assert result["referent"]["provider"] == FacebookVideoEmbedParser.provider
