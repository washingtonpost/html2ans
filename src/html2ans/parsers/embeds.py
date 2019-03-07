import re
from six.moves.urllib_parse import urlparse, unquote
from bs4.element import Tag

from html2ans.parsers.base import BaseElementParser, ParseResult
from html2ans.parsers.raw_html import RawHtmlParser
from html2ans.parsers.utils import parse_dimensions


class AbstractEmbedParser(BaseElementParser):
    """
    Abstract class for embed parsing.

    `Reference ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/utils/reference.json>`_

    `Oembed response ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/utils/oembed_response.json>`_
    """

    applicable_elements = ['blockquote']
    non_oembed_service_types = ['video']
    regex = ''
    """
    A regex that can be used to find the embed's ID
    """

    tag = None
    """
    The tag the embed URL will appear in
    """

    attr = None
    """
    The attribute the embed URL will appear in
    """

    embed_type = None
    """
    The embed type (for populating ``referent.type``)
    """

    provider = ''
    """
    A URL from the embed can be accessed from (given the embed's ID)
    """

    def get_tag_id(self, tag):
        tag_id = None
        tag_attr = tag.get(self.attr)
        if tag_attr:
            if self.regex:
                match = re.search(self.regex, tag_attr)
                if match:
                    tag_id = match.group(1)
            else:
                tag_id = tag_attr
        return tag_id

    def _remove_embed_script(self, element):
        next_tag = element.next_sibling
        while next_tag and self.is_empty(next_tag):
            next_tag = next_tag.next_sibling
        if isinstance(next_tag, Tag):
            if next_tag.name == "script":
                next_tag.decompose()
            else:
                self._remove_all_scripts(next_tag)
        else:
            self._remove_all_scripts(element)

    def _remove_all_scripts(self, element):
        for tag in element.find_all('script'):
            tag.decompose()

    def parse(self, element, *args, **kwargs):
        result = None
        match = False
        tag_id = self.get_tag_id(element)
        if not tag_id:
            sub_tags = element.find_all(self.tag)
            for sub_tag in sub_tags:
                sub_id = self.get_tag_id(sub_tag)
                if sub_id:
                    tag_id = sub_id
                    break
        if tag_id:
            match = True
            result = self.construct_output(element, "reference")
            result["referent"] = {
                "provider": self.provider,
                "type": self.embed_type,
                "id": unquote(tag_id).replace("http://", "https://")
            }
            if self.embed_type not in self.non_oembed_service_types:
                result['referent']['service'] = 'oembed'
        # many embeds come with a script that should be removed
        self._remove_embed_script(element)
        return ParseResult(result, match)


class DailyMotionEmbedParser(AbstractEmbedParser):
    """
    DailyMotion video parser.

    Example:

    .. code-block:: html

        <iframe src="https://www.dailymotion.com/embed/video/x2p99yn"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "x2p99yn",
                "type": "dailymotion",
                "provider": "https://www.dailymotion.com/services/oembed?id=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['iframe']
    regex = r'https?://www.dailymotion.com/embed/video/(.+)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'dailymotion'
    provider = 'https://www.dailymotion.com/services/oembed?id='


class FlickrEmbedParser(AbstractEmbedParser):
    """
    Flickr embed parser.

    Example:

    .. code-block:: html

        <a data-flickr-embed="true" href="https://www.flickr.com/photos/16177003@N03/8240338083/in/photolist-dyaTqx" title="Fox">
            <img src="https://farm9.staticflickr.com/8066/8240338083_938cc14c6f_k.jpg" width="2048" height="1272" alt="Fox">
        </a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.flickr.com/photos/16177003@N03/8240338083/in/photolist-dyaTqx",
                "type": "flickr",
                "provider": "https://www.flickr.com/services/oembed.json/?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['a']
    regex = r'(https?://www.flickr.com/photos/.+)'
    tag = 'a'
    attr = 'href'
    embed_type = 'flickr'
    provider = "https://www.flickr.com/services/oembed.json/?url="


class RedditEmbedParser(AbstractEmbedParser):
    """
    Reddit embed parser.

    Example:

    .. code-block:: html

        <blockquote class="reddit-card" data-card-created="1549834040">
            <a href="https://www.reddit.com/r/programming/comments/6l689j/a_manually_curated_list_of_240_popular/">
                A manually curated list of 240+ popular programming podcast episodes
            </a> from <a href="http://www.reddit.com/r/programming">r/programming</a>
        </blockquote>
        <script async src="//embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.reddit.com/r/programming/comments/6l689j/a_manually_curated_list_of_240_popular/",
                "type": "reddit",
                "provider": "https://www.reddit.com/oembed?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['blockquote']
    applicable_classes = ['reddit-card']
    tag = 'a'
    attr = 'href'
    embed_type = 'reddit'
    provider = "https://www.reddit.com/oembed?url="


class PollDaddyEmbedParser(AbstractEmbedParser):
    """
    PollDaddy embed parser.

    Example:

    .. code-block:: html

        <noscript>
            <b>Click here to see this poll: <a href="https://poll.fm/6514633">https://poll.fm/6514633</a></b>
        </noscript>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://poll.fm/6514633",
                "type": "polldaddy",
                "provider": "https://polldaddy.com/oembed/?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['noscript']
    regex = r'(https?://poll.fm/(\d+))'
    tag = 'a'
    attr = 'href'
    embed_type = 'polldaddy'
    provider = "https://polldaddy.com/oembed/?url="


class TwitterTweetEmbedParser(AbstractEmbedParser):
    """
    Twitter post parser.

    Example:

    .. code-block:: html

        <blockquote class="twitter-tweet" data-lang="en">
            <p lang="en" dir="ltr">
                Displaced by Woolsey fire, Malibu families gather for a meal and hugs:
                <a href="https://t.co/W3ZWJIKOjG">https://t.co/W3ZWJIKOjG</a>
                <a href="https://t.co/FUouJS6xwl">pic.twitter.com/FUouJS6xwl</a>
            </p>
            Los Angeles Times (@latimes)
            <a href="https://twitter.com/latimes/status/1065323995959037953?ref_src=twsrc%5Etfw">November 21, 2018</a>
        </blockquote>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": 1065323995959037953,
                "type": "twitter",
                "provider": "https://api.twitter.com/1.1/statuses/oembed.json?id=",
                "service": "oembed"
            },
            "additional_properties": {
                "class": "twitter-tweet",
                "data-lang": "en"
            }
        }

    """

    applicable_classes = ['twitter-tweet']
    regex = r'https?://twitter.com/\w+/status/(\d+)'
    tag = 'a'
    attr = 'href'
    embed_type = 'twitter'
    provider = 'https://api.twitter.com/1.1/statuses/oembed.json?id='


class TwitterVideoEmbedParser(TwitterTweetEmbedParser):
    """
    Twitter video parser.

    Example:

    .. code-block:: html

        <blockquote class="twitter-video" data-lang="de">
            <p lang="de" dir="ltr">
                Am Sonntag wird in Hannover gefeiert!

                <a href="https://twitter.com/hashtag/Einschulung?src=hash&amp;ref_src=twsrc%5Etfw">
                    #Einschulung
                </a>
                <a href="https://twitter.com/hashtag/HAZfest?src=hash&amp;ref_src=twsrc%5Etfw">
                    #HAZfest
                </a>
                <a href="https://twitter.com/hashtag/AktionSichererSchulweg?src=hash&amp;ref_src=twsrc%5Etfw">
                    #AktionSichererSchulweg
                </a>
                <a href="https://t.co/8q7hHjy1zK">
                    pic.twitter.com/8q7hHjy1zK
                </a>
            </p>
            &mdash; HAZ (@HAZ)
            <a href="https://twitter.com/HAZ/status/1027958659404521475?ref_src=twsrc%5Etfw">August 10, 2018</a>
        </blockquote>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": 1027958659404521475,
                "type": "twitter",
                "provider": "https://api.twitter.com/1.1/statuses/oembed.json?id=",
                "service": "oembed"
            },
            "additional_properties": {
                "class": "twitter-video",
                "data-lang": "de"
            }
        }

    """

    applicable_classes = ['twitter-video']


class InstagramEmbedParser(AbstractEmbedParser):
    """
    Instagram embed parser.

    Example:

    .. code-block:: html

        <blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading" data-instgrm-version="12">
            <div>
                <a href="https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading" target="_blank">
                    Removed stuff
                </a>
                <p>
                    <a href="https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading" target="_blank">
                        A post shared by CNN (@cnn)
                    </a> on <time datetime="2018-11-18T01:00:10+00:00">Nov 17, 2018 at 5:00pm PST</time>
                </p>
            </div>
        </blockquote>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.instagram.com/p/BqTW3VBDl2c/?utm_source=ig_embed&amp;utm_medium=loading",
                "type": "instagram",
                "provider": "https://api.instagram.com/oembed?url=",
                "service": "oembed"
            },
            "additional_properties": {
                "class": "instagram-media"
            }
        }

    """
    applicable_classes = ['instagram-media']
    regex = r'(https?://www.instagram.com/[\w-]+/[\w-]+/)'
    tag = 'a'
    attr = 'href'
    embed_type = 'instagram'
    provider = 'https://api.instagram.com/oembed?url='


class VineEmbedParser(AbstractEmbedParser):
    """
    Vine embed parser.

    Example:

    .. code-block:: html

        <iframe class="vine-embed" src="https://vine.co/v/imPIVvJ6E5j/embed/simple"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "imPIVvJ6E5j",
                "type": "vine",
                "provider": "https://vine.co/oembed.json?url=",
                "service": "oembed"
            },
            "additional_properties": {
                "class": "vine-embed"
            }
        }

    """
    applicable_elements = ['iframe']
    applicable_classes = ['vine-embed']
    regex = r'(https?://vine.co/v(/[\w?=]+)+)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'vine'
    provider = 'https://vine.co/oembed.json?url='


class ArcPlayerEmbedParser(AbstractEmbedParser):
    applicable_elements = ['div']
    applicable_classes = ['arc-player']
    tag = 'div'
    attr = 'data-uuid'
    embed_type = 'video'


class FacebookPostEmbedParser(AbstractEmbedParser):
    """
    Facebook post embed parser.

    Example:

    .. code-block:: html

        <iframe src="https://www.facebook.com/plugins/post.php?href=https://www.facebook.com/zuck/posts/10102883338403521&width=500"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.facebook.com/zuck/posts/10102883338403521&width=500",
                "type": "facebook-post",
                "provider": "https://www.facebook.com/plugins/post/oembed.json/?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['iframe']
    regex = r'https?://www.facebook.com/plugins/post\.php\?href=(.*)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'facebook-post'
    provider = 'https://www.facebook.com/plugins/post/oembed.json/?url='


class FacebookVideoEmbedParser(FacebookPostEmbedParser):
    """
    Facebook video embed parser.

    Example:

    .. code-block:: html

        <iframe src="https://www.facebook.com/plugins/video.php?href=https://www.facebook.com/chicagotribune/videos/351670322074116/&show_text=0&width=560"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.facebook.com/chicagotribune/videos/351670322074116/&show_text=0&width=560",
                "type": "facebook-video",
                "provider": "https://www.facebook.com/plugins/video/oembed.json/?url=",
                "service": "oembed"
            }
        }

    """
    regex = r'https?://www.facebook.com/plugins/video\.php\?href=(.*)'
    provider = 'https://www.facebook.com/plugins/video/oembed.json/?url='
    embed_type = 'facebook-video'


class YoutubeEmbedParser(AbstractEmbedParser):
    """
    Youtube video embed parser.

    Example:

    .. code-block:: html

        <iframe src="https://www.youtube.com/embed/4I86iz4X4jM"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://www.youtube.com/embed/4I86iz4X4jM",
                "type": "youtube",
                "provider": "https://www.youtube.com/oembed?format=json&url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['iframe']
    regex = r'(https?://www.youtube.com/embed/[\w-]+)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'youtube'
    provider = 'https://www.youtube.com/oembed?format=json&url='

    def parse(self, element, *args, **kwargs):
        parsed_result = super(YoutubeEmbedParser, self).parse(element)
        if parsed_result.output:
            path = urlparse(parsed_result.output.get("referent").get("id")).path
            tag_id = 'https://www.youtube.com/watch?v={}'.format(path.replace('/embed/', ''))
            parsed_result.output["referent"]["id"] = tag_id
        return parsed_result


class VimeoEmbedParser(AbstractEmbedParser):
    """
    Vimeo video embed parser.

    Example:

    .. code-block:: html

        <iframe src="https://player.vimeo.com/video/76979871"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://player.vimeo.com/video/76979871",
                "type": "vimeo",
                "provider": "https://vimeo.com/api/oembed.json?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['iframe']
    regex = r'(https?://player.vimeo.com/video/\w+)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'vimeo'
    provider = 'https://vimeo.com/api/oembed.json?url='


class TumblrEmbedParser(AbstractEmbedParser):
    """
    Vimeo video embed parser.

    Example:

    .. code-block:: html

        <div class="tumblr-post" data-href="https://embed.tumblr.com/embed/post/67gzjB87rG0-5qSuAaoBxA/180352280783" data-did="a57f8b609347877835580bb80b3d7d8566419e40">'
            <a href="https://herepet.tumblr.com/post/180352280783/source-instagramcom-mydogiscutest-i-pwomise-i">
                https://herepet.tumblr.com/post/180352280783/source-instagramcom-mydogiscutest-i-pwomise-i
            </a>
        </div>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://herepet.tumblr.com/post/180352280783/source-instagramcom-mydogiscutest-i-pwomise-i",
                "type": "tumblr",
                "provider": "https://www.tumblr.com/oembed/1.0?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['div']
    applicable_classes = ['tumblr-post']
    regex = r'(https?://\w+.tumblr.com/post/\d+)'
    tag = 'a'
    attr = 'href'
    embed_type = 'tumblr'
    provider = 'https://www.tumblr.com/oembed/1.0?url='


class SpotifyEmbedParser(AbstractEmbedParser):
    """
    Spotify embed parser.

    Example:

    .. code-block:: html

        <iframe src="https://open.spotify.com/user/112389858/playlist/4E55G0GYK0CuUWZ0IQiaoD"></iframe>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://open.spotify.com/user/112389858/playlist/4E55G0GYK0CuUWZ0IQiaoD",
                "type": "spotify",
                "provider": "https://embed.spotify.com/oembed/?url=",
                "service": "oembed"
            }
        }

    """
    applicable_elements = ['iframe']
    regex = r'(https?://\w+.spotify.com/.*)'
    tag = 'iframe'
    attr = 'src'
    embed_type = 'spotify'
    provider = 'https://embed.spotify.com/oembed/?url='


class ImgurEmbedParser(AbstractEmbedParser):
    """
    Imgur embed parser.

    Example:

    .. code-block:: html

        <blockquote class="imgur-embed-pub" lang="en" data-id="w7zCp">
            <a href="https://imgur.com/w7zCp">View post on imgur.com</a>
        </blockquote>

    ->

    .. code-block:: python

        {
            "type": "reference",
            "referent": {
                "id": "https://imgur.com/w7zCp",
                "type": "imgur",
                "provider": "https://api.imgur.com/oembed/?url=",
                "service": "oembed"
            }
        }

    """
    applicable_classes = ['imgur-embed-pub']
    regex = r'(https?://imgur.com/.*)'
    tag = 'a'
    attr = 'href'
    embed_type = 'imgur'
    provider = 'https://api.imgur.com/oembed/?url='


class IFrameParser(RawHtmlParser):
    """
    Iframe parser.

    Example:

    .. code-block:: html

        <iframe src="http://www.test.com?var=value" height="315" scrolling="no"></iframe>

    ->

    .. code-block:: python

        {
            "type": "raw_html",
            "content": "<iframe src="http://www.test.com?var=value" height="315" scrolling="no"></iframe>",
            "additional_properties": {
                "height": 315
            }
        }

    """

    applicable_elements = ['iframe']

    def is_applicable(self, element, *args, **kwargs):
        return BaseElementParser.is_applicable(self, element) or element.find('iframe')

    def parse(self, element, *args, **kwargs):
        result = super(IFrameParser, self).parse(element).output
        if element.name == 'iframe':
            iframe_tag = element
        else:
            iframe_tag = element.find('iframe')
        add_props = result.get("additional_properties", {})
        if iframe_tag.attrs:
            add_props.update(iframe_tag.attrs)
        parse_dimensions(iframe_tag, add_props, ['height'])
        if add_props:
            result["additional_properties"] = add_props
        return ParseResult(result, True)
