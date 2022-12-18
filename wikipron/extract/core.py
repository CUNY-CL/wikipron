"""Core functionality for word and pron extraction."""

import logging
import re
import typing
import unicodedata

import requests_html


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator


def _skip_pron(pron: str, skip_spaces: bool) -> bool:
    if "-" in pron:
        return True
    if skip_spaces and (" " in pron or "\u00A0" in pron):
        return True
    return False


def _handle_parens(pron: str, skip_parens: bool) -> str:
    if skip_parens:
        pron = pron.replace("(", "").replace(")", "")
    return pron


def yield_pron(
    request_html: requests_html.Element,
    ipa_xpath_selector: str,
    config: "Config",
) -> "Iterator[str]":
    for ipa_element in request_html.xpath(ipa_xpath_selector):
        m = re.search(config.ipa_regex, ipa_element.text)
        if not m:
            continue
        pron = m.group(1)
        # Removes parens around various segments unless --keep-parens is used.
        pron = _handle_parens(pron, config.skip_parens)
        if _skip_pron(pron, config.skip_spaces_pron):
            continue
        try:
            # All pronunciation processing is done in NFD-space.
            pron = unicodedata.normalize("NFD", pron)
            pron = config.process_pron(pron)
        except IndexError:
            logging.info(
                "IndexError encountered processing %s during scrape of %s",
                pron,
                config.language,
            )
            continue
        if pron:
            # The segments package inserts a # in-between spaces.
            if not config.skip_spaces_pron:
                pron = pron.replace(" #", "")
            yield pron
