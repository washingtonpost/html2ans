from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser
from html2ans.parsers.text import (
    LinkParser,
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
    SpotifyEmbedParser,
    TumblrEmbedParser,
    TwitterTweetEmbedParser,
    TwitterVideoEmbedParser,
    VimeoEmbedParser,
    VineEmbedParser,
    YoutubeEmbedParser,
    FacebookPostEmbedParser,
    FacebookVideoEmbedParser,
    IFrameParser,
    ImgurEmbedParser,
    InstagramEmbedParser,
    ArcPlayerEmbedParser,
)
from html2ans.parsers.audio import AudioParser
from html2ans.parsers.raw_html import RawHtmlParser


class DefaultHtmlAnsParser(BaseHtmlAnsParser):
    """
    The default root/top-level parser class.

    """

    DEFAULT_PARSERS = [
        HeaderParser(),  # h1-h6
        ListParser(),  # ul/ol
        FormattedTextParser(),  # strong, em, etc.
        LinkedImageParser(),  # a
        LinkParser(),  # a
        ImageParser(),  # img
        ArcPlayerEmbedParser(),  # div
        TumblrEmbedParser(),  # div
        FigureParser(),  # figure
        AudioParser(),  # audio
        TwitterTweetEmbedParser(),  # blockquote (with embed inside)
        TwitterVideoEmbedParser(),  # blockquote (with embed inside)
        InstagramEmbedParser(),  # blockquote (with embed inside)
        ImgurEmbedParser(),  # blockquote (with embed inside)
        YoutubeEmbedParser(),  # iframe (with embed inside)
        FacebookPostEmbedParser(),  # iframe (with embed inside)
        FacebookVideoEmbedParser(),  # iframe (with embed inside)
        SpotifyEmbedParser(),  # iframe (with embed inside)
        VimeoEmbedParser(),  # iframe (with embed inside)
        VineEmbedParser(),  # iframe (with embed inside)
        BlockquoteParser(),  # blockquote
        ParagraphParser(),  # NavigableString, p
        IFrameParser(),  # iframe
        NullParser(),  # comments
    ]
    """
    Default parsers for the default implementation.
    """

    BACKUP_PARSERS = [
        IFrameParser(),
        RawHtmlParser()
    ]
    """
    Backup parsers for the default implementation.
    """

    def __init__(self, *args, **kwargs):
        super(DefaultHtmlAnsParser, self).__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)


# kind of for backwards compatibility
# but more for being succint
Html2Ans = DefaultHtmlAnsParser
