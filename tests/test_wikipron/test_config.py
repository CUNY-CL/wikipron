import datetime
import re

import pytest
import requests_html

from wikipron.config import _PHONEMES_REGEX, _PHONES_REGEX
from wikipron.scrape import _PAGE_TEMPLATE, HTTP_HEADERS

from . import can_connect_to_wiktionary, config_factory

_TODAY = datetime.date.today()
_DATE_TODAY = _TODAY.isoformat()
_DATE_FUTURE = (_TODAY + datetime.timedelta(days=10)).isoformat()
_DATE_RECENT_PAST = (_TODAY - datetime.timedelta(days=10)).isoformat()
_DATE_DISTANT_PAST = (_TODAY - datetime.timedelta(days=20)).isoformat()


@pytest.mark.parametrize(
    "casefold, input_word, expected_word",
    [(True, "FooBar", "foobar"), (False, "FooBar", "FooBar")],
)
def test_casefold(casefold, input_word, expected_word):
    config = config_factory(casefold=casefold)
    assert config.casefold(input_word) == expected_word


@pytest.mark.parametrize(
    "stress, syllable_boundaries, input_pron, expected_pron",
    [
        (False, False, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ ɡ w ɪ s t ɪ k s"),
        (False, True, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ . ɡ w ɪ s . t ɪ k s"),
        (True, False, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ ˈɡ w ɪ s t ɪ k s"),
        (True, True, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ . ˈɡ w ɪ s . t ɪ k s"),
        # GH-59: Prons with only stress or syllable boundaries are skipped.
        (True, True, "ˈ", None),
        (True, True, ".", None),
        (True, True, "", None),
    ],
)
def test_process_pron(stress, syllable_boundaries, input_pron, expected_pron):
    config = config_factory(
        stress=stress, syllable_boundaries=syllable_boundaries
    )
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "segment, input_pron, expected_pron",
    [
        (True, "lɛ̃.ɡɥis.tik", "l ɛ̃ . ɡ ɥ i s . t i k"),
        (True, "kʰæt", "kʰ æ t"),
        (True, "ad͡ʒisɐ̃w", "a d͡ʒ i s ɐ̃ w"),
        (True, "ovoɫˈnʲɤ", "o v o ɫ ˈnʲ ɤ"),
        # GH-83: Challenging IPA tokenizations.
        (True, "ˌæb.oʊˈmaɪ.sɪn", "ˌæ b . o ʊ ˈm a ɪ . s ɪ n"),
        (True, "ʷoˈtɤu̯", "ʷo ˈt ɤ u̯"),
        (True, "ⁿdaˈɽá.ma", "ⁿd a ˈɽ á . m a"),
        (False, "lɛ̃.ɡɥis.tik", "lɛ̃.ɡɥis.tik"),
        (True, "ʔɓaːn˧˩ ŋaː˦ˀ˥", "ʔ ɓ aː n ˧˩ # ŋ aː ˦ˀ˥"),
    ],
)
def test_segment(segment, input_pron, expected_pron):
    config = config_factory(segment=segment)
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "tone, input_pron, expected_pron",
    [
        (True, "aˈɓa.ɽé", "a ˈɓ a . ɽ é"),
        (False, "aˈɓa.ɽé", "a ˈɓ a . ɽ e"),
        (
            False,
            "feɪ̯³⁵ʈ͡ʂaɪ̯³⁵kʰwaɪ̯⁵¹⁻⁵³lɤ⁵¹ʂweɪ̯²¹⁴⁻²¹⁽⁴⁾",
            "f e ɪ̯ ʈ͡ʂ a ɪ̯ kʰ w a ɪ̯ l ɤ ʂ w e ɪ̯",
        ),
        (
            False,
            "kra˨˩.duːk̚˨˩.ton˥˩.kʰaː˩˩˦",
            "k r a . d uː k̚ . t o n . kʰ aː",
        ),
        (False, "aˈt͡ʃe.w⁽ᵝ⁾á", "a ˈt͡ʃ e . w ⁽ᵝ ⁾ a"),
    ],
)
def test_tone(tone, input_pron, expected_pron):
    config = config_factory(tone=tone)
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "error, cut_off_date, word_available_date, expected",
    [
        # Input cut_off_date is invalid.
        (True, _DATE_FUTURE, None, None),
        (True, "not-a-valid_date", None, None),
        # Input cut_off_date is valid.
        (False, None, _DATE_RECENT_PAST, _DATE_TODAY),
        (False, _DATE_TODAY, _DATE_TODAY, _DATE_TODAY),
        (False, _DATE_TODAY, _DATE_RECENT_PAST, _DATE_TODAY),
        (False, _DATE_RECENT_PAST, _DATE_DISTANT_PAST, _DATE_RECENT_PAST),
        (False, _DATE_RECENT_PAST, _DATE_TODAY, _DATE_RECENT_PAST),
    ],
)
def test_cut_off_date(error, cut_off_date, word_available_date, expected):
    if error:
        with pytest.raises(ValueError):
            config_factory(cut_off_date=cut_off_date)
    else:
        config = config_factory(cut_off_date=cut_off_date)
        assert config.cut_off_date == expected


@pytest.mark.parametrize(
    "narrow, ipa_regex, word_in_ipa",
    [(True, _PHONES_REGEX, "[foobar]"), (False, _PHONEMES_REGEX, "/foobar/")],
)
def test_ipa_regex(narrow, ipa_regex, word_in_ipa):
    config = config_factory(narrow=narrow)
    # Make sure we use the correct regex depending on narrow vs broad.
    assert config.ipa_regex == ipa_regex
    # Make sure the IPA extraction by regex works.
    assert re.search(ipa_regex, word_in_ipa).group(1) == "foobar"


@pytest.mark.parametrize(
    "dialect, expected_pron_xpath_selector",
    [
        (
            None,
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  \n"
                "]\n"
            ),
        ),
        (
            "US",
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content" and a[text() = "US"]]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "General American | US",
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content" and a[text() = "General American" or text() = "US"]]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
    ],
)
def test_pron_xpath_selector(dialect, expected_pron_xpath_selector):
    config = config_factory(key="en", dialect=dialect)
    assert config.pron_xpath_selector == expected_pron_xpath_selector


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
def test_american_english_dialect_selection():
    # Pick a word for which Wiktionary has dialect-specified pronunciations
    # for both US and non-US English.
    word = "mocha"
    html_session = requests_html.HTMLSession()
    response = html_session.get(
        _PAGE_TEMPLATE.format(word=word), headers=HTTP_HEADERS
    )
    # Construct two configs to demonstrate the US dialect (non-)selection.
    config_only_us = config_factory(key="en", dialect="US | American English")
    config_any_dialect = config_factory(key="en")
    # Apply each config's XPath selector.
    results_only_us = response.html.xpath(config_only_us.pron_xpath_selector)
    results_any_dialect = response.html.xpath(
        config_any_dialect.pron_xpath_selector
    )
    assert (
        len(results_any_dialect)  # containing both US and non-US results
        > len(results_only_us)  # containing only the US result
        > 0
    )


@pytest.mark.parametrize(
    "expected_language, keys",
    [
        # Languages that the iso639 package can directly handle.
        ("English", {"en", "eng", "English"}),
        ("Spanish", {"spa", "es"}),
        # Languages handled by our own _LANGUAGE_CODES dict.
        ("Greek", {"el", "ell", "gre", "Greek"}),
        ("Slovene", {"sl", "slv", "Slovene", "Slovenian"}),
        # For all Proto-X languages. X may contain hyphens in the middle.
        ("Proto-Germanic", {"Proto-Germanic", "proto-germanic"}),
        ("Proto-Balto-Slavic", {"Proto-Balto-Slavic", "proto-balto-slavic"}),
    ],
)
def test_language(expected_language, keys):
    for key in keys:
        config = config_factory(key=key)
        assert config.language == expected_language, f"key = {key}"
