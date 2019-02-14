from bs4 import BeautifulSoup, NavigableString, Tag
from html2ans.parsers.base import AbstractParserUtilities, ParseResult
from html2ans.exc import ParsingException


class AbstractHtmlAnsParser(object):
    """
    The abstract base root/top-level parser class. Makes no assumptions about
    underlying libraries.
    """

    def generate_ans(self, html, *args, **kwargs):
        """
        Parses html and produces ANS in a jsonify-able format.

        :param html: the html to parse
        :type html: str
        :return: a list of ANS elements as dictionaries

        """
        raise NotImplementedError()


class BaseHtmlAnsParser(AbstractHtmlAnsParser, AbstractParserUtilities):
    """
    The base root/top-level parser class; assumes elements will be parsed with ``BeautifulSoup``.
    Use this class to generate a list of ANS elements from an HTML document.
    HTML elements within the document will be parsed using
    element parsers present in the ``parsers`` attribute. The ``parsers`` attribute is populated
    first with the parsers from the ``DEFAULT_PARSERS`` variable. Other parsers can be added
    using this class's ``add_parser`` and ``insert_parser`` methods.

    Attempts at parsing an element will use each parser in an element's parser list in order.
    If a parser isn't applicable (``is_applicable`` returns ``False``) or ``parse`` indicates
    this element wasn't a match, the next parser is tried. Why are there two ways of indicating
    if an element/parser are compatable? You can't always tell if an element/parser are compatible
    until you're parsing the element. ``is_applicable`` catches early, obvious issues (like "this
    parser is for ``img`` elements; is this an ``img``?).

    Using an ``ans_version`` won't affect the output of these parsers in terms of actual
    ANS version compatibility; it is provided as a convenience (sometimes you need to update
    the overall ANS version because of a specific new feature, but won't want to update the
    output of all parsers).

    Use the ``suppress_exceptions`` option to treat element parsing exceptions as non-matches.
    With ``suppress_exceptions``, when exceptions are thrown, the next parser will be tried (as
    though ``is_applicable`` returned ``False``).

    :keyword ans_version: the ANS version to apply to the output of parsers that require a version
    :type ans_version: str
    :keyword bs_parse_lib: the BeautifulSoup parsing library to use
    :type bs_parse_lib: str
    :keyword suppress_exceptions: whether or not to suppress exceptions during element parsing
    :type suppress_exceptions: bool
    :keyword default_parsers: The default parsers to populate ``parsers`` with. Order matters here!
    :type default_parsers: list

    """

    BACKUP_PARSERS = []
    """
    The backup parsers for this class to use. This list will be used on _every_ parsing
    attempt if the primary parsers for a given type don't match. For example, if ``parsers``
    contains ``'p': [ParagraphParser()]`` and an exception is thrown when processing a
    paragraph tag using the ``ParagraphParser``, all backup parsers will also be tried. In
    the default implementation, this essentially means that producing raw_html will be
    the last resort when all other parsers fail.
    """

    def __init__(
            self,
            ans_version=None,
            soup_parse_lib='lxml',
            suppress_exceptions=False,
            default_parsers=None,
            *args,
            **kwargs):
        self.ans_version = ans_version
        self.soup_parse_lib = soup_parse_lib
        self.suppress_exceptions = suppress_exceptions
        self.parsers = {}
        """
        A mapping of potential HTML elements to a list of
        parsers to use to attempt to parse elements of that type
        """

        default_parsers = default_parsers or []
        for parser in default_parsers:
            self.add_parser(parser)
        super(BaseHtmlAnsParser, self).__init__()

    def generate_ans(self, html, start_tag="body", *args, **kwargs):
        """
        Parses html and produces ANS in a jsonify-able format.

        :param html: the html to parse
        :type html: str
        :param start_tag: where to start parsing (if not provided, all tags will be parsed)
        :type start_tag: str
        :return: a list of ANS elements as dictionaries

        """
        soup = BeautifulSoup(html, self.soup_parse_lib)
        main_tag = soup.find(start_tag)
        if main_tag:
            return self._parse_elements(main_tag.children)
        else:
            return self._parse_elements(soup.find_all(True))

    def insert_parser(self, element_key, parser, position=None, *args, **kwargs):
        """
        Insert a parser of the given type into the list of parsers for that type.

        :param element_key: The key of the element in self.parsers (e.g. 'p')
        :type element_key: str
        :param parser: The parser object to insert
        :type parser: html2ans.parsers.base.ElementParser
        :param position: Where to insert the parser in the list
        :type position: int

        """
        applicable_parsers = self.parsers.get(element_key, [])
        if position is not None:
            applicable_parsers.insert(position, parser)
        else:
            applicable_parsers.append(parser)
        self.parsers[element_key] = applicable_parsers

    def add_parser(self, parser, *args, **kwargs):
        """
        Add a parser to ``self.parsers`` using the parser's ``applicable_elements``.

        :param parser: The parser object to insert
        :type parser: html2ans.parsers.base.BaseElementParser

        """
        for element_key in parser.applicable_elements:
            self.insert_parser(element_key, parser)

    def _parse_elements(self, elements, *args, **kwargs):
        """
        Parses a list of html elements (produced by ``BeautifulSoup``) to ANS.

        :param elements: the list of children to parse
        :return: a list of ANS elements

        """
        output_elements = []
        for item in elements:
            if not self.is_empty(item):
                if self.is_wrapper(item) and isinstance(item, Tag):
                    output_elements.extend(self._parse_elements(item.children))
                elif isinstance(item, Tag):
                    self._parse_element(item.name, item, output_elements)
                else:
                    self._parse_element(type(item), item, output_elements)
        return output_elements

    def _parse_element(self, element_key, element, output_elements):
        """
        Builds a list of parsers for the given element (using ``self.parsers`` and
        ``self.BACKUP_PARSERS``). If ``_attempt_element_parse`` returns a
        successful result, adds that result to the list of ``output_elements``.
        """
        parser_candidates = self.parsers.get(element_key, [])
        # if none of the parser_candidates work, we want to check for embeds or
        # lastly, use raw_html
        # the BACKUP_PARSERS handle this logic
        parser_candidates.extend(self.BACKUP_PARSERS)
        parser_result = self._attempt_element_parse(element, parser_candidates)
        if parser_result.match and parser_result.output:
            if isinstance(parser_result.output, list):
                # allows parsers to parser out multiple elements
                output_elements.extend(filter(None, parser_result.output))
            else:
                output_elements.append(parser_result.output)

    def _attempt_element_parse(self, element, parser_candidates):
        """
        Tries to parse the given ``element`` using each parser in ``parser_candidates``
        until one is a match. If the parser has ``version_required`` set to true, the
        ANS version is added to the output.
        """
        for parser in parser_candidates:
            try:
                if parser.is_applicable(element):
                    parser_result = parser.parse(element)
                    if parser_result.match:
                        if parser_result.output and parser.version_required:
                            parser_result.output.setdefault("version", self.ans_version)
                        return parser_result
            except Exception as exc:
                if self.suppress_exceptions:
                    continue
                else:
                    raise ParsingException(exc)
        return ParseResult(None, False)
