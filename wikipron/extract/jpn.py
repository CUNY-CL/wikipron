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


def extract_jpn_pron(request, config):
    # Just want to grab the first transcription.
    # Will encounter words that have no transcription.
    pron_element = request.html.xpath(config.pron_xpath_selector, first=True)
    if pron_element:
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_jpn_word(word, request):
    word_element = request.html.xpath(_WORD_XPATH_SELECTOR, first=True)
    if word_element:
        # Remove text within title element for empty links
        word = word_element.rstrip(" (page does not exist)")

    yield word


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # print('SCRAPING', word)
    new_word = extract_jpn_word(word, request)
    prons = extract_jpn_pron(request, config)
    yield from zip(new_word, prons)
