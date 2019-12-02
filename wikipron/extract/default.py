"""Default word and pron extraction."""

import itertools
import typing

import requests

from wikipron.extract.core import yield_pron


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron, Word, WordPronPair


IPA_XPATH_SELECTOR = '//span[@class = "IPA"]'


def _yield_phn(
    request: requests.Response, config: "Config"
) -> "Iterator[Pron]":
    for pron_element in request.html.xpath(config.pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_default(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = _yield_phn(request, config)
    yield from zip(words, prons)
