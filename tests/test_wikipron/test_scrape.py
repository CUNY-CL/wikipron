import collections

import pytest

from wikipron.scrape import scrape, _skip_word, _skip_date
from wikipron.extract import EXTRACTION_FUNCTIONS

from . import can_connect_to_wiktionary, config_factory


SmokeTestLanguage = collections.namedtuple(
    "SmokeTestLanguage", ("key", "wik_name", "config_params")
)
SmokeTestLanguage.__doc__ = """
Represents a language to run a smoke test on.

Parameters
----------
key : str
    An ISO 639 code or language name.
wik_name : str
    The language name used by Wiktionary.
config_params : dict
    Parameters for the Config class.
"""

_SMOKE_TEST_LANGUAGES = [
    SmokeTestLanguage("eng", "English", {}),
    # Test that 'sup[a[@title = "wikipedia:Slovak phonology"]]' works.
    SmokeTestLanguage("slk", "Slovak", {}),
    # Test that the extra "span" layer for Korean is handled.
    # Korean data is mostly narrow transcription only.
    SmokeTestLanguage("kor", "Korean", {"narrow": True}),
    SmokeTestLanguage("khb", "Lü", {}),
    SmokeTestLanguage("khm", "Khmer", {}),
    SmokeTestLanguage("shn", "Shan", {}),
    SmokeTestLanguage("tha", "Thai", {}),
    SmokeTestLanguage("lat", "Latin", {}),
    # Japanese data is mostly narrow transcription.
    SmokeTestLanguage("jpn", "Japanese", {"narrow": True}),
    SmokeTestLanguage("cmn", "Chinese", {"skip_spaces_pron": False}),
    # Vietnamese data is mostly narrow transcription.
    SmokeTestLanguage(
        "vie",
        "Vietnamese",
        {
            "narrow": True,
            "skip_spaces_word": False,
            "skip_spaces_pron": False,
        },
    ),
    SmokeTestLanguage("yue", "Cantonese", {"skip_spaces_pron": False}),
    SmokeTestLanguage("nan", "Min Nan", {"skip_spaces_pron": False}),
    SmokeTestLanguage("blt", "Tai Dam", {"narrow": True}),
]


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
@pytest.mark.parametrize("smoke_test_language", _SMOKE_TEST_LANGUAGES)
def test_smoke_test_scrape(smoke_test_language):
    """A smoke test for scrape()."""
    n = 10  # number of word-pron pairs to scrape
    config = config_factory(
        key=smoke_test_language.key, **smoke_test_language.config_params
    )
    assert config.language == smoke_test_language.wik_name
    pairs = []
    for i, (word, pron) in enumerate(scrape(config)):
        if i >= n:
            break
        pairs.append((word, pron))
    assert len(pairs) == n
    assert all(word and pron for (word, pron) in pairs)


def test_special_languages_covered_by_smoke_test():
    """All languages handled by wikipron.extract must have a smoke test."""
    special_languages = {lang for lang in EXTRACTION_FUNCTIONS.keys()}
    smoke_test_languages = {lang.wik_name for lang in _SMOKE_TEST_LANGUAGES}
    assert special_languages.issubset(smoke_test_languages), (
        "These languages must also be included in the smoke test: "
        f"{special_languages - smoke_test_languages}"
    )


@pytest.mark.parametrize(
    "word, skip_spaces, expected",
    [
        ("foobar", True, False),
        ("a phrase", True, True),
        ("hyphen-ated", True, True),
        ("prefix-", True, True),
        ("-suffix", True, True),
        ("hasdigit2", False, True),
        ("a phrase", False, False),
        ("foobar", True, False),
    ],
)
def test__skip_word(word, skip_spaces, expected):
    assert _skip_word(word, skip_spaces) == expected


@pytest.mark.parametrize(
    "date_from_word, cut_off_date, expected",
    [
        ("2019-10-15", "2019-10-20", False),
        ("2019-10-20", "2019-10-20", False),
        ("2019-10-25", "2019-10-20", True),
    ],
)
def test__skip_date(date_from_word, cut_off_date, expected):
    assert _skip_date(date_from_word, cut_off_date) == expected
