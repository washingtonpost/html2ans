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


def test_audio_with_spaces_in_src(parser, make_tag):
    tag = make_tag('<audio id="asset-1234" class="audio-player" controls="controls">'
                   '<source src="http://example.com/audio/name with spaces.mp3" type="audio/mpeg">'
                   '</audio>',
                   'audio')
    parsed = parser.parse(tag)[0]
    assert parsed.get('type') == 'audio'
    assert parsed.get("additional_properties", {}).get("class") == ["audio-player"]
    assert parsed.get("additional_properties", {}).get("controls") == "controls"
    assert parsed.get("additional_properties", {}).get("id") == "asset-1234"
    assert parsed.get('streams')[0]["url"] == "http://example.com/audio/name%20with%20spaces.mp3"
