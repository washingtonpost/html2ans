# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import InstagramEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<blockquote class="instagram-media" data-instgrm-version="7">'
     '<div><p><a href="https://www.instagram.com/p/BFfIlFNxTYF/" target="_blank">'
     'A photo posted by Kylo Ren (@kylotheoutlawdog)</a> on '
     '<time datetime="2016-05-16T23:24:38+00:00">May 16, 2016 at 4:24pm PDT</time>'
     '</p></div></blockquote>',
     "https://www.instagram.com/p/BFfIlFNxTYF/"),
    ('<blockquote class="instagram-media" data-instgrm-permalink='
     '"https://www.instagram.com/p/BqaTp5yhzod/?utm_source=ig_embed&amp;utm_medium=loading"'
     ' data-instgrm-version="12"><div><a href="https://www.instagram.com/p/BqaTp5yhzod/'
     '?utm_source=ig_embed&amp;utm_medium=loading" target="_blank">Removed stuff</a><p>'
     '<a href="https://www.instagram.com/p/BqaTp5yhzod/?utm_source=ig_embed&amp;utm_medium=loading"'
     ' target="_blank">A post shared by CNN (@cnn)</a> on '
     '<time datetime="2018-11-20T18:04:28+00:00">Nov 20, 2018 at 10:04am PST</time>'
     '</p></div></blockquote>',
     "https://www.instagram.com/p/BqaTp5yhzod/"),
    ('<blockquote class="instagram-media" data-instgrm-permalink='
     '"https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading"'
     ' data-instgrm-version="12"><div><a href="https://www.instagram.com/p/BqTW3VBDl2c/?'
     'utm_source=ig_embed&amp;utm_medium=loading" target="_blank">Removed stuff</a><p>'
     '<a href="https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading"'
     ' target="_blank">A post shared by CNN (@cnn)</a> on '
     '<time datetime="2018-11-18T01:00:10+00:00">Nov 17, 2018 at 5:00pm PST</time>'
     '</p></div></blockquote>',
     "https://www.instagram.com/p/BqTW3VBDl2c/")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "blockquote")
        result, match = InstagramEmbedParser().parse(embed_tag)
        assert match is True
        assert result["referent"]["id"] == expected_id
        assert result["type"] == "reference"
        assert result["referent"]["type"] == "instagram"
        assert result["referent"]["provider"] == InstagramEmbedParser.provider
