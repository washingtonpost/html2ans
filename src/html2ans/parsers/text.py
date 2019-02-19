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
            if isinstance(result, dict):
                result["content"] = "<{}>{}</{}>".format(
                    element.name,
                    result.get("content"), element.name)
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


class LinkParser(BaseElementParser):
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


class ListParser(BaseElementParser):
    """
    List parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/story_elements/list.json>`_

    Example:

    .. code-block:: html

        <ul>
            <li>Post Reports is the daily podcast from The Washington Post.</li>
            <li>Unparalleled reporting.</li>
            <li>Expert insight.</li>
            <li>Clear analysis.</li>
        </ul>

    ->

    .. code-block:: python

        {
            "type": "list",
            "list_type": "unordered",
            "items": [
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
    applicable_elements = ['ul', 'ol']

    def parse(self, element, *args, **kwargs):
        if element.name == 'ul':
            list_type = 'unordered'
        else:
            list_type = 'ordered'
        list_elements = []
        for list_item in element.contents:
            # as of ANS 0.6.2, has to be either text or another list
            # https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.6.2/story_elements/list_element.json
            if isinstance(list_item, Tag) and list_item.contents:
                # we could do something complicated so that this parser has its own sub-parsers
                # but for the time being, assume the list items are fairly simple
                # if this item is wrapping something else, just take the first child
                list_item = list_item.contents[0]
            if isinstance(list_item, Tag) and list_item.name in self.applicable_elements:
                parsed_list_item = self.parse(list_item).output
                field_check = "items"
            else:
                parsed_list_item = ParagraphParser().parse(list_item).output
                field_check = "content"
            if isinstance(parsed_list_item, dict) and parsed_list_item.get(field_check):
                list_elements.append(parsed_list_item)

        result = self.construct_output(element, "list")
        result["list_type"] = list_type
        result["items"] = list_elements
        return ParseResult(result, True)
