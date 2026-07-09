"""Word and pron extraction for English."""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

import re

from wikipron.extract.default import yield_pron

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# Direct-child (not descendant) so a general-outer <li> does not also scoop the
# IPA of accent variants nested in sub-<li>s; each variant is matched on its
# own line. Matches the base selector, which likewise keys on a direct-child
# IPA.
IPA_XPATH_SELECTOR = 'span[contains(@class, "IPA")]'


def yield_eng_pron(request: HTMLResponse, config: "Config") -> "Iterator[str]":
    for li_container in request.html.xpath(config.pron_xpath_selector):
        for pron in yield_pron(li_container, IPA_XPATH_SELECTOR, config):
            # Replaces the trilled /r/ with /ɹ/.
            pron = pron.replace("r", "ɹ")
            # Replaces word-final /əɹ/ with /ɚ/.
            pron = re.sub(r"ə ?ɹ$", "ɚ", pron)
            yield pron


def extract_word_pron_eng(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_eng_pron(request, config)
    yield from zip(words, prons)
