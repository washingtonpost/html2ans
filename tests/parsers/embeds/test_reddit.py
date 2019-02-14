# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import RedditEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<blockquote class="reddit-card" data-card-created="1549834040">'
     '<a href="https://www.reddit.com/r/programming/comments/6l689j/'
     'a_manually_curated_list_of_240_popular/">A manually curated list '
     'of 240+ popular programming podcast episodes</a> from '
     '<a href="http://www.reddit.com/r/programming">r/programming</a>'
     '</blockquote><script async src="//embed.redditmedia.com/widgets'
     '/platform.js" charset="UTF-8"></script>',
     "https://www.reddit.com/r/programming/comments/6l689j/a_manually_curated_list_of_240_popular/")
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "blockquote")
        result, match = RedditEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "reddit"
        assert result["referent"]["provider"] == RedditEmbedParser.provider
        assert result["referent"]["service"] == "oembed"
