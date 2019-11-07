"""Core functionality for word and pron extraction."""

import re
import typing

import requests


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Pron


def yield_pron(
    request_html: requests.Response, ipa_xpath_selector: str, config: "Config"
) -> "Iterator[Pron]":
    for x in request_html.xpath(ipa_xpath_selector):
        m = re.search(config.ipa_regex, x.text)
        if not m:
            continue
        pron = m.group(1)
        # Removes parens around various segments.
        pron = pron.replace("(", "").replace(")", "")
        # Skips examples with a space in the pron.
        if " " in pron:
            continue
        pron = config.process_pron(pron)
        if pron:
            yield pron
