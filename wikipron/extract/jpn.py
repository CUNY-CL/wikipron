"""Simplified word and pron extraction for Japanese

This extraction function attempts to target Japanese orthographic entries
that are composed solely of kana. As of March 2020, the kana variant of a
headword containing kanji is generally found inside an <rt> element
that is itself contained with the <strong> element containing
the headword.

As written, this extraction function will only target one orthographic
entry on a given page and only extracts pronunciations from within the
first Pronunciation <li> it finds. This was done to avoid the complexity
of having to correctly match words to pronunciations when varying amounts
of each are given.
"""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, Pron, WordPronPair


# Grab title of <a> because of possibly split kana.
_WORD_XPATH_SELECTOR = """
    //strong[@class="Jpan headword"]
        //rt
          //a/@title
"""


def yield_jpn_pron(
    request: requests.Response, config: "Config"
) -> "Iterator[Pron]":
    # For simplicity, just want to grab the first transcription.
    # Will encounter words that have no transcription.
    pron_element = request.html.xpath(config.pron_xpath_selector, first=True)
    if pron_element:
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def yield_jpn_word(
    word: "Word", request: requests.Response
) -> "Iterator[Word]":
    # Again for simplicity, only grabbing first "sub"-word.
    word_element = request.html.xpath(_WORD_XPATH_SELECTOR, first=True)
    if word_element:
        # Remove text within title element for empty links
        word = word_element.rstrip(" (page does not exist)")

    yield from itertools.repeat(word)


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # If we can't find a kana alternative, then the headword
    # must itself be kana.
    replacement_word = yield_jpn_word(word, request)
    prons = yield_jpn_pron(request, config)
    yield from zip(replacement_word, prons)
