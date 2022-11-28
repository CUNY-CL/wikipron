"""Word and pron extraction for Tai Dam."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron

_PRON_XPATH_SELECTOR_TEMPLATE = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:{language} pronunciation (page does not exist)"
    or
    @title = "wikipedia:{language} phonology"
  ]]]
  and
  span[@class = "IPA"]
]
"""

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


def extract_word_pron_blt(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    selector = _PRON_XPATH_SELECTOR_TEMPLATE.format(language=config.language)
    prons = yield_pron(request.html, selector, config)
    yield from zip(words, prons)
