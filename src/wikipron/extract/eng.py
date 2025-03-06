"""Word and pron extraction for English."""

import itertools
import typing

import requests_html
import re

from wikipron.extract.default import yield_pron

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


IPA_XPATH_SELECTOR = '//span[@class = "IPA"]'


def yield_eng_pron(
    request: requests_html, config: "Config"
) -> "Iterator[str]":
    for li_container in request.html.xpath(config.pron_xpath_selector):
        for pron in yield_pron(li_container, IPA_XPATH_SELECTOR, config):
            # replaces the trilled /r/ with /ɹ/
            pron = pron.replace("r", "ɹ")
            # replaces word final /əɹ/ with /ɚ/
            pron = re.sub(r"ə ?ɹ$", "ɚ", pron)
            yield pron


def extract_word_pron_eng(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_eng_pron(request, config)
    yield from zip(words, prons)
