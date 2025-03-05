"""Word and pron extraction for English."""

import itertools
import typing

import requests_html
import re

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


_PRON_XPATH_TEMPLATE = """
    //div[@class="vsHide"]
        //ul
            //li[(a[@title="w:English"])]
"""


def yield_eng_pron(
    request: requests_html, config: "Config"
) -> "Iterator[str]":
    for li_container in request.html.xpath(_PRON_XPATH_TEMPLATE):
        for pron in yield_pron(li_container, IPA_XPATH_SELECTOR, config):
            pron = pron.replace("r", "ɹ")
            pron = re.sub(r"ə ɹ$", "ɚ", pron)
            yield pron


def extract_word_pron_eng(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_eng_pron(request, config)
    yield from zip(words, prons)
