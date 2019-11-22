import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

# from typing import List

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron, Word, WordPronPair


_HIRAGANA_WORD_XPATH_SELECTOR = '//b[contains(@class, "Jpan form-of lang-ja kana")]'
_KATAKANA_WORD_XPATH_SELECTOR = '//strong[@class = "Jpan headword" and @lang = "ja"]'

_PRON_XPATH_SELECTOR = """
{pron_to_work_from}
    /preceding::{heading}
        /span[@id = "Pronunciation"]
            /following::ul
                //li[
                    (.|span)[sup[a[
                        @title = "Appendix:Japanese pronunciation"
                    ]]]
                    and
                    span[@class = "IPA"]
                ]

"""

# Pretty sure Japanese has always been an <h2>
# Confirms that the page has a pron and
# a hiragana form.
_PAIR_CHECK_XPATH_SELECTOR = """
//{heading}
    /span[@id = "Pronunciation"]
        /following::p
            //b[contains(@class, "Jpan form-of lang-ja kana")]
"""

# If we find more than one etymology, then change <h3> to <h4>
_TOC_ETYMOLOGY_XPATH_SELECTOR = """
//a[@href = "#Japanese"]
  /following-sibling::ul
    /li
      /a
        [starts-with(@href, "#Etymology")]
"""


def _check_jpn_hiragana_pair(request, path):
    try:
        request.html.xpath(path)[0]
        return True
    except IndexError:
        # skip if we don't find a pair
        return False


def _check_etymologies(request):
    count = 0
    for a_element in request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR):
        count += 1
    return "h4" if count > 1 else "h3"


def _yield_jpn_word(request, path):
    for word_element in request.html.xpath(path):
        word = word_element.text.rstrip(",(")
        yield from itertools.repeat(word)


def _yield_jpn_pron(request, path, config):
    for pron_element in request.html.xpath(path):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


# Currently functions as such:
# If we find hiragana on the page, grab it and whatever prons we can
# find that are directly connected to that hiragana word
# If we can't find hiragana, grab the headword and connected prons.
# The assumption is that no kanji is listed without correspoding
# hiragana and thus we shouldn't ever pick up any kanji if we
# can't find hiragana.
# (Does annoyingly pick up one Kanji term because of what I assume
# is 'mislabelled' hiragana - does not cohere with all other hiragana
# html.)
def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    pair_check_xpath_selector = _PAIR_CHECK_XPATH_SELECTOR.format(
        heading=_check_etymologies(request)
    )

    if _check_jpn_hiragana_pair(request, pair_check_xpath_selector):
        words = _yield_jpn_word(request, _HIRAGANA_WORD_XPATH_SELECTOR)
        pron_xpath_selector = _PRON_XPATH_SELECTOR.format(
            pron_to_work_from=_HIRAGANA_WORD_XPATH_SELECTOR,
            heading=_check_etymologies(request)
        )
        prons = _yield_jpn_pron(request, pron_xpath_selector, config)
    else:
        words = _yield_jpn_word(request, _KATAKANA_WORD_XPATH_SELECTOR)
        pron_xpath_selector = _PRON_XPATH_SELECTOR.format(
            pron_to_work_from=_KATAKANA_WORD_XPATH_SELECTOR,
            heading=_check_etymologies(request)
        )
        prons = _yield_jpn_pron(request, pron_xpath_selector, config)
    yield from zip(words, prons)
