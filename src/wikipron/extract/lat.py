"""Word and pron extraction for Latin.

As of writing (November 2019), Latin cannot use the default extraction
function, which uses the Wiktionary entry page title as the graphemes.
Latin uses the macrons orthographically (for vowel length),
but the Wiktionary entry page titles never have them.
The correct orthographic form is available from within the entry page.

In the underlying HTML, the Latin entry pages are in two different forms.

1. Because the orthographic distinction by macrons is collapsed,
   a Latin entry page organizes the "homographs" in terms of "Etymologies".
   Each etymology has its own (correct) orthographic form and pronunciations:

   <h3>
       <span class="mw-headline" id = "Etymology_1">Etymology 1</span>
   </h3>
   <p>
       <!-- The orthographic form we want. -->
       <strong class="Latn headword" lang="la">...</strong>
   </p>
   <ul>
       <!-- The pronunciation we want. -->
       <span class="IPA">...</span>
   </ul>

2. For entries that don't have "Etymology" sections, the underlying HTML
   structure is very similar, with everything moved up one level,
   from <h3> for an etymology to <h2> for Latin.

   <h2>
       <span class="mw-headline" id = "Latin">Latin</span>
   </h2>
   <p>
       <!-- The orthographic form we want. -->
       <strong class="Latn headword" lang="la">...</strong>
   </p>
   <ul>
       <!-- The pronunciation we want. -->
       <span class="IPA">...</span>
   </ul>
"""

import itertools
import typing
from typing import List

import requests_html

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


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
    {dialect_selector}
"""

_PRON_WITH_DIALECT_XPATH_SELECTOR_TEMPLATE = """
//li[
  sup[a[@title = "Appendix:Latin pronunciation"]]
  and
  span[@class = "IPA"]
  and
  span[@class = "ib-content" and a[{dialects_text}]]
]
"""

_WORD_XPATH_TEMPLATE = """
//{heading}[span[@class = "mw-headline" and @id = "{tag}"]]
  /following-sibling::p
    /strong[@class = "Latn headword" and @lang = "la"][1]
"""


def _get_tags(request: requests_html) -> List[str]:
    """Extract the Latin Etymology ID tags from the table of contents."""
    tags = []
    for a_element in request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR):
        tag = a_element.attrs["href"].lstrip("#")
        tags.append(tag)
    # If the entry doesn't have etymology sections, we target the "Latin"
    # language section directly.
    if not tags:
        tags = ["Latin"]
    return tags


def _yield_latin_word(request: requests_html, tag: str) -> "Iterator[str]":
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
    request: requests_html, config: "Config", tag: str
) -> "Iterator[str]":
    heading = "h2" if tag == "Latin" else "h3"
    if config.dialect:
        dialect_selector = _PRON_WITH_DIALECT_XPATH_SELECTOR_TEMPLATE.format(
            dialects_text=" or ".join(
                f'text() = "{d.strip()}"' for d in config.dialect.split("|")
            )
        )
    else:
        dialect_selector = (
            '[descendant::a[@title = "Appendix:Latin pronunciation"]]'
        )
    pron_xpath_selector = _PRON_XPATH_TEMPLATE.format(
        heading=heading, tag=tag, dialect_selector=dialect_selector
    )
    for pron_element in request.html.xpath(pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_latin(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    # For Latin, we don't use the title word from the Wiktionary page,
    # because it never has macrons (necessary for Latin vowel length).
    # We will get the word from each "Etymology" section within the page.
    tags = _get_tags(request)
    for tag in tags:
        # The words and prons are extracted from the same request response but
        # separately (so with somewhat overlapping XPath selectors), because
        # the targeted words and prons are at the same hierarchical level in
        # the underlying HTML, and may be separated by other irrelevant sibling
        # tags. Trying to get both words and prons while walking through
        # the request response only once might be technically possible,
        # but the result would be less maintainable.
        words = _yield_latin_word(request, tag)
        prons = _yield_latin_pron(request, config, tag)
        yield from zip(words, prons)
