from html2ans.parsers.base import BaseElementParser, ParseResult


class AudioParser(BaseElementParser):
    """
    Audio element parser. `ANS schema
    <https://github.com/washingtonpost/ans-schema/blob/master/src/main/resources/schema/ans/0.8.0/audio.json>`_

    Example:

    .. code-block:: html

        <audio><source src="postreports.mp3" /></audio>

    ->

    .. code-block:: python

        {
            "type": "audio",
            "version": "0.8.0",
            "streams": [
                "url": "postreports.mp3"
            ]
        }

    """
    applicable_elements = ['audio']
    version_required = True

    def parse(self, element, *args, **kwargs):
        result = None
        match = False
        source_element = element.find('source')
        if source_element:
            source_url = source_element.attrs.get('src')
            if source_url:
                result = self.construct_output(element, "audio")
                result["streams"] = [{
                    # url encodes any illegal url characters
                    "url": self._create_encoded_url(source_url)
                }]
                match = True
        return ParseResult(result, match)
