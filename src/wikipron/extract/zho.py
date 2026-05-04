"""Shared word and pron extraction helpers for Chinese languages."""

import typing

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.html_utils import HTMLTree
    from wikipron.typing import Iterator


# Wiktionary uses this class for non-IPA Chinese romanizations
# (Pe̍h-ōe-jī, Peng'im, Leizhou Pinyin, Jyutping, Pinyin, etc.).
ZHPRON_MONOSPACE_XPATH_SELECTOR = (
    './/span[contains(@class, "zhpron-monospace")]'
)


def yield_zhpron_monospace(
    container: "HTMLTree", config: "Config"
) -> "Iterator[str]":
    """Yield pronunciations from <span class="zhpron-monospace"> elements.

    Slash-separated variants (e.g. "kim / kem") are split into individual
    pronunciations. Text is yielded as-is — no IPA normalization, since
    these spans hold romanizations like Pe̍h-ōe-jī, Peng'im, or Leizhou
    Pinyin rather than IPA.
    """
    for el in container.xpath(ZHPRON_MONOSPACE_XPATH_SELECTOR):
        for variant in el.text.split("/"):
            pron = variant.strip()
            if not pron:
                continue
            if config.skip_spaces_pron and (" " in pron or " " in pron):
                continue
            yield pron
