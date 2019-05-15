Changelog
=========


v3.0.3
------

* Fixes audio streaming url encoding


v3.0.2
------

* Fixes link parsing inside list elements by adding a ``ListItemParser`` (used by the ``ListParser``) and modifying the handling of inline tags in text


v3.0.1
------

* Adds ``DailyMotionEmbedParser``, ``FlickrEmbedParser``, ``PollDaddyEmbedParser``, and ``RedditEmbedParser`` to ``DEFAULT_PARSERS`` in ``Html2Ans``/``DefaultHtmlAnsParser``

  - These were accidentally left out of ``DEFAULT_PARSERS`` in v3.0.0

* Updates the ``InstagramEmbedParser`` to accept hyphens in embed IDs
* Internal improvements:

  - ``setup.py`` is now the source of truth for requirements
  - Stopped outputting a .pypirc for pypi deployment; instead using Twine environment variables in the circleci build config


v3.0.0
------

* Initial open source release!
