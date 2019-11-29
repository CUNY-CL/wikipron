"""Word and Pron extraction for Japanese.

Japanese cannot use the default extraction function because Japanese entry page
titles may contain a mix of three scripts: kanji, hiragana, and katakana.
The goal of this extraction function is to grab the corresponding hiragana
form of entries containing kanji and grab entries that are solely katakana
or hiragana.

Japanese entry pages may differ from one another in a variety of ways and
on the whole Japanese entry pages appear to be less consistent in their
underlying HTML than other languages on Wiktionary.
Entry pages may use inconsistent HTML both within a single page
and across pages.

This extraction function attempts to grab data from as many entries
as possible, but may not always grab all potential data on a given entry page.
To reduce the complexity of scraping the sometimes widely different Japanese
entry pages, this extraction function attempts to target "pairs" of words
and pronunciations. It thus only grabs a word if it can find a "local"
pronunciation entry on the page, and only grabs a pronunciation if it can
find a "local" word on the page.

The reason for not indiscriminately scraping each entry page for words or
pronunciations that share a class is because of pages like:
https://en.wiktionary.org/wiki/%E8%84%9A#Japanese
https://en.wiktionary.org/wiki/%E5%B9%B3%E5%9C%B0#Japanese
Where not all "Etymologies" contain pronunciations and not all "Etymologies"
(as in the first link) are listed as missing or incomplete. Scraping
indiscriminately may lead to matching words and pronunciations that are not
meant to be together.
"""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron, Word, WordPronPair


_HIRAGANA_WORD_XPATH_SELECTOR = """
//b[contains(@class, "Jpan form-of lang-ja kana")]
"""

# Will also catch some purely hiragana entries and
# hiragana entries that do not use the above HTML despite
# being in the same position as them on the page.
_KATAKANA_WORD_XPATH_SELECTOR = """
//strong[@class = "Jpan headword" and @lang = "ja"]
"""

# Works upward from the word to its pronunciation
_PRON_XPATH_SELECTOR = """
{word_to_work_from}/..
        /preceding-sibling::*[1][self::{heading}]
            /preceding-sibling::*[1][self::ul]
                {second_ul}
"""

# Assumes never more than two <ul>'s containing IPA pronunciations.
# There may be an intervening <table>, <div>, or <h4>
# between the "Pronunciation" heading and the word.
# The selector as written does not handle skipping those.
_PAIR_CHECK_XPATH_SELECTOR = """
{word_to_grab}[
    ..
        /preceding-sibling::*[1][self::{heading}]
            /preceding-sibling::*[1][self::ul][
                (. | preceding-sibling::*[1][self::ul])
                /preceding-sibling::*[1][self::{heading}][
                    span[contains(@id, "Pronunciation")]
                ]
            ]

]
"""

# Check for more than one etymology for the same reason as in lat.py
# If there is more than one etymology, the headings get shifted down a level.
_TOC_ETYMOLOGY_XPATH_SELECTOR = """
//a[@href = "#Japanese"]
  /following-sibling::ul
    /li
      /a
        [starts-with(@href, "#Etymology")]
"""


# Some pages may not have etymology section.
def _check_etymologies(request: requests.Response):
    count = len(request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR))
    return "h4" if count > 1 else "h3"


# Check if hiragana entry on page
def _check_hiragana(request: requests.Response, hiragana_path: str):
    try:
        request.html.xpath(hiragana_path)[0]
        return True
    except IndexError:
        return False


# The extraction functions below speak to some of the complexity
# involved with Japanese. In other languages, on each entry page,
# we are always mapping prons to a single word. In Japanese an entry page
# may contain multiple prons that need to be mapped to multiple words.
# This extraction function avoids some of this complexity by always only
# taking one word for each word-pron pairing we find on an entry page,
# but it does this for as many pairings as we can find on the entry page.
def _yield_jpn_word(
    request: requests.Response, pair_check_path: str, word_path: str
) -> "Iterator[Word]":
    # Iterate through the pair groups, grabbing the
    # first hiragana word in each.
    for pair_group in request.html.xpath(pair_check_path):
        try:
            word_element = pair_group.xpath(word_path)[0]
        except IndexError:
            return
        word = word_element.text.rstrip(",(")
        yield word


# Japanese "Pronunciation" headers are most often sibling to a <ul> containing
# an IPA transcription. There may also be a <ul> sibling to that <ul> which
# contains a second IPA transcription (though second transcriptions are not
# always contained within a separate <ul>). The only way I could work in
# grabbing the transcriptions in both <ul>'s with my attempt to connect
# words and prons "locally" - by moving stepwise from the word to the pron -
# was to update _PRON_XPATH_SELECTOR with the second <ul> and
# run a separate request.
def _yield_jpn_upper_pron(
    request: requests.Response, config: "Config",
    word_target: str, heading: str
) -> "Iterator[Pron]":
    pron_path = _PRON_XPATH_SELECTOR.format(
        word_to_work_from=word_target,
        heading=heading,
        second_ul="[preceding-sibling::*[1][self::ul]]",
    )
    try:
        request.html.xpath(pron_path)[0]
    except IndexError:
        return

    for upper_pron_ele in request.html.xpath(pron_path):
        prons = list(yield_pron(upper_pron_ele, IPA_XPATH_SELECTOR, config))
        yield prons


def _yield_jpn_lower_pron(
    request: requests.Response, config: "Config",
    word_target: str, heading: str
) -> "Iterator[Pron]":
    pron_path = _PRON_XPATH_SELECTOR.format(
        word_to_work_from=word_target,
        heading=heading,
        second_ul="",
    )
    for pron_element in request.html.xpath(pron_path):
        prons = list(yield_pron(pron_element, IPA_XPATH_SELECTOR, config))
        upper_prons = _yield_jpn_upper_pron(
            request, config, word_target, heading
        )
        # There is a possible, though seemingly unlikely, undesirable side
        # effect of this approach. This could potentially match a second
        # "upper" pronunciation (most likely in a second Etymology) and
        # append it to the "lower" pronunciations yielded from the first
        # Etymology. Or append the "upper" pronunciation of the first
        # Etymology to the "lower" pronunciation of the second Etymology, etc.
        # Fortunately entries with multiple <ul>'s and multiple
        # etymologies are exceedingly rare. I'm not sure I've seen any.
        try:
            prons += next(upper_prons)
        except StopIteration:
            # Did not find a second <ul>
            pass
        # Yielding here because we don't want to collect all pronunciation
        # entries on a page at the same time. Doing so would make it difficult
        # to connect words to their prons appropriately. We only want to grab
        # the prons that are linked to the word we have scraped.
        yield prons


def _combine_word_pron_pairs(
    words: "Iterator[Word]", prons: "Iterator[Pron]"
) -> "Iterator[WordPronPair]":
    for word in words:
        try:
            associated_prons = next(prons)
        # With the selectors we use, we should never hit this except block.
        # A StopIteration error could only occur if our selectors told us
        # there was a word-pron pair on the page and we grabbed
        # the word associated with the pron, but could not grab the pron
        # associated with the word. This is possible if an entry page
        # has a "Pronunciation" heading that is sister to a <ul>
        # containing no span[@class = "IPA"] elements. This try-except
        # block therefore handles a theoretically possible error that
        # would stop the scrape.
        except StopIteration:
            continue
        yield from zip(itertools.repeat(word), associated_prons)


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    if _check_hiragana(request, _HIRAGANA_WORD_XPATH_SELECTOR):
        xpath_selector = _HIRAGANA_WORD_XPATH_SELECTOR
    else:
        xpath_selector = _KATAKANA_WORD_XPATH_SELECTOR

    heading = _check_etymologies(request)
    pair_check_xpath_selector = _PAIR_CHECK_XPATH_SELECTOR.format(
        heading=heading,
        word_to_grab=xpath_selector,
    )
    words = _yield_jpn_word(
        request, pair_check_xpath_selector, xpath_selector
    )
    prons = _yield_jpn_lower_pron(
        request, config, xpath_selector, heading
    )
    for word, pron in _combine_word_pron_pairs(words, prons):
        yield word, pron
