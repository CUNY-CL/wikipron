"""Word and pron extraction for Shan, language spoken in Myanmar."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron

_IPA_XPATH_SELECTOR = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:Shan pronunciation (page does not exist)"
    or
    @title = "wikipedia:Shan phonology"
  ]]]
  and
  span[@class = "IPA"]
]
"""

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


def extract_word_pron_shan(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_pron(request.html, _IPA_XPATH_SELECTOR, config)
    yield from zip(words, prons)
