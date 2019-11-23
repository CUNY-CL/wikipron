"""Word and Pron extraction for Japanese.

Japanese cannot use the default extraction function because Japanese entry page
titles may contain a mix of three scripts: kanji, hiragana, and katakana.
The goal of this extraction function is to grab the corresponding hiragana
form of entries containing kanji and grab entries that are solely katakana.

Japanese entry pages may differ from one another in a variety of ways and
on the whole Japanese entry pages appear to be less consistent in their
underlying HTML than other languages on Wiktionary.
Entry pages may use inconsistent HTML both within a single page
and across pages. For example:
    - In https://en.wiktionary.org/wiki/%E8%84%9A#Japanese the hiragana
    entry under "Etymology 1" is contained within a <b> element that has
    the class: "Jpan form-of lang-ja kana-noun-form-of". The <b> elements
    containing the hirgana under "Etymology 2" lack that class.
    - In https://en.wiktionary.org/wiki/%E6%9C%AC%E5%91%BD#Japanese each
    "Pronunciation" section is numbered and given a numbered "id":
    <span class="mw-headline" id="Pronunciation_1">Pronunciation 1</span>
    while in https://en.wiktionary.org/wiki/%E3%81%82%E3%81%84#Japanese the
    first "Pronunciation" section and its "id" are not numbered,
    but the second is.

This extraction function attempts to grab data from as many entries
as possible, but may not always grab all potential data on a given entry page.
It works by first checking if the page contains hiragana. If it does, it will
grab the first hiragana word and whatever pronunciations are connected to that
hiragana word. If we can't find hiragana, we grab the "headword" and its
connected prons. The assumption is that no kanji is listed without 
corresponding hiragana and thus we shouldn't ever pick up any kanji
if we can't find hiragana.

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
_KATAKANA_WORD_XPATH_SELECTOR = """
//strong[@class = "Jpan headword" and @lang = "ja"]
"""

_PRON_XPATH_SELECTOR = """
{word_to_work_from}/..
        /preceding-sibling::*[1][self::{heading}]
            /preceding-sibling::*[1][self::ul]
                {single_pron}
            

"""

# Assume nothing comes between Pronunciation and word heading
# Assume never more than 2 prons.
# Table may be in the way, just skip that for now.
_PAIR_CHECK_XPATH_SELECTOR = """
{script_to_grab}[
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


# Confirms that the page has a pron and a hiragana form.
def _check_hiragana_pron_pair(request, pair_path, hiragana_path):
    try:
        # Check if hiragana entry on page
        request.html.xpath(hiragana_path)[0]
        return True
    except IndexError:
        return False


# Some pages may not have etymology section.
def _check_etymologies(request):
    count = 0
    for a_element in request.html.xpath(_TOC_ETYMOLOGY_XPATH_SELECTOR):
        count += 1
    return "h4" if count > 1 else "h3"


def _yield_jpn_word(request, pair_check_path, word_path):
    # Iterate through the pair groups, grabbing the
    # first hiragana word in each.
    for pair_group in request.html.xpath(pair_check_path):
        try:
            word_element = pair_group.xpath(
                word_path
            )[0]
        except IndexError:
            # Should not expect to see this printed.
            print('INDEX ERROR')
            return
        word = word_element.text.rstrip(",(")
        yield word


def _check_multi_ul(request, script):
    pron_path = _PRON_XPATH_SELECTOR.format(
        word_to_work_from=script,
        heading=_check_etymologies(request),
        single_pron="[preceding-sibling::*[1][self::ul]]"
    )
    try:
        request.html.xpath(pron_path)[0]
        return True
    except IndexError:
        return False


def _yield_jpn_upper_pron(request, config, script):
    pron_path = _PRON_XPATH_SELECTOR.format(
        word_to_work_from=script,
        heading=_check_etymologies(request),
        single_pron="[preceding-sibling::*[1][self::ul]]"
    )
    try:
        request.html.xpath(pron_path)[0]
    except IndexError:
        return

    for upper_pron_ele in request.html.xpath(pron_path):
        prons = []
        for pron in yield_pron(upper_pron_ele, IPA_XPATH_SELECTOR, config):
            prons.append(pron)
        yield prons


def _yield_jpn_lower_pron(request, config, script):
    pron_path = _PRON_XPATH_SELECTOR.format(
        word_to_work_from=script,
        heading=_check_etymologies(request),
        single_pron=''
    )

    for pron_element in request.html.xpath(pron_path):
        prons = []
        for pron in yield_pron(pron_element, IPA_XPATH_SELECTOR, config):
            prons.append(pron)
        upper_prons = _yield_jpn_upper_pron(request, config, script)
        try:
            prons += next(upper_prons)
        except StopIteration:
            pass
        yield prons


def _combine_word_pron_pairs(words, prons):
    for word in words:
        try:
            associated_prons = next(prons)
        except StopIteration:
            pass
        yield from (zip(itertools.repeat(word), associated_prons))


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    pair_check_xpath_selector = _PAIR_CHECK_XPATH_SELECTOR.format(
        heading=_check_etymologies(request),
        script_to_grab=_HIRAGANA_WORD_XPATH_SELECTOR
    )
    # print('HEADWORD', word)
    if _check_hiragana_pron_pair(
        request, pair_check_xpath_selector, _HIRAGANA_WORD_XPATH_SELECTOR
    ):
        words = _yield_jpn_word(
            request, pair_check_xpath_selector, _HIRAGANA_WORD_XPATH_SELECTOR
        )

        prons = _yield_jpn_lower_pron(request, config, _HIRAGANA_WORD_XPATH_SELECTOR)
    else:
        pair_check_xpath_selector = _PAIR_CHECK_XPATH_SELECTOR.format(
            heading=_check_etymologies(request),
            script_to_grab=_KATAKANA_WORD_XPATH_SELECTOR
        )
        words = _yield_jpn_word(
            request, pair_check_xpath_selector, _KATAKANA_WORD_XPATH_SELECTOR
        )

        prons = _yield_jpn_lower_pron(request, config, _KATAKANA_WORD_XPATH_SELECTOR)
    for vals in _combine_word_pron_pairs(words, prons):
        yield vals
