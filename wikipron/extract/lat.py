"""Word and pron extraction for Latin."""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron

xpath = """

Table of contents:
<div id="toc class="toc">

Go to Latin:
<a href="#Latin">

Find the following sibling <ul>

Within this <ul>
find the <a href="#Etymology*"> tags, where * could be _1, _1_2, _7, etc.

For each <span class="mw-headline" id="Etymology*">:
Find the following two things before the next <span class="mw-headline" id="Etymology*">
1. all occurrences of <span class="IPA">....</span>
2. <strong class="Latn headword" lang="la">...</strong> (there should be only one)
    

"""


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, WordPronPair


def extract_word_pron_latin(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat("foo")
    prons = itertools.repeat("bar")
    yield from zip(words, prons)
