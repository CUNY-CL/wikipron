"""Word and pron extraction for Thai."""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.default import yield_pron

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# Thai pronunciations now render inside a <table>: the IPA <span> lives in a
# <td> whose row's <th> carries the pronunciation-appendix/phonology anchor.
# Restrict to those rows so we scrape Thai only (other languages render
# Thai-script IPA on the same page).
_THAI_IPA_XPATH_SELECTOR = (
    "//tr[.//sup/a["
    '@title = "Appendix:Thai pronunciation" or '
    '@title = "wikipedia:Thai phonology" or '
    '@title = "w:Thai language"]]'
    '//span[contains(@class, "IPA")]'
)


def extract_word_pron_thai(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_pron(request.html, _THAI_IPA_XPATH_SELECTOR, config)
    yield from zip(words, prons)
