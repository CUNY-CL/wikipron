"""Core functionality for word and pron extraction."""

import itertools
import logging
import re
import typing
import unicodedata


from wikipron.html_utils import HTMLTree

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator


def _skip_pron(pron: str, skip_spaces: bool) -> bool:
    if "-" in pron:
        return True
    if skip_spaces and (" " in pron or "\u00a0" in pron):
        return True
    return False


def _skip_parens(pron: str) -> str:
    """Remove all parentheses from a pronunciation string."""
    return pron.replace("(", "").replace(")", "")


def _expand_parens(pron: str) -> list[str]:
    """Expand parenthesized groups into all variants.

    Each parenthesized group ``(X)`` generates two alternatives:
    the content ``X`` (included) and the empty string (excluded).
    Multiple groups produce a Cartesian product.
    """
    parts = re.split(r"(\([^()]+\))", pron)
    alternatives = []
    for part in parts:
        if part.startswith("(") and part.endswith(")"):
            alternatives.append([part[1:-1], ""])
        else:
            alternatives.append([part])
    return ["".join(combo) for combo in itertools.product(*alternatives)]


def yield_pron(
    request_html: HTMLTree,
    ipa_xpath_selector: str,
    config: "Config",
) -> "Iterator[str]":
    for ipa_element in request_html.xpath(ipa_xpath_selector):
        m = re.search(config.ipa_regex, ipa_element.text)
        if not m:
            continue
        pron = m.group(1)
        if config.parens == "skip":
            prons_to_process = [_skip_parens(pron)]
        elif config.parens == "expand":
            prons_to_process = _expand_parens(pron)
        else:  # "show"
            prons_to_process = [pron]
        for pron in prons_to_process:
            if _skip_pron(pron, config.skip_spaces_pron):
                continue
            try:
                # All pronunciation processing is done in
                # NFD-space.
                pron = unicodedata.normalize("NFD", pron)
                pron = config.process_pron(pron)
            except IndexError:
                logging.info(
                    "IndexError processing %s in %s",
                    pron,
                    config.language,
                )
                continue
            if pron:
                # The segments package inserts a # in-between
                # spaces.
                if not config.skip_spaces_pron:
                    pron = pron.replace(" #", "")
                yield pron
