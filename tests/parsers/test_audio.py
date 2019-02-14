import pytest
from html2ans.parsers.audio import AudioParser


@pytest.fixture
def parser():
    return AudioParser()


@pytest.fixture(params=[
    '<audio></audio>',
])
def valid_audio_tag(request):
    return request.param


def test_empty(parser, make_tag):
    tag = make_tag('<audio></audio>', 'audio')
    assert (None, False) == parser.parse(tag)


def test_is_applicable(parser, valid_audio_tag, make_tag):
    assert parser.is_applicable(make_tag(valid_audio_tag, 'audio'))


def test_audio(parser, make_tag):
    tag = make_tag('<audio><source src=audiosource /></audio>', 'audio')
    parsed = parser.parse(tag)[0]
    assert parsed.get('streams')[0]["url"] == 'audiosource'
    assert parsed.get('type') == 'audio'
