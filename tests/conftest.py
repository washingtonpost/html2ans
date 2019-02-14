from io import open
import json
import os
import pytest

from html2ans.default import DefaultHtmlAnsParser

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture
def test_html2ans():
    return DefaultHtmlAnsParser('0.8.0', 'lxml')


@pytest.fixture(scope='session')
def get_html_fixture():

    def loader(file_name):

        with open(os.path.join(FIXTURES_DIR, file_name), "r", encoding='utf8') as html_file:
            return html_file.read()

    return loader


@pytest.fixture(scope='session')
def get_json_data(get_html_fixture):

    def loader(filename, *args, **kwargs):

        fileobj = open(os.path.join(FIXTURES_DIR, filename), *args, **kwargs)
        return json.load(fileobj)

    return loader


@pytest.fixture(scope='session')
def write_html_fixture():

    def writer(file_name, content):

        with open(os.path.join(FIXTURES_DIR, file_name), 'w', encoding='utf8') as html_file:
            html_file.write(content)

    return writer
