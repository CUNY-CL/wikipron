"""Word and pron extraction for Polish.

Polish uses the default extraction, except that pronunciation lines labelled
"Middle Polish" (16th-18th c.) are skipped. English Wiktionary gives many
Polish entries such a line next to the modern one, e.g. for ``który``:

    <li>IPA(key): <span class="IPA">/ˈktu.rɘ/</span></li>
    <li>
        <span class="usage-label-accent">
            (<span class="ib-content label-content">
                <a title="w:Middle Polish">Middle Polish</a>
            </span>)
        </span>
        IPA(key): <span class="IPA">/ˈkto.rɨ/</span>
    </li>

Without this filter, the Middle Polish forms (``k t o r ɨ``) end up in the
TSV as ordinary Polish pronunciations, with no label.

A line is skipped if the label is on the line itself or on an enclosing
``<li>``. A label on a nested sub-``<li>`` does not cause the outer line to
be skipped.
"""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.core import yield_pron
from wikipron.extract.default import IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


_MIDDLE_POLISH_LABEL = (
    'span[contains(@class, "usage-label-accent")]'
    '//a[@title = "w:Middle Polish"]'
)
# Evaluated on a pronunciation <li>/<p> element: selects the element itself
# if it or an enclosing <li> carries the Middle Polish label as a direct
# child, and nothing otherwise.
_MIDDLE_POLISH_XPATH_SELECTOR = (
    f"self::*[{_MIDDLE_POLISH_LABEL} or ancestor::li/{_MIDDLE_POLISH_LABEL}]"
)


def _yield_phn(request: HTMLResponse, config: "Config") -> "Iterator[str]":
    for pron_element in request.html.xpath(config.pron_xpath_selector):
        if pron_element.xpath(_MIDDLE_POLISH_XPATH_SELECTOR):
            continue
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_polish(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = _yield_phn(request, config)
    yield from zip(words, prons)
