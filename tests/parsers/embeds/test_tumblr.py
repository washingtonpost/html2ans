# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import TumblrEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/xu6zPm7j0A8sEf03xcnR9w/101895859192"'
     ' data-did="1332a9c3948cd691a2db1da3e68a58fbbf20e709">'
     '<a href="https://unwrapping.tumblr.com/post/101895859192/tumblr-sweatshirt-merch">'
     'https://unwrapping.tumblr.com/post/101895859192/tumblr-sweatshirt-merch</a></div>',
     "https://unwrapping.tumblr.com/post/101895859192"),
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/Wbp15Kb-pFzI_72xjPdxzg/180346104805"'
     ' data-did="d29c58387b823a602d72949f81783548c5fe732d">'
     '<a href="https://cartoonpolitics.tumblr.com/post/180346104805/'
     'story-here-cartoon-by-matt-wuerker">'
     'https://cartoonpolitics.tumblr.com/post/180346104805/story-here-cartoon-by-matt-wuerker'
     '</a></div>',
     "https://cartoonpolitics.tumblr.com/post/180346104805"),
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/AmZ4bK_DeMjgveszNO_mjQ/180342217797"'
     ' data-did="da39a3ee5e6b4b0d3255bfef95601890afd80709">'
     '<a href="http://bled.tumblr.com/post/180342217797">'
     'http://bled.tumblr.com/post/180342217797</a></div>',
     "https://bled.tumblr.com/post/180342217797"),
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/vY3dYyu03_ZK8zKR3Ukiiw/180352219168"'
     ' data-did="e3e682a6f281e89038308b810e95b75ddbe6b78f">'
     '<a href="https://abookhaven.tumblr.com/post/180352219168/'
     'the-best-part-of-being-home-cats-and-books-and">'
     'https://abookhaven.tumblr.com/post/180352219168/'
     'the-best-part-of-being-home-cats-and-books-and</a></div>',
     "https://abookhaven.tumblr.com/post/180352219168"),
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/67gzjB87rG0-5qSuAaoBxA/180352280783"'
     ' data-did="a57f8b609347877835580bb80b3d7d8566419e40">'
     '<a href="https://herepet.tumblr.com/post/180352280783/'
     'source-instagramcom-mydogiscutest-i-pwomise-i">'
     'https://herepet.tumblr.com/post/180352280783/'
     'source-instagramcom-mydogiscutest-i-pwomise-i</a></div>',
     "https://herepet.tumblr.com/post/180352280783"),
    ('<div class="tumblr-post"'
     ' data-href="https://embed.tumblr.com/embed/post/Rw6A9YUevF3zQ2f_RIFS5w/180351911516"'
     ' data-did="ef6d50fd9a8cc93fd93bf801d898e60d2900db24">'
     '<a href="https://totallydoglife.tumblr.com/post/180351911516/'
     'my-buddy-luke-always-loves-a-nap-after-the-park">'
     'https://totallydoglife.tumblr.com/post/180351911516/'
     'my-buddy-luke-always-loves-a-nap-after-the-park</a></div>',
     "https://totallydoglife.tumblr.com/post/180351911516")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "div")
        result, match = TumblrEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "tumblr"
        assert result["referent"]["provider"] == TumblrEmbedParser.provider
