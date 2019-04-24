Development
===========

Getting set up
--------------

* Clone this repo
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


Release Process
---------------

* New releases will be pushed to pypi when an appropriate tag (i.e. a version number in the form X.X.X) is pushed
* In preparation for a new release:

  - Decide what the next version will be per `semantic versioning <https://semver.org/>`_
  - Make a new branch called ``release/<version number>``
  - Update the version in ``setup.py`` 
  - Update the changelog for all changes that will be included in the release
  - Commit your changes and make a PR against master
  - Once the changes are merged, tag the branch with the version's release number and push that tag
  - Merge master into dev
