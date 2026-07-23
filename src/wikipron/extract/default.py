"""Default word and pron extraction."""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.core import yield_pron

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# Direct-child (not descendant) so a general-outer <li> does not also scoop the
# IPA of accent variants nested in sub-<li>s; each variant is matched on its
# own line. Matches the base selector, which likewise keys on a direct-child
# IPA.
IPA_XPATH_SELECTOR = 'span[contains(@class, "IPA")]'


def _yield_phn(request: HTMLResponse, config: "Config") -> "Iterator[str]":
    for pron_element in request.html.xpath(config.pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_default(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = _yield_phn(request, config)
    yield from zip(words, prons)
