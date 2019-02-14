import six
from html2ans.parsers.base import BaseElementParser, ParseResult


class RawHtmlParser(BaseElementParser):
    """
    Raw HTML parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/raw_html.json>`_

    Example:

    .. code-block:: html

        <iframe src="https://app.stitcher.com/splayer/f/335403/58653169" width="220" height="150"></iframe>

    ->

    .. code-block:: python

        {
            "type": "raw_html",
            "content": "<iframe src="https://app.stitcher.com/splayer/f/335403/58653169" width="220" height="150"></iframe>"
        }

    """

    def is_applicable(self, element, *args, **kwargs):
        return True

    def parse(self, element, *args, **kwargs):
        return ParseResult(self.construct_output(element, "raw_html", six.text_type(element)), True)
