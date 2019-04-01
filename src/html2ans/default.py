from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser
from html2ans.parsers.text import (
    InterstitialLinkParser,
    BlockquoteParser,
    FormattedTextParser,
    HeaderParser,
    ListParser,
    ParagraphParser,
)
from html2ans.parsers.image import (
    FigureParser,
    LinkedImageParser,
    ImageParser,
)
from html2ans.parsers.embeds import (
    ArcPlayerEmbedParser,
    DailyMotionEmbedParser,
    FacebookPostEmbedParser,
    FacebookVideoEmbedParser,
    FlickrEmbedParser,
    IFrameParser,
    ImgurEmbedParser,
    InstagramEmbedParser,
    PollDaddyEmbedParser,
    RedditEmbedParser,
    SpotifyEmbedParser,
    TumblrEmbedParser,
    TwitterTweetEmbedParser,
    TwitterVideoEmbedParser,
    VimeoEmbedParser,
    VineEmbedParser,
    YoutubeEmbedParser,
)
from html2ans.parsers.audio import AudioParser
from html2ans.parsers.raw_html import RawHtmlParser


class DefaultHtmlAnsParser(BaseHtmlAnsParser):
    """
    The default root/top-level parser class.

    """

    DEFAULT_PARSERS = [
        # embed parsers
        ArcPlayerEmbedParser(),  # div
        DailyMotionEmbedParser(),  # iframe
        FacebookPostEmbedParser(),  # iframe (with embed inside)
        FacebookVideoEmbedParser(),  # iframe (with embed inside)
        FlickrEmbedParser(),  # a (with image inside)
        ImgurEmbedParser(),  # blockquote (with embed inside)
        InstagramEmbedParser(),  # blockquote (with embed inside)
        PollDaddyEmbedParser(),  # noscript
        RedditEmbedParser(),  # blockquote (with embed inside)
        SpotifyEmbedParser(),  # iframe (with embed inside)
        TumblrEmbedParser(),  # div
        TwitterTweetEmbedParser(),  # blockquote (with embed inside)
        TwitterVideoEmbedParser(),  # blockquote (with embed inside)
        YoutubeEmbedParser(),  # iframe (with embed inside)
        VimeoEmbedParser(),  # iframe (with embed inside)
        VineEmbedParser(),  # iframe (with embed inside)

        # text parsers
        HeaderParser(),  # h1-h6
        ListParser(),  # ul/ol
        FormattedTextParser(),  # strong, em, etc.
        BlockquoteParser(),  # blockquote
        ParagraphParser(),  # NavigableString, p

        # image/figure parsers
        LinkedImageParser(),  # a
        ImageParser(),  # img
        FigureParser(),  # figure

        InterstitialLinkParser(),  # a

        AudioParser(),  # audio

        IFrameParser(),  # generic iframe

        NullParser(),  # comments
    ]
    """
    Default parsers for the default implementation. These will be added to
    the `BaseHtmlAnsParser` ``parsers`` attribute in the order listed, so
    order matters!
    """

    BACKUP_PARSERS = [
        IFrameParser(),
        RawHtmlParser()
    ]
    """
    Backup parsers for the default implementation. These will be tried in
    the order listed, so order matters!
    """

    def __init__(self, *args, **kwargs):
        super(DefaultHtmlAnsParser, self).__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)


# kind of for backwards compatibility
# but more for being succint
Html2Ans = DefaultHtmlAnsParser
