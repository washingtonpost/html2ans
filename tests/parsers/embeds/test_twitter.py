# -*- coding: utf-8 -*-
import pytest
from html2ans.parsers.embeds import (
    TwitterTweetEmbedParser,
    TwitterVideoEmbedParser
)


@pytest.mark.parametrize('tag_string,expected_id,tag_lang', [
    ('<blockquote class="twitter-tweet" data-lang="en">'
     '<p lang="en" dir="ltr">.<a href="https://twitter.com/CityDogsRescue">'
     '@CityDogsRescue</a> facilitated 712 adoptions in 2015—best decision I '
     'ever made was to be one of those adopters. <a href="https://t.co/eLKIuPSfE0">'
     'pic.twitter.com/eLKIuPSfE0</a></p>&mdash; Melissa Steffan (@melissasteffan) '
     '<a href="https://twitter.com/melissasteffan/status/692759996610715648">'
     'January 28, 2016</a></blockquote>',
     "692759996610715648",
     "en"),
    ('<blockquote class=\"twitter-tweet\" data-lang=\"fr\">'
     '<p lang=\"fr\" dir=\"ltr\">La Marseillaise retentit avant lentr\u00e9e des'
     ' cercueils de Simone et Antoine Veil au Panth\u00e9on '
     '<a href=\"https://t.co/QWCChWtVcx\">pic.twitter.com/QWCChWtVcx</a></p>'
     '\u2014 BFMTV (@BFMTV) <a href=\"https://twitter.com/BFMTV/status/'
     '1013363643424100354?ref_src=twsrc%5Etfw\">1 juillet 2018</a></blockquote>',
     "1013363643424100354",
     "fr"),
    ('<blockquote class="twitter-tweet" data-lang="en">'
     '<p lang="en" dir="ltr">Analysis: Trump broke his word on Jamal Khashoggi'
     ' — plain and simple <a href="https://t.co/oDnShqp7sw">https://t.co/oDnShqp7sw'
     '</a></p>&mdash; The Washington Post (@washingtonpost) '
     '<a href="https://twitter.com/washingtonpost/status/1065283964343074817'
     '?ref_src=twsrc%5Etfw">November 21, 2018</a></blockquote>',
     "1065283964343074817",
     "en"),
    ('<blockquote class="twitter-tweet" data-lang="en">'
     '<p lang="en" dir="ltr">.<a href="https://twitter.com/Acosta?ref_src=twsrc%5Etfw">'
     '@Acosta</a>: ”Are you letting the Saudis get away with murder, murdering a '
     'journalist?&quot;<br><br>President Trump: “No. This is about America First. '
     'They’re paying us $400 billion plus to purchase and invest in our country.”'
     ' <a href="https://t.co/fCTCd1cFyV">https://t.co/fCTCd1cFyV</a> '
     '<a href="https://t.co/O9URVX1HkW">pic.twitter.com/O9URVX1HkW</a></p>&mdash; '
     'The Situation Room (@CNNSitRoom) <a href="https://twitter.com/CNNSitRoom/status/'
     '1065023224893841408?ref_src=twsrc%5Etfw">November 20, 2018</a></blockquote>',
     "1065023224893841408",
     "en"),
    ('<blockquote class="twitter-tweet" data-lang="en">'
     '<p lang="en" dir="ltr">Displaced by Woolsey fire, Malibu families gather '
     'for a meal and hugs: <a href="https://t.co/W3ZWJIKOjG">https://t.co/W3ZWJIKOjG</a> '
     '<a href="https://t.co/FUouJS6xwl">pic.twitter.com/FUouJS6xwl</a></p>&mdash; '
     'Los Angeles Times (@latimes) <a href="https://twitter.com/latimes/status/'
     '1065323995959037953?ref_src=twsrc%5Etfw">November 21, 2018</a></blockquote>',
     "1065323995959037953",
     "en"),
    ('<blockquote class="twitter-tweet" data-lang="fr">'
     '<p lang="fr" dir="ltr">Le gilet jaune, symbole d’une “situation d’urgence sociale” '
     '<a href="https://t.co/uvxlBMDzun">https://t.co/uvxlBMDzun</a> '
     '<a href="https://t.co/i9qQ1hIYts">pic.twitter.com/i9qQ1hIYts</a></p>'
     '&mdash; FRANCE 24 Français (@France24_fr) <a href="https://twitter.com/France24_fr'
     '/status/1065322223064367104?ref_src=twsrc%5Etfw">November 21, 2018</a></blockquote>',
     "1065322223064367104",
     "fr")
])
def test_tweet_embed_parser(tag_string, expected_id, tag_lang, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "blockquote")
        result, match = TwitterTweetEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "twitter"
        assert result["referent"]["provider"] == TwitterTweetEmbedParser.provider
        assert result["referent"]["service"] == "oembed"
        assert result["additional_properties"]["class"][0] == "twitter-tweet"
        assert result["additional_properties"]["data-lang"] == tag_lang


@pytest.mark.parametrize('tag_string,expected_id,tag_lang', [
    ('<blockquote class="twitter-video" data-lang="es">'
     '<p dir="ltr" lang="es">¡GRACIAS! <a href="https://t.co/OYvbV0lqGB">'
     'pic.twitter.com/OYvbV0lqGB</a></p>\n<p>— Granaderos a Caballo (@Granaderosarg) '
     '<a href="https://twitter.com/Granaderosarg/status/752635477799370752">'
     'July 11, 2016</a></p></blockquote>',
     "752635477799370752",
     "es"),
    ('<blockquote class="twitter-video" data-lang="en">'
     '<p lang="en" dir="ltr">A waterspout caused havoc at a port in southern Italy, '
     'overturning shipping containers and sending others into the water.<br>'
     '<br>For more videos like this one, head here: '
     '<a href="https://t.co/iOm40vn1kt">https://t.co/iOm40vn1kt</a> '
     '<a href="https://t.co/fJq2vzHXRF">pic.twitter.com/fJq2vzHXRF</a></p>&mdash; '
     'Sky News (@SkyNews) <a href="https://twitter.com/SkyNews/status/1065291355713355776'
     '?ref_src=twsrc%5Etfw">November 21, 2018</a></blockquote>',
     "1065291355713355776",
     "en"),
    ('<blockquote class="twitter-video" data-lang="de">'
     '<p lang="de" dir="ltr">Am Sonntag wird in Hannover gefeiert! '
     'Die HAZ lädt alle Eltern und ihre Kinder zum großen Familienfest ans Rathaus ein. '
     '<a href="https://twitter.com/hashtag/Einschulung?src=hash&amp;ref_src=twsrc%5Etfw">'
     '#Einschulung</a> <a href="https://twitter.com/hashtag/HAZfest?'
     'src=hash&amp;ref_src=twsrc%5Etfw">#HAZfest</a> '
     '<a href="https://twitter.com/hashtag/AktionSichererSchulweg?src=hash&amp;'
     'ref_src=twsrc%5Etfw">#AktionSichererSchulweg</a> <a href="https://t.co/8q7hHjy1zK">'
     'pic.twitter.com/8q7hHjy1zK</a></p>&mdash; HAZ (@HAZ) '
     '<a href="https://twitter.com/HAZ/status/1027958659404521475?ref_src=twsrc%5Etfw">'
     'August 10, 2018</a></blockquote>',
     "1027958659404521475",
     "de")
])
def test_video_embed_parser(tag_string, expected_id, tag_lang, make_http_tag, make_https_tag):
    for test_function in [make_http_tag, make_https_tag]:
        embed_tag = test_function(tag_string, "blockquote")
        result, match = TwitterVideoEmbedParser().parse(embed_tag)
        assert match is True
        assert result["type"] == "reference"
        assert result["referent"]["id"] == expected_id
        assert result["referent"]["type"] == "twitter"
        assert result["referent"]["provider"] == TwitterVideoEmbedParser.provider
        assert result["referent"]["service"] == "oembed"
        assert result["additional_properties"]["class"][0] == "twitter-video"
        assert result["additional_properties"]["data-lang"] == tag_lang
