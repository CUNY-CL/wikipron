import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR
from wikipron.extract.default import _yield_phn

# from typing import List

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron, Word, WordPronPair


# This is for grabbing forms listed as hiragana on pages.
_WORD_XPATH_SELECTOR = '//b[contains(@class, "Jpan form-of lang-ja kana")]'


_PAIR_XPATH_SELECTOR = """


"""


def _yield_jpn_word(request, config):
    # print('TRYING')
    # Currently only selects hiragana
    # And obviously will only grab one at a time.
    for word_element in request.html.xpath(_WORD_XPATH_SELECTOR):
        word = word_element.text.rstrip(",")
        print("WORD", word)
        yield from itertools.repeat(config.casefold(word))


def _yield_jpn_pron():
    pass


def extract_word_pron_jpn(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    # print('HEADWORD', word)
    words = _yield_jpn_word(request, config)
    # Only want to grab a pron when we have the hiragana
        # Actually this probably doesn't matter, maybe we grab prons
        # But with no words, zip yields nothing
        # and it appears nothing gets printed.
            # (Still quite inefficient though)
    # I think the way this currently works, we will repeatedly apply whatever
    # word we have collected to whatever prons we have collected.
    # So what if we have 1 pron and 2 words? We will only zip 1 thing...
    prons = _yield_phn(request, config)
    yield from zip(words, prons)
