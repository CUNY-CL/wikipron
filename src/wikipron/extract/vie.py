"""Word and pron extraction for Vietnamese."""

import itertools
import typing

import requests_html

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

_PRON_XPATH_SELECTOR_TEMPLATE = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:{language} pronunciation"
    or
    @title = "wikipedia:{language} phonology"
  ]]]
  and
  span[@class = "IPA"]
  {dialect_selector}
]
"""

_DIALECT_XPATH_SELECTOR_TEMPLATE = (
    "and\n"
    '  (span[@class = "ib-content" and {dialects_text}]\n'
    "   or i/a[{dialects_text}])"
)

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


def extract_pron(
    request: requests_html, selector: str, config: "Config"
) -> "Iterator[str]":
    for pron_element in request.html.xpath(selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_vie(
    word: str, request: requests_html, config: "Config"
) -> "Iterator[WordPronPair]":
    if config.dialect:
        dialect_selector = _DIALECT_XPATH_SELECTOR_TEMPLATE.format(
            dialects_text=" or ".join(
                f'text() = "{d.strip()}"' for d in config.dialect.split("|")
            )
        )
        selector = _PRON_XPATH_SELECTOR_TEMPLATE.format(
            language=config.language, dialect_selector=dialect_selector
        )
        prons = extract_pron(request, selector, config)
    else:
        prons = extract_pron(request, config.pron_xpath_selector, config)
    words = itertools.repeat(word)
    yield from zip(words, prons)
