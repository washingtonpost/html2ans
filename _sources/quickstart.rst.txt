Quickstart
==========


Generating ANS from HTML
------------------------

.. code-block:: python

    from html2ans.default import Html2Ans

    parser = Html2Ans()
    content_elements = parser.generate_ans(your_html_here)


Adding Parsers
--------------

Basic Addition
^^^^^^^^^^^^^^

If you need to parse a certain tag in a customized way, you can write your own parser class and add it to the
parsers ``Html2Ans`` will use like so:


.. code-block:: python

    from html2ans.default import Html2Ans

    parser = Html2Ans()
    parser.add_parser(YourCustomImageParser())
    parser.generate_ans(your_html_here)


The default parser class (``DefaultHtmlAnsParser`` or ``Html2Ans``) has parsers for text, links, images, various social media embeds, etc.


Prioritized Addition
^^^^^^^^^^^^^^^^^^^^

The parsers that can be used for each element type (e.g. ``img``, ``p``) are held in a list. If you want your parser to have a higher priority than the default parsers, add it like so:

.. code-block:: python

    from html2ans.default import Html2Ans

    parser = Html2Ans()
    parser.insert_parser('img', YourCustomImageParser(), 0)
    parser.generate_ans(your_html_here)


Creating Custom Parsers
-----------------------

Missing from the snippet above is a definition of ``YourCustomImageParser``. Before talking about how to create such a parser,
let's examine why you might need to do so.

The default image parser ``html2ans.parsers.image.ImageParser`` applies to html ``img`` tags only. Imagine you need to parse html whose images come in ``div`` tags (labelled with the class ``fancy-figure``) that also hold a caption (labelled with the class ``fancy-caption``). Here is a possible implementation of a parser for such images (note: this returns basic image ANS, not a reference): 

.. code-block:: python

    from html2ans.parsers.image import ImageParser
    from html2ans.parsers.base import ParseResult

    class YourCustomImageParser(ImageParser):
        applicable_elements = ['div']
        applicable_classes = ['fancy-figure']

        def parse(self, element, *args, **kwargs):
            image_tag = element.find('img')
            caption_tag = element.find('p', {"class": "fancy-caption"})
            if image_tag:
                image = self.construct_output(image_tag)
                if caption_tag:
                  image["caption"] = caption_tag.text
                return ParseResult(image, True)
            return ParseResult(None, True)
