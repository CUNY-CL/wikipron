"""Word and pron extraction for Lü.

Customized extractor for Lü has to deal with wrong titles (see the
original report here: https://github.com/CUNY-CL/wikipron/issues/86).
"""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.default import yield_pron

_IPA_XPATH_SELECTOR = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:Lü pronunciation (page does not exist)"
    or
    @title = "wikipedia:Lü phonology"
  ]]]
  and
  span[contains(@class, "IPA")]
]
"""

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


def extract_word_pron_lu(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_pron(request.html, _IPA_XPATH_SELECTOR, config)
    yield from zip(words, prons)
