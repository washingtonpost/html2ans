# Contributing to html2ans

Welcome to the contribution guide for html2ans. Here are some important resources to get you started:
  
  * [html2ans Wiki](https://github.com/washingtonpost/html2ans/wiki)
  * [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  
## Questions or Issues
If you can't find an answer to your question in the above, please open an [issue](https://github.com/washingtonpost/html2ans/issues).

## Testing
html2ans has unit tests built with [tox](https://tox.readthedocs.io/en/latest/). If you create new functionality, please include tests along with it.

## Submitting changes
Please make a pull request on html2ans with a clear list of what you've done (you can read more about [Github pull requests here](http://help.github.com/pull-requests/)). Please follow the best practices guide below and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

## Best Practices

  * Follow [pep8](https://www.python.org/dev/peps/pep-0008/)
  * Code should be documented and commented using rST formatting for [Sphinx](https://www.sphinx-doc.org/en/master/index.html)
    - Example: https://www.datacamp.com/community/tutorials/docstrings-python#fifth-sub
  * Please make sure you've tested your code by running tox prior to submitting a pull request 
