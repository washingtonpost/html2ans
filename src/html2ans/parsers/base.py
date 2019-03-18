from collections import namedtuple
from functools import reduce

from bs4.element import Comment, Tag

from html2ans.parsers.utils import AbstractParserUtilities


class ParseResult(namedtuple('ParseResult', ['output', 'match'])):
    """
    A wrapper for holding the results of parsing.

    ``output`` is the ANS JSON parsed by the parser.

    ``match`` indicates whether or not other parse attempts should be made.

    The idea of the parsing "match" is necessary so that we can try
    multiple parsers per tag (and not try multiple parsers when we don't have to).
    For example, when parsing ``<p></p>``, if we only returned an empty dictionary
    with the first available parser, the next logical step is to try the next parser.
    By returning ``match=True`` in that situation, we don't make any more
    parsing attempts, we just move on to the next element in the tree.

    :param output: The output ANS
    :type output: dict or list[dict]
    :param match: Whether or not this parse was a match for a given element
    :type match: bool
    """
    pass


class ElementParser(object):
    """
    Element parsing interface.
    """

    def is_applicable(self, element, *args, **kwargs):
        """
        Indicates if the given element is something this
        parser can/should be parsing.

        :param element: the element to check for applicability
        :type element: bs4.element.Tag or bs4.element.Comment or bs4.element.NavigableString
        """
        raise NotImplementedError()

    def parse(self, element, *args, **kwargs):
        """
        Parses the given element.

        :param element: the element to parse
        :type element: bs4.element.Tag or bs4.element.Comment or bs4.element.NavigableString
        """
        raise NotImplementedError()


class BaseElementParser(ElementParser, AbstractParserUtilities):
    """
    Base element parser; assumes elements are being parsed using
    BeautifulSoup. Provides a standard method of checking for
    applicability via ``applicable_elements`` and ``applicable_classes``.
    """

    version_required = False
    """
    Whether or not a version should be added to this parser's
    output in the root document parser
    """

    applicable_elements = []
    """
    The types of elements this parser should be used on. For example,
    ``applicable_elements = [Comment, 'br']`` indicates that this parser
    is meant for ``Comment`` objects and br tags.
    """

    applicable_classes = []
    """
    The classes of elements this parser should be used on. This is an
    extra requirement on top of ``applicable_elements``--if this list is
    populated, then an HTML tag must have an applicable name and an
    applicable class in order to be considered. For example, if
    ``applicable_elements = ['div']`` and ``applicable_classes = ['headlines']``,
    ``<div><img ...><p>My headline</p></div>`` would not be considered applicable
    but ``<div class="headlines"><img ...><p>My headline</p></div>`` would.
    """

    def is_applicable(self, element, *args, **kwargs):
        """
        Checks applicability using ``applicable_elements`` and, optionally,
        ``applicable_classes``

        :param element: the element to parse
        :type element: bs4.element.Tag or bs4.element.Comment or bs4.element.NavigableString
        """
        is_element_applicable = False
        if isinstance(element, Tag) and element.name in self.applicable_elements:
            is_element_applicable = True
            if self.applicable_classes:
                is_element_applicable = is_element_applicable and self.is_class_applicable(element)
        elif type(element) in self.applicable_elements:
            is_element_applicable = True
        return is_element_applicable

    def is_class_applicable(self, tag):
        classes = tag.attrs.get('class')
        return classes and reduce(
            lambda x, y: x and y,
            list(applicable_class in classes for applicable_class in self.applicable_classes))

    def construct_output(self, element, ans_type=None, content=None, version=None, *args, **kwargs):
        """
        Convenience method for constructing an output dictionary. If element is a ``Tag`` with
        attributes, those attributes will be stashed in ``additional_properties``.

        :param element: the element being parsed
        :type element: bs4.element.Tag or bs4.element.Comment or bs4.element.NavigableString
        :param ans_type: the ANS type to put in the output ``type`` field
        :type ans_type: str
        :param content: the content to put in the ``content`` field
        :type content: str
        :param version: the version to put in the ``version`` field. Note: if not provided but
            ``version_required=True`` on this parser, the output will receive a version from the
            root parser
        :type version: str

        """
        result = {}
        if ans_type:
            result["type"] = ans_type
        if content:
            result["content"] = content
        if isinstance(element, Tag):
            if element.attrs:
                result["additional_properties"] = element.attrs
        if version:
            result["version"] = version
        return result


class NullParser(BaseElementParser):
    """
    Parser for elements we want to ignore in the output ANS.
    """

    applicable_elements = [Comment, 'br']

    def is_applicable(self, element, *args, **kwargs):
        return True

    def parse(self, element, *args, **kwargs):
        return ParseResult(None, True)
