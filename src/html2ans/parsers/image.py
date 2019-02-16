from html2ans.parsers.utils import parse_dimensions
from html2ans.parsers.base import BaseElementParser, ParseResult


class AbstractImageParser(BaseElementParser):
    """
    Abstract class for image parsing.

    `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/image.json>`_
    """

    version_required = True

    def _parse_dimensions(self, element, element_json, dimension_keys=('width', 'height')):
        parse_dimensions(element, element_json)

    def construct_output(self, element, *args, **kwargs):
        result = super(AbstractImageParser, self).construct_output(element, "image")
        result["url"] = element.attrs.get('src')
        caption = element.attrs.get('alt')
        if caption:
            result["caption"] = caption
        self._parse_dimensions(element, result)
        return result


class ImageParser(AbstractImageParser):
    """
    Basic img element parser.

    Example:

    .. code-block:: html

        <img src="postreports.jpg" alt="The Post Reports" width="50" height="50" />

    ->

    .. code-block:: python

        {
            "type": "image",
            "version": "0.8.0",
            "url": "postreports.jpg",
            "caption": "The Post Reports",
            "width": 50,
            "height": 50
        }

    """
    applicable_elements = ['img']

    def parse(self, element, *args, **kwargs):
        if element.attrs.get('src'):
            return ParseResult(self.construct_output(element), True)
        return ParseResult(None, True)


class LinkedImageParser(ImageParser):
    """
    Link-wrapped image parser.

    Example:

    .. code-block:: html

        <a href="https://www.stitcher.com/podcast/the-washington-post/post-reports">
            <img src="postreports.jpg" alt="The Post Reports" width="50" height="50" />
        </a>

    ->

    .. code-block:: python

        {
            "type": "image",
            "version": "0.8.0",
            "url": "postreports.jpg",
            "caption": "The Post Reports",
            "width": 50,
            "height": 50,
            "additional_properties": {
                "image_link": "https://www.stitcher.com/podcast/the-washington-post/post-reports"
            }
        }

    """
    applicable_elements = ['a']

    def is_applicable(self, element, *args, **kwargs):
        return super(LinkedImageParser, self).is_applicable(element) and element.find('img')

    def parse(self, element, *args, **kwargs):
        img_element = element.find('img')
        if img_element:
            parsed_result = super(LinkedImageParser, self).parse(img_element)
            if parsed_result.output:
                image_link = element.attrs.get('href')
                if image_link:
                    parsed_result.output["additional_properties"] = {
                        "image_link": image_link
                    }
                return parsed_result
        return ParseResult(None, False)


class FigureParser(ImageParser):
    """
    Figure-wrapped image parser.

    Example:

    .. code-block:: html

        <figure>
            <img src="postreports.jpg" alt="The Post Reports logo" width="50" height="50" />
            <figcaption>The Post Reports</figcaption>
        </figure>

    ->

    .. code-block:: python

        {
            "type": "image",
            "version": "0.8.0",
            "url": "postreports.jpg",
            "caption": "The Post Reports",
            "width": 50,
            "height": 50
        }

    """
    applicable_elements = ['figure']

    def parse(self, element, *args, **kwargs):
        result = None
        match = True
        img_element = element.find('img')
        if img_element:
            parsed_result = super(FigureParser, self).parse(img_element)
            if parsed_result.output:
                caption = self._parse_caption(element)
                if caption:
                    parsed_result.output['caption'] = caption
            return parsed_result
        return ParseResult(result, match)

    def _parse_caption(self, element):
        result = ''
        caption_element = element.find('figcaption')
        if caption_element:
            result = caption_element.text.strip()
        return result
