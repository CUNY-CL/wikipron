"""Word and pron extraction for Min Nan."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# /ul/li[small[i[a[@title="w:Hokkien"]]]] is arbitarily selecting
# Hokkien as the 'standard' dialect. Users can then specify the
# particular 'subdialect' of Hokkien that they desire using the
# --dialect flag.
_PRON_XPATH_SELECTOR_TEMPLATE = """
    //div[@class="vsHide"][(.|ul)]
        //li[a[@title="w:Min Nan"]]
            /ul/li[small[i[a[@title="w:Hokkien"]]]]
                {dialect_selector}
"""

_DIALECT_XPATH_SELECTOR_TEMPLATE = """
/ul
    /li[
        small[i[a[{dialects_text}]]]
    ]
"""


def yield_nan_pron(
    request: requests_html, selector: str, config: "Config"
) -> "Iterator[str]":
    for li_container in request.html.xpath(selector):
        yield from yield_pron(li_container, IPA_XPATH_SELECTOR, config)


def extract_word_pron_nan(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    if config.dialect:
        dialect_selector = _DIALECT_XPATH_SELECTOR_TEMPLATE.format(
            dialects_text=" or ".join(
                f'text() = "{d.strip()}"' for d in config.dialect.split("|")
            )
        )
    else:
        dialect_selector = ""
    selector = _PRON_XPATH_SELECTOR_TEMPLATE.format(
        dialect_selector=dialect_selector
    )
    words = itertools.repeat(word)
    prons = yield_nan_pron(request, selector, config)
    yield from zip(words, prons)
