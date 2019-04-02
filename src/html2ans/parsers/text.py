from __future__ import absolute_import, unicode_literals  # need this for python 2.7 unicode issues

import six
from bs4.element import NavigableString, Tag
from ftfy import fix_text

from html2ans.parsers.base import BaseElementParser, ParseResult


class AbstractTextParser(BaseElementParser):
    """
    Abstract parser for text-only elements (``NavigableString``, ``p``, etc.).
    """

    def construct_output(self, element, *args, **kwargs):
        if isinstance(element, NavigableString) or isinstance(element, six.text_type):
            content = six.text_type(element).strip()
        elif element.name in self.INLINE_TAGS:
            content = str(element)
        else:
            # There doesn't seem to be a great way to extract the text
            # without eliminating text formatters
            # like <strong>, thus the strange join statement
            content = fix_text(''.join([six.text_type(x) for x in element.contents]).strip())
        if content:
            return super(AbstractTextParser, self).construct_output(element, "text", content)
        return None


class ParagraphParser(AbstractTextParser):
    """
    Paragraph parser. This parser does not remove text-formatting
    tags like ``em``, ``b``, ``i``, etc. OR inline links. What is
    or isn't removed by this parser can be adjusted by updating the
    ``TEXT_TAGS`` field which is inherited from
    ``html2ans.parsers.utils.AbstractParserUtilities``. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/text.json>`_

    Example:

    .. code-block:: html

        <p>Post Reports is the daily podcast from <a href="https://www.washingtonpost.com">The Washington Post</a></p>

    ->

    .. code-block:: python

        {
            "type": "text",
            "content": "Post Reports is the daily podcast from <a href=\"https://www.washingtonpost.com\">The Washington Post</a>"
        }

    """
    applicable_elements = ['p', NavigableString]

    def parse(self, element, *args, **kwargs):
        result = None
        match = False
        if self.is_text_only(element):
            match = True
            content = self.construct_output(element)
            if isinstance(content, list) or (isinstance(content, dict) and content.get("content")):
                result = content
        return ParseResult(result, match)


class FormattedTextParser(AbstractTextParser):
    """
    Formatted text parser. This parser does not remove text-formatting
    tags like ``em``, ``b``, ``i``, etc. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/text.json>`_

    Example:

    .. code-block:: html

        <em>Post Reports</em>

    ->

    .. code-block:: python

        {
            "type": "text",
            "content": "<em>Post Reports</em>"
        }

    """

    applicable_elements = [
        'b',
        'del',
        'em',
        'i',
        'ins',
        'mark',
        'small',
        'strong',
        'sub',
        'sup',
        'u']

    def parse(self, element, *args, **kwargs):
        result = None
        match = False
        if self.is_text_only(element):
            match = True
            result = self.construct_output(element)
        return ParseResult(result, match)


class BlockquoteParser(AbstractTextParser):
    """
    Blockquote parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/quote.json>`_

    Example:

    .. code-block:: html

        <blockquote>
            <p>Post Reports is the daily podcast from The Washington Post.</p>
            <p>Unparalleled reporting.</p>
            <p>Expert insight.</p>
            <p>Clear analysis.</p>
        </blockquote>

    ->

    .. code-block:: python

        {
            "type": "quote",
            "content_elements": [
                {
                    "type": "text",
                    "content": "Post Reports is the daily podcast from The Washington Post."
                },
                {
                    "type": "text",
                    "content": "Unparalleled reporting."
                },
                {
                    "type": "text",
                    "content": "Expert insight."
                },
                {
                    "type": "text",
                    "content": "Clear analysis."
                }
            ]
        }

    """
    applicable_elements = ['blockquote']

    def parse(self, element, *args, **kwargs):
        result = None
        match = False
        content_elements = []
        if self.is_text_only(element):
            match = True
            p_elements = element.find_all('p')
            if p_elements:
                for p_element in p_elements:
                    # don't want to process oembed (twitter, inselementram, etc) as blockquotes,
                    # so only consider text
                    # technically since v0.6.0 we could put in the oembeds but shouldn't by default
                    if not self.is_empty(p_element):
                        p_result = ParagraphParser().parse(p_element)
                        if p_result.match and p_result.output:
                            content_elements.append(p_result.output)
            else:
                p_result = ParagraphParser().parse(element)
                if p_result.match:
                    content_elements.append(p_result.output)
        if match:
            result = {
                "type": "quote",
                "content_elements": content_elements
            }
        return ParseResult(result, match)


class HeaderParser(BaseElementParser):
    """
    Header parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/header.json>`_

    Example:

    .. code-block:: html

        <h1>Post Reports</h1>

    ->

    .. code-block:: python

        {
            "type": "header",
            "level": 1,
            "content": "Post Reports"
        }

    """

    applicable_elements = ["h1", "h2", "h3", "h4", "h5", "h6"]

    def parse(self, element, *args, **kwargs):
        result = None
        content = element.text
        if content:
            result = self.construct_output(element, "header", content)
            result["level"] = int(element.name[1:len(element.name)])
        return ParseResult(result, True)


class InterstitialLinkParser(BaseElementParser):
    """
    Converts links in anchor elements into
    ANS elements of type ``interstitial_link``. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/interstitial_link.json>`_

    Example:

    .. code-block:: html

        <a href="https://www.washingtonpost.com">The Washington Post</a>

    ->

    .. code-block:: python

        {
            "type": "interstitial_link",
            "url": "https://www.washingtonpost.com",
            "content": "The Washington Post"
        }

    """
    applicable_elements = ['a']

    def parse(self, element, *args, **kwargs):
        result = self.construct_output(element, "interstitial_link", element.text)
        match = True
        url = element.attrs.get('href')
        result["url"] = url
        content = result.get("content")
        if not (url and content):
            result = None
            match = True
        return ParseResult(result, match)


class ListItemParser(ParagraphParser):
    """
    Parses a single list item tag as paragraph text
    ANS elements of type ``text``. As of ANS 0.6.2, list items have
    to be either text or another list (in the case of another list,
    the ``ListParser`` is used recursively). `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/list_element.json>`_

    Example:

    .. code-block:: html

        <li>
            Post Reports,
            <a href="/podcast/">a daily podcast</a>
            from The Washington Post.
        </li>

    ->

    .. code-block:: python

        {
            "type": "text",
            "content": "Post Reports, <a href="/podcast/">a daily podcast</a> from The Washington Post."
        }

    """
    applicable_elements = ["li"]

    def __init__(self):
        self.TEXT_TAGS.append("li")


class ListParser(BaseElementParser):
    """
    List parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/list.json>`_

    Example:

    .. code-block:: html

        <ul>
            <li>
                Post Reports,
                <a href="/podcast/">a daily podcast</a>
                from The Washington Post.
            </li>
            <li>
                <ol>
                    <li>Unparalleled reporting.</li>
                    <li>Expert insight.</li>
                </ol>
            <li><p>Clear analysis.</p></li>
        </ul>

    ->

    .. code-block:: python

        {
            'type': 'list',
            'list_type': 'unordered',
            'items': [
                {
                    'type': 'text',
                    'content': 'Post Reports, <a href="/podcast/">a daily podcast</a> from The Washington Post.'
                },
                {
                    'type': 'list',
                    'list_type': 'ordered',
                    'items': [
                        {
                            'type': 'text',
                            'content': 'Unparalleled reporting.'
                        },
                        {
                            'type': 'text',
                            'content': 'Expert insight.'
                        }
                    ]
                },
                {
                    'type': 'text',
                    'content': '<p>Clear analysis.</p>'
                }
            ]
        }

    :param list_item_parser: the parser to use on individual list elements (defaults to ``ListItemParser``)
    :type list_item_parser: ElementParser

    """
    applicable_elements = ['ul', 'ol']

    def __init__(self, list_item_parser=None):
        self.list_item_parser = list_item_parser if list_item_parser else ListItemParser()

    def parse(self, element, *args, **kwargs):
        list_elements = []

        def _add_list_element(parsed_list_item, check_field):

            if isinstance(parsed_list_item, dict) and parsed_list_item.get(check_field):
                list_elements.append(parsed_list_item)

        if element.name == 'ul':
            list_type = 'unordered'
        else:
            list_type = 'ordered'

        for list_item in element.contents:
            if isinstance(list_item, Tag) and list_item.contents:
                child_lists = list_item.find_all(self.applicable_elements)

                if child_lists:

                    for child in child_lists:
                        _add_list_element(self.parse(child).output, "items")

                else:

                    if self.list_item_parser.is_applicable(list_item):
                        _add_list_element(self.list_item_parser.parse(list_item).output, "content")

        result = self.construct_output(element, "list")
        result["list_type"] = list_type
        result["items"] = list_elements
        return ParseResult(result, True)


# Backwards compatibility
LinkParser = InterstitialLinkParser
