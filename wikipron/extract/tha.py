"""Word and pron extraction for Thai."""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, WordPronPair


def extract_word_pron_thai(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(config.casefold(word))
    prons = yield_pron(request.html, IPA_XPATH, config)
    yield from zip(words, prons)
