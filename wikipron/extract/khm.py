"""Word and pron extraction for Khmer."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


_IPA_XPATH_SELECTOR = '//span[@class = "IPA" and @lang = "km"]'


def extract_word_pron_khmer(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_pron(request.html, _IPA_XPATH_SELECTOR, config)
    yield from zip(words, prons)
