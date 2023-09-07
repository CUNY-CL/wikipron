"""Word and pron extraction for (Mandarin) Chinese."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# Select pron from within this li
_PRON_XPATH_TEMPLATE = """
    //div[@class="vsHide"]
        //ul
            //li[(a[@title="w:Mandarin Chinese"])]
"""


def yield_cmn_pron(
    request: requests_html, config: "Config"
) -> "Iterator[str]":
    for li_container in request.html.xpath(_PRON_XPATH_TEMPLATE):
        yield from yield_pron(li_container, IPA_XPATH_SELECTOR, config)


def extract_word_pron_cmn(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_cmn_pron(request, config)
    yield from zip(words, prons)
