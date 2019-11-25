"""Core functionality for word and pron extraction."""

import re
import typing

import requests_html


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron


def _skip_pron(pron: str) -> bool:
    if "-" in pron:
        return True
    if " " in pron:
        return True
    return False


def yield_pron(
    request_html: requests_html.Element,
    ipa_xpath_selector: str,
    config: "Config",
) -> "Iterator[Pron]":
    for ipa_element in request_html.xpath(ipa_xpath_selector):
        m = re.search(config.ipa_regex, ipa_element.text)
        if not m:
            continue
        pron = m.group(1)
        # Removes parens around various segments.
        pron = pron.replace("(", "").replace(")", "")
        if _skip_pron(pron):
            continue
        pron = config.process_pron(pron)
        if pron:
            yield pron
