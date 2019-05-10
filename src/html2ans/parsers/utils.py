import six

from bs4.element import NavigableString, Tag
from furl import furl


def has_attributes(tag, filter_types=('id', 'class', 'style')):
    """
    Helper function to check if a tag has attributes (excluding the given ``filter_types``).
    """
    if isinstance(tag, Tag) and tag.attrs:
        return len(list(filter(lambda attr: attr not in filter_types, tag.attrs))) > 0
    return False


def parse_dimensions(tag, tag_json, dimension_keys=('width', 'height')):
    """
    Adds dimensions to converted JSON. Images and iframes will generally
    have width/height properties; this is just a convenience method for
    adding those properties.
    """
    for dimension_key in dimension_keys:
        try:
            tag_json[dimension_key] = int(tag.attrs.get(dimension_key))
        except Exception:
            pass


class AbstractParserUtilities(object):
    """
    Common utility functions for parsers. These methods are grouped here (rather
    than in the ``BaseElementParser``) because they are used both in element
    parsing and in document parser (i.e. by the ``BaseHtmlAnsParser``).
    """

    WRAPPER_TAGS = ['p', 'div']
    """
    Which tags to consider as potential wrappers in the ``is_wrapper`` method.
    """

    EMPTY_STRINGS = [None, '', ' ', '\n', '<br>', '<br/>']
    """
    List of strings considered empty (if a ``NavigableString`` is passed to
    ``is_empty`` and the string is in this list, ``is_empty`` will return True).
    """

    EMPTY_TAGS = ['br']
    """
    List of tags considered empty (if a tag passed to ``is_empty`` is in this list,
    ``is_empty`` will return True).
    """
    INLINE_TAGS = [
        'a',
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
        'span'
    ]

    TEXT_TAGS = INLINE_TAGS + ['p', 'blockquote']
    """
    List of tags considered to be text. This affects the results of ``is_text_only``
    which is used by most text parsers. For example, because by default ``a`` tags
    are considered text, ``<p>Here is a <a href="google.com">link</a></p>`` would
    be considered text only.
    """

    @classmethod
    def is_empty(cls, element, *args, **kwargs):
        """
        Returns true if the given tag is empty. Things like \n, <p>\n</p>, <iframe />
        are considered empty.
        :param tag: the tag to check
        :return: True if empty

        """
        result = False
        if isinstance(element, NavigableString):
            result = six.text_type(element).strip() in cls.EMPTY_STRINGS
        elif element.name in cls.EMPTY_TAGS:
            result = True
        elif not (cls.get_children(element) or has_attributes(element)):
            result = True
        return result

    @classmethod
    def is_text_only(cls, element, *args, **kwargs):
        """
        Returns true if the given tag only has ``NavigableString`` or
        tags in ``TEXT_TYPES`` for children.
        :param element:
        :return: True if this element only contains text
        """
        result = False
        if not element:
            result = True
        elif isinstance(element, NavigableString):
            result = True
        elif element.name not in cls.TEXT_TAGS:
            result = False
        else:
            result = not list(filter(lambda child: not cls.is_text_only(child), cls.get_children(element)))
        return result

    @classmethod
    def is_wrapper(cls, element, *args, **kwargs):
        """
        Returns true if this tag is only wrapping other content.
        :param element:
        :return: True if the given element is only wrapping sub-content
        """
        # is this something we should even consider unwrapping?
        if element.name in cls.WRAPPER_TAGS:
            # check 1: if the element has attributes, it's not a wrapper
            # e.g. <a href="google.com"></a>
            # obviously this will also catch things like <p class="fancy"><p>Some other text</p></p>
            # but we can't account for all possible bad html
            if not (element.attrs and has_attributes(element)):
                # check 2: if the item is text only, we probably don't want to unwrap it
                # for example, <p><img src="awesome_image" /></p> we DO want to unwrap
                # but <p>A <a href="awesome_image">link</a> to a cool image</p> we DON'T
                return not (cls.is_text_only(element) and len(cls.get_children(element)) > 1)
        return False

    @classmethod
    def get_children(cls, element, filter_tags=None, filter_types=None):
        """
        Returns the given tag's children (excluding the ``filter_types`` and
        ``filter_tags``).
        :param element: the element to check
        :param filter_types: class types to filter from the tag's children
        :param filter_tags: tag names to filter from the tag's children
        :return: the unfiltered/unempty children if element is a Tag, else []
        """
        if not filter_tags:
            filter_tags = []
        if not filter_types:
            filter_types = []
        result = []
        if element and isinstance(element, Tag):
            for child in element.children:
                if not cls.is_empty(child):
                    if isinstance(child, Tag):
                        if child.name not in filter_tags:
                            result.append(child)
                    elif not [isinstance(child, filter_type) for filter_type in filter_types]:
                        result.append(child)
        return result

    def _create_encoded_url(self, original_url):
        """
        Url encode path a uri.

        :param original_url: str URI value
        :return: URI value properly url encoded to include in ans
        """

        return furl(original_url).url
