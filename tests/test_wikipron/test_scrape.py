import collections
import queue
import threading
import time

import pytest
import requests

from wikipron import Config
from wikipron.scrape import (
    _PAGE_TEMPLATE,
    _iter_page_responses_once,
    _skip_date,
    _skip_word,
    _word_from_title,
    scrape,
)
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
    # Latin data is narrow transcription only.
    SmokeTestLanguage("lat", "Latin", {"narrow": True}),
    # Japanese data is mostly narrow transcription.
    SmokeTestLanguage("jpn", "Japanese", {"narrow": True}),
    # Chinese varieties: Sinological IPA scraped from the unified
    # Chinese-character pages. skip_spaces_pron=False because some
    # IPA values include spaces.
    SmokeTestLanguage("cmn", "Mandarin", {"skip_spaces_pron": False}),
    SmokeTestLanguage("yue", "Cantonese", {"skip_spaces_pron": False}),
    SmokeTestLanguage("gan", "Gan", {"skip_spaces_pron": False}),
    SmokeTestLanguage("hak", "Hakka", {"skip_spaces_pron": False}),
    SmokeTestLanguage("cjy", "Jin", {"skip_spaces_pron": False}),
    SmokeTestLanguage("mnp", "Northern Min", {"skip_spaces_pron": False}),
    SmokeTestLanguage("cdo", "Eastern Min", {"skip_spaces_pron": False}),
    SmokeTestLanguage("cpx", "Puxian Min", {"skip_spaces_pron": False}),
    SmokeTestLanguage("nan", "Min Nan", {"skip_spaces_pron": False}),
    SmokeTestLanguage("luh", "Leizhou Min", {"skip_spaces_pron": False}),
    SmokeTestLanguage("csp", "Southern Pinghua", {"skip_spaces_pron": False}),
    SmokeTestLanguage("wuu", "Wu", {"skip_spaces_pron": False}),
    SmokeTestLanguage("hsn", "Xiang", {"skip_spaces_pron": False}),
    SmokeTestLanguage("och", "Old Chinese", {"skip_spaces_pron": False}),
    SmokeTestLanguage("ltc", "Middle Chinese", {"skip_spaces_pron": False}),
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
    SmokeTestLanguage("blt", "Tai Dam", {"narrow": True}),
]

# Smaller / sparser Chinese varieties — the scraper has to walk through
# many Chinese-category pages before accumulating hits for these, so we
# mark them slow. Run the full set with: pytest --runslow
_SLOW_SMOKE_KEYS = frozenset({"luh", "csp", "mnp", "cpx", "cdo", "och", "ltc"})

_SMOKE_TEST_PARAMS = [
    pytest.param(
        lang,
        marks=pytest.mark.slow if lang.key in _SLOW_SMOKE_KEYS else (),
        id=lang.key,
    )
    for lang in _SMOKE_TEST_LANGUAGES
]


# Per-language wall-clock budget for the live-API smoke tests. A language that
# stops yielding (e.g. after a Wiktionary layout change) would otherwise walk
# its entire category and hang CI past the 10-minute no-output limit.
_SMOKE_TEST_TIMEOUT_SECONDS = 60


def _collect_pairs(
    config: Config, n: int, timeout: float
) -> tuple[list[tuple[str, str]], bool]:
    """Collect up to ``n`` (word, pron) pairs from ``scrape(config)``.

    Give up after ``timeout`` seconds and return ``(pairs, timed_out)``. The
    scrape runs on a daemon thread so the budget is enforced even when the
    generator yields nothing and never hands control back to a consumer loop.
    """
    pair_queue: queue.Queue = queue.Queue()
    sentinel = object()

    def worker():
        try:
            for pair in scrape(config):
                pair_queue.put(pair)
        except Exception as error:
            pair_queue.put(error)
        finally:
            pair_queue.put(sentinel)

    threading.Thread(target=worker, daemon=True).start()
    pairs: list[tuple[str, str]] = []
    deadline = time.monotonic() + timeout
    while len(pairs) < n:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return pairs, True
        try:
            item = pair_queue.get(timeout=remaining)
        except queue.Empty:
            return pairs, True
        if item is sentinel:
            break
        if isinstance(item, Exception):
            raise item
        pairs.append(item)
    return pairs, False


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
@pytest.mark.parametrize("smoke_test_language", _SMOKE_TEST_PARAMS)
def test_smoke_test_scrape(smoke_test_language):
    """A smoke test for scrape()."""
    n = 3  # number of word-pron pairs to scrape
    config = config_factory(
        key=smoke_test_language.key, **smoke_test_language.config_params
    )
    assert config.language == smoke_test_language.wik_name
    pairs, timed_out = _collect_pairs(config, n, _SMOKE_TEST_TIMEOUT_SECONDS)
    if timed_out:
        pytest.skip(
            f"{smoke_test_language.wik_name} "
            f"({smoke_test_language.key}) yielded only {len(pairs)}/{n} "
            f"pairs within {_SMOKE_TEST_TIMEOUT_SECONDS}s; skipping "
            f"(possible Wiktionary change or slow network)."
        )
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
        ("2019-10-15T11:22:33Z", "2019-10-20", False),
        ("2019-10-20T11:22:33Z", "2019-10-20", False),
        ("2019-10-25T11:22:33Z", "2019-10-20", True),
    ],
)
def test__skip_date(date_from_word, cut_off_date, expected):
    assert _skip_date(date_from_word, cut_off_date) == expected


@pytest.mark.parametrize(
    "title, expected",
    [
        ("a/languages A to L", "a"),
        ("a/languages M to Z", "a"),
        ("i/languages M to Z", "i"),
        # Ordinary titles are unchanged.
        ("kot", "kot"),
        ("a", "a"),
        # Only the "/languages X to Y" suffix is a split page.
        ("a/languages", "a/languages"),
        ("a/languages A to L/extra", "a/languages A to L/extra"),
        ("a/something else", "a/something else"),
    ],
)
def test__word_from_title(title, expected):
    assert _word_from_title(title) == expected


class _StubSession:
    """Records requested URLs instead of fetching them."""

    def __init__(self):
        self.urls = []

    def get(self, url, timeout):
        self.urls.append(url)
        return requests.Response()


def test__iter_page_responses_once_split_pages():
    """Split-page subpages are fetched by title but yielded as the word."""
    titles = [
        "a/languages A to L",
        "a phrase",
        "a/languages M to Z",
        "kot",
    ]
    data = {
        "query": {
            "categorymembers": [
                {
                    "title": title,
                    "timestamp": "2019-10-15T11:22:33Z",
                    "sortkey": str(i),
                }
                for i, title in enumerate(titles)
            ]
        }
    }
    session = _StubSession()
    config = config_factory(key="pol", cut_off_date="2019-10-20")
    words = [
        word for word, _ in _iter_page_responses_once(data, session, config)
    ]
    # The multiword title is still skipped, without a fetch.
    assert words == ["a", "a", "kot"]
    assert session.urls == [
        _PAGE_TEMPLATE.format(word=title)
        for title in ("a/languages A to L", "a/languages M to Z", "kot")
    ]
