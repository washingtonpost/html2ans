Development
===========

Getting set up
--------------

* Clone this repo
* Make sure you have Python 3.6+ installed
* Ideally, set up a virtualenv and activate it (http://virtualenvwrapper.readthedocs.io/en/latest/)
* From your local copy of this project, run ``pip install -r requirements-dev.txt``
* Run tox with the command ``tox``
* If that completes successfully, you are good to go!
* Make sure you re-run tox before committing changes


Documentation
-------------

* The documentation for this project is generated using Sphinx and hosted via Github

  - See https://daler.github.io/sphinxdoc-test/includeme.html#publishing-sphinx-generated-docs-on-github

* Docs will be automatically generated and uploaded when a new version is released
* To update docs independent of a new release:

  - Follow `these instructions <https://daler.github.io/sphinxdoc-test/includeme.html#setting-up-cloned-repos-on-another-machine>`_
  - Run ``python setup.py build_sphinx``
  - ``cd ../html2ans-docs/html``
  - Commit and push the newly generated documentation
