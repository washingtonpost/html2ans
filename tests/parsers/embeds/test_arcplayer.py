# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import ArcPlayerEmbedParser


@pytest.mark.parametrize('tag_string,tag_type,expected_id', [
    ('<div class="arc-player" data-org="washingtonpost" '
     'data-uuid="cc09466e-7982-4dca-a56e-8d1155f68361" '
     'id="arc-player-cc09466e-7982-4dca-a56e-8d1155f68361"></div>',
     'div',
     "cc09466e-7982-4dca-a56e-8d1155f68361"),
    ('<p class="arc-player" data-org="washingtonpost" '
     'data-uuid="ff4cf9b3-5d3c-4ebb-87f5-df8056790270" '
     'id="arc-player-ff4cf9b3-5d3c-4ebb-87f5-df8056790270"></p>',
     'p',
     "ff4cf9b3-5d3c-4ebb-87f5-df8056790270"),
    ('<section class="arc-player" data-org="washingtonpost" '
     'data-uuid="7248840b-57c8-436f-ad8b-291f5d3fc9e6" '
     'id="arc-player-7248840b-57c8-436f-ad8b-291f5d3fc9e6"></section>',
     'section',
     "7248840b-57c8-436f-ad8b-291f5d3fc9e6"),
    ('<article class="arc-player" data-org="washingtonpost" '
     'data-uuid="7248840b-57c8-436f-ad8b-291f5d3fc9e6" '
     'id="arc-player-7248840b-57c8-436f-ad8b-291f5d3fc9e6"></article>',
     'article',
     "7248840b-57c8-436f-ad8b-291f5d3fc9e6"),
    ('<blockquote class="arc-player" data-org="washingtonpost" '
     'data-uuid="7248840b-57c8-436f-ad8b-291f5d3fc9e6" '
     'id="arc-player-7248840b-57c8-436f-ad8b-291f5d3fc9e6"></blockquote>',
     'blockquote',
     "7248840b-57c8-436f-ad8b-291f5d3fc9e6"),
    ('<span class="arc-player" data-org="washingtonpost" '
     'data-uuid="7248840b-57c8-436f-ad8b-291f5d3fc9e6" '
     'id="arc-player-7248840b-57c8-436f-ad8b-291f5d3fc9e6"></span>',
     'span',
     "7248840b-57c8-436f-ad8b-291f5d3fc9e6"),
])
def test_embed_parser(tag_string, tag_type, expected_id, make_tag):
    """Test arc player class parsing"""
    embed_tag = make_tag(tag_string, tag_type)
    result, match = ArcPlayerEmbedParser().parse(embed_tag)
    assert match is True
    assert result["type"] == "reference"
    assert result["referent"]["id"] == expected_id
    assert result["referent"]["type"] == "video"
    assert result["referent"]["provider"] == ""
