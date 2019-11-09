# TODO: Update documentation as well as names of functions and variables.

"""Word and pron extraction for Latin.

As of writing (November 2019), Latin cannot use the default extraction
function because of the following:

1. The default extraction function uses the Wiktionary entry page title
   as the graphemes. Latin uses the macrons orthographically (for vowel
   length), but the Wiktionary entry page titles never have them.
2. Relatedly, because the orthographic distinction by macrons is collapsed,
   a Latin entry page organizes the "homographs" in terms of "Etymologies".
   Each etymology has its own (correct) orthographic form and pronunciations.

The solution for Latin is to go through each "Etymology" and extract the
word and pronunciation at this level.
"""

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
//{heading}[span[@class = "mw-headline" and @id = "{tag}"]]
  /following-sibling::ul[1]
"""

_WORD_XPATH_TEMPLATE = """
//{heading}[span[@class = "mw-headline" and @id = "{tag}"]]
  /following-sibling::p
    /strong[@class = "Latn headword" and @lang = "la"][1]
"""


def _get_etymology_tags(request: requests.Response) -> List[str]:
    """Extract the Latin Etymology ID tags from the table of contents."""
    tags = []
    for a_element in request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR):
        tag = a_element.attrs["href"].lstrip("#")
        tags.append(tag)
    if not tags:
        tags = ["Latin"]
    return tags


def _yield_latin_word(
    request: requests.Response, tag: str
) -> "Iterator[Word]":
    heading = "h2" if tag == "Latin" else "h3"
    word_xpath_selector = _WORD_XPATH_TEMPLATE.format(heading=heading, tag=tag)
    try:
        # Within each "Etymology", we expect exactly one word to extract,
        # and therefore we don't loop through `request.html.xpath`.
        word_element = request.html.xpath(word_xpath_selector)[0]
    except IndexError:
        # Skip if this "Etymology" doesn't have a word.
        return
    # Unfortunately, word_element.text is sometimes incorrectly appended with
    # " (" or " (+" as the beginning of some morphological information.
    word = word_element.text.rstrip(" (+")
    yield from itertools.repeat(word)


def _yield_latin_pron(
    request: requests.Response, config: "Config", tag: str
) -> "Iterator[Pron]":
    heading = "h2" if tag == "Latin" else "h3"
    pron_xpath_selector = _PRON_XPATH_TEMPLATE.format(heading=heading, tag=tag)
    for pron_element in request.html.xpath(pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_latin(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # For Latin, we don't use the title word from the Wiktionary page,
    # because it never has macrons (necessary for Latin vowel length).
    # We will get the word from each "Etymology" section within the page.
    word = None  # noqa: F841
    etymology_tags = _get_etymology_tags(request)
    for etymology_tag in etymology_tags:
        # The words and prons are extracted from the same request response but
        # separately (so with somewhat overlapping XPath selectors), because
        # the targeted words and prons are at the same hierarchical level in
        # the underlying HTML, and may be separated by other irrelevant sibling
        # tags. Trying to get both words and prons while walking through
        # the request response only once might be technically possible,
        # but the result would be less maintainable.
        words = _yield_latin_word(request, etymology_tag)
        prons = _yield_latin_pron(request, config, etymology_tag)
        yield from zip(words, prons)
