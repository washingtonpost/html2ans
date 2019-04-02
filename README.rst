html2ans
========

.. image:: https://img.shields.io/pypi/v/html2ans.svg
    :target: https://pypi.org/project/html2ans/

.. image:: https://img.shields.io/pypi/pyversions/html2ans.svg
    :target: https://pypi.org/project/html2ans/

.. image:: https://circleci.com/gh/washingtonpost/html2ans.svg?style=shield
    :target: https://circleci.com/gh/washingtonpost/html2ans

.. image:: https://img.shields.io/pypi/l/html2ans.svg
    :target: https://pypi.python.org/pypi/html2ans/


This project provides a standardized method of parsing HTML elements into `ANS elements
<https://github.com/washingtonpost/ans-schema>`_. It is mainly used by Arc Publishing's
professional services team to migrate client data into the Arc platform, but can also be
used for arbitrary conversion of HTML to JSON.

html2ans is hosted on `pypi <https://pypi.org/project/html2ans/>`_.

Please use the `GitHub issue tracker <https://github.com/washingtonpost/html2ans/issues>`_ to submit bugs or request features.

Full documentation can be found `here <https://washingtonpost.github.io/html2ans/>`_.


Quickstart
----------

Generating ANS from HTML
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from html2ans.default import Html2Ans

    parser = Html2Ans()
    content_elements = parser.generate_ans(your_html_here)


Adding Parsers
~~~~~~~~~~~~~~

Basic Addition
^^^^^^^^^^^^^^

If you need to parse a certain tag in a customized way, you can write your own parser class and add it to the
parsers ``Html2Ans`` will use like so:


.. code-block:: python

    from html2ans.default import Html2Ans

    parser = Html2Ans()
    parser.add_parser(YourCustomImageParser())
    parser.generate_ans(your_html_here)


The types of items your parser can parse should be listed in its ``applicable_elements`` attribute.

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
~~~~~~~~~~~~~~~~~~~~~~~

Missing from the snippet above is a definition of ``YourCustomImageParser``. Before talking about how to create such a parser,
let's examine why you might need to do so.

The default image parser ``html2ans.parsers.image.ImageParser`` applies to html ``img`` tags only. Imagine you need to parse html whose images come in ``div`` tags (labelled with the class ``fancy-figure``) that also hold a caption (labelled with the class ``fancy-caption``). Here is a possible implementation of a parser for such images (note: this returns basic image ANS, not a reference): 

.. code-block:: python

    from html2ans.parsers.image import ImageParser
    from html2ans.parsers.base import ParseResult

    class YourCustomImageParser(ImageParser):
        applicable_elements = ['div', 'figure']
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


Custom Parsing Tips
~~~~~~~~~~~~~~~~~~~

ANS Versions
^^^^^^^^^^^^

Some ANS types require a version. You can set a version in your main parser (``Html2Ans``) and then automatically include that version in any element parser's output by setting the parser's ``version_required`` attribute to ``True``.

*Note: this doesn't mean valid, version-compatible ANS is automatically produced!*


Keeping HTML in ``text`` Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To adjust what HTML is/isn't left inline when parsing text, adjust the ``INLINE_TAGS`` attribute on the text parser. Every parser inherits from ``html2ans.parsers.utils.AbstractParserUtilities`` which provides a list of default ``INLINE_TAGS`` which can be used to make sure text formatters (e.g. ``strong``, ``em``, etc.) are left in place when text is parsed.


Link Parsing
^^^^^^^^^^^^

By default, ``a`` tags are left inline in text, assuming there is text outside of the link. A link by itself (e.g. ``<p><a href="google.com">Search</a></p>``) will be turned into an ``interstitial_link``. If ``interstitial_link`` elements are unwanted, simply add ``a`` to the list of ``applicable_elements`` for the ``ParagraphParser``.


Removing Unnecessary Tags
^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it is helpful to remove unnecessary tags (e.g. ``<p></p>``, ``<div><img src="..." /></div>``). By default, ``Html2Ans`` considers ``p`` and ``div`` tags with no attributes other than ``id``, ``class``, or ``style`` to be unnecessary "wrappers". When these are encountered, they are ignored and their children are parsed.

The benefit of this is that ``<p></p>`` is ignored and ``<div><img src="..." /></div>`` is parsed as an image.

The downside is that sometimes you don't want your HTML removed! There are a few options in this case. You can configure what tags can be considered wrappers via the ``WRAPPER_TAGS`` attribute on ``Html2Ans``. So if ``div`` tags should never be removed, simply remove ``div`` from this list. If a more complicated set of rules are necessary, override the ``is_wrapper`` method on ``Html2Ans``.

If it's easier to modify the HTML than to modify this library, you can also add an arbitrary attribute like so: ``<div no_parse_flag="true">...</div>``. This ``div`` will not be considered a wrapper when it is encountered.
