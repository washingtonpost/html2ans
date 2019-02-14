# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import FlickrEmbedParser


@pytest.mark.parametrize('tag_string,expected_id', [
    ('<a data-flickr-embed="true" href="https://www.flickr.com/photos/'
     '16177003@N03/8240338083/in/photolist-dyaTqx" title="Fox">'
     '<img src="https://farm9.staticflickr.com/8066/8240338083_938cc14c6f_k.jpg"'
     ' width="2048" height="1272" alt="Fox"></a>'
     '<script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
     'https://www.flickr.com/photos/'
     '16177003@N03/8240338083/in/photolist-dyaTqx')
])
def test_embed_parser(tag_string, expected_id, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "a")
        result, match = FlickrEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "flickr"
        assert result["referent"]["provider"] == FlickrEmbedParser.provider
