import re

import pytest

from bs4 import BeautifulSoup, NavigableString, Tag


@pytest.fixture(scope='session')
def make_tag():

    def func(html, tag_type):
        if html is tag_type is None:
            return None
        if not tag_type:
            return NavigableString(html)
        return BeautifulSoup(html, 'lxml').find_all(tag_type)[0]

    return func


@pytest.fixture(scope='session')
def make_div_tag(make_tag):

    def func(html):
        return make_tag(html, 'div')

    return func


@pytest.fixture(scope='session')
def make_p_tag(make_tag):

    def func(html):
        return make_tag(html, 'p')

    return func


@pytest.fixture(scope="session")
def make_http_tag(make_tag):

    def func(html, tag_type):
        html = re.sub(r'https?', r'http', html)

        return make_tag(html, tag_type)

    return func


@pytest.fixture(scope="session")
def make_https_tag(make_tag):

    def func(html, tag_type):
        html = re.sub(r'https?', r'https', html)

        return make_tag(html, tag_type)

    return func
