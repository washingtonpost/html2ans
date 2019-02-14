import six

from bs4.element import NavigableString, Tag


def has_attributes(tag, filter_types=('id', 'class', 'style')):
    if isinstance(tag, Tag) and tag.attrs:
        return len(list(filter(lambda attr: attr not in filter_types, tag.attrs))) > 0
    return False


def parse_dimensions(tag, tag_json, dimension_keys=('width', 'height')):
    """
    Adds dimensions to converted JSON. Images and iframes will generally
    have width/height properties;
    this is just a convenience method for adding those properties.
    :param tag:
    :param tag_json:
    :param dimension_keys:
    :return:
    """
    for dimension_key in dimension_keys:
        try:
            tag_json[dimension_key] = int(tag.attrs.get(dimension_key))
        except Exception:
            pass


class AbstractParserUtilities(object):

    WRAPPER_TAGS = ['p', 'div']

    EMPTY_STRINGS = [None, '', '', ' ', '\n', '<br>', '<br/>']

    EMPTY_TAGS = ['br']

    TEXT_TAGS = [
        'blockquote',
        'p',
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
        'span']

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
        Returns true if the given tag only has NavigableStrings or
        tags in TEXT_TYPES for children.
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
        Returns the given tag's children (excluding the filter_types and filter_tags).
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
