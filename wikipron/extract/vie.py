"""Word and pron extraction for Vietnamese."""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR
# from wikipron.config import _PRON_XPATH_SELECTOR_TEMPLATE

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
    '  (span[@class = "ib-content qualifier-content" and {dialects_text}]\n'
    '   or i/a[{dialects_text}])'
)

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, WordPronPair


def extract_pron_dialect(request, selector, config):
    for pron_element in request.html.xpath(selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_pron_default(request, config):
    for pron_element in request.html.xpath(config.pron_xpath_selector):
        yield from yield_pron(pron_element, IPA_XPATH_SELECTOR, config)


def extract_word_pron_vie(
    word: "Word", request: requests.Response, config: "Config"
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
        prons = extract_pron_dialect(request, selector, config)
    else:
        prons = extract_pron_default(request, config)
    words = itertools.repeat(word)
    yield from zip(words, prons)