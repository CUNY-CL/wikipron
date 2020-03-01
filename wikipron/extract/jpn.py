"""Simplified word and pron extraction for Japanese"""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, Pron, WordPronPair


# Grab title of a element because of possibly split hiragana.
_WORD_XPATH_SELECTOR = """
    //strong[@class="Jpan headword"]
        //rt
          //a/@title
"""


def yield_jpn_pron(request, config):
    # Just want to grab the first transcription.
    pron_element = request.html.xpath(config.pron_xpath_selector)[0]
    yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def yield_jpn_word(word, request):
    word_element_list = request.html.xpath(_WORD_XPATH_SELECTOR)
    if len(word_element_list):
        # Remove text for empty links
        word = word_element_list[0].rstrip(" (page does not exist)")
        yield word
    else:
        yield(word)


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # print('SCRAPING', word)
    words = yield_jpn_word(word, request)
    prons = yield_jpn_pron(request, config)
    yield from zip(words, prons)
