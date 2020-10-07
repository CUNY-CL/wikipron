"""Word and pron extraction for Lü.

Customized extractor for Lü has to deal with wrong titles (see the
original report here: https://github.com/kylebgorman/wikipron/issues/86).
"""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron

_IPA_XPATH_SELECTOR = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:Lü pronunciation (page does not exist)"
    or
    @title = "wikipedia:Lü phonology"
  ]]]
  and
  span[@class = "IPA"]
]
"""

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, WordPronPair


def extract_word_pron_lu(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_pron(request.html, _IPA_XPATH_SELECTOR, config)
    yield from zip(words, prons)
