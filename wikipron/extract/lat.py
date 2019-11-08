# TODO: More documentation.

"""Word and pron extraction for Latin."""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

from typing import List


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron, Word, WordPronPair


_TOC_ETYMOLOGY_XPATH_SELECTOR = """
//a[@href = "#Latin"]
  /following-sibling::ul
    /li
      /a
        [starts-with(@href, "#Etymology")]
"""

_PRON_XPATH_TEMPLATE = """
//h3[span[@class = "mw-headline" and @id = "{etymology_tag}"]]
  /following-sibling::ul[1]
"""

_WORD_XPATH_TEMPLATE = """
//h3[span[@class = "mw-headline" and @id = "{etymology_tag}"]]
  /following-sibling::p
    /strong[@class = "Latn headword" and @lang = "la"][1]
"""


def _get_etymology_tags(request: requests.Response) -> List[str]:
    tags = []
    for a_element in request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR):
        tag = a_element.attrs["href"].lstrip("#")
        tags.append(tag)
    return tags


def _get_latin_word(request: requests.Response, etymology_tag: str) -> "Word":
    word_xpath_selector = _WORD_XPATH_TEMPLATE.format(
        etymology_tag=etymology_tag
    )
    word_element = request.html.xpath(word_xpath_selector)[0]
    # FIXME: Why do many words have " ("?
    return word_element.text


def _yield_latin_pron(
    request: requests.Response, config: "Config", etymology_tag: str
) -> "Iterator[Pron]":
    pron_xpath_selector = _PRON_XPATH_TEMPLATE.format(
        etymology_tag=etymology_tag
    )
    for pron_element in request.html.xpath(pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_latin(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # For Latin, we don't use the title word from the Wiktionary page,
    # because it never has macrons (necessary for Latin vowel length).
    # We will get the word from each "Etymology" section.
    word = None
    etymology_tags = _get_etymology_tags(request)
    for etymology_tag in etymology_tags:
        word = _get_latin_word(request, etymology_tag)
        words = itertools.repeat(word)
        prons = _yield_latin_pron(request, config, etymology_tag)
        yield from zip(words, prons)
