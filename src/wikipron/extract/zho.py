"""Sinological IPA extraction for Chinese varieties on Wiktionary.

A single extractor (`extract_word_pron_zho`) handles every Chinese
variety registered in EXTRACTION_FUNCTIONS, living and dead. The
Wiktionary language name carried on `config.language` selects the
right sub-tree of the pronunciation block; `config.dialect` picks the
specific dialect bullet. Living varieties live in `<div class="vsHide">`
(filtered by the "Sinological" label); Old / Middle Chinese live
elsewhere in the same `<div class="zhpron">` block and are filtered by
the Zhengzhang Shangfang anchor.
"""

import itertools
import re
import typing

from wikipron.extract.core import yield_pron
from wikipron.extract.default import IPA_XPATH_SELECTOR
from wikipron.html_utils import HTMLResponse

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


_VS_HIDE = '//div[@class="vsHide"]'
_PRON_BOX = '//div[contains(@class, "zhpron")]'
_SINO = '[contains(., "Sinological")]'

# Wiktionary variety name -> dialect key -> XPath. Each XPath targets
# the <li> that immediately wraps the Sinological IPA <span class="IPA">.
_SINOLOGICAL_IPA_XPATHS: dict[str, dict[str, str]] = {
    "Mandarin": {
        "standard": (
            f'{_VS_HIDE}//li[a[@title="w:Mandarin Chinese"]]'
            f'//li[small/i/a[@title="w:Standard Chinese"]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Cantonese": {
        "standard": (
            f'{_VS_HIDE}//li[a[@title="w:Cantonese"]]'
            f'//li[small/i/a[@title="w:Standard Cantonese"]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Gan": {
        "nanchang": (
            f'{_VS_HIDE}//li[a[@title="w:Gan Chinese"]]'
            f'//li[small/i/a[contains(@title, "Nanchang")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Hakka": {
        # Hakka outer heading uses an mw-redirect link, so we match the
        # Meixian sub-bullet directly inside vsHide.
        "meixian": (
            f'{_VS_HIDE}//li[small/i/a[contains(@title, "Meixian")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Jin": {
        "taiyuan": (
            f'{_VS_HIDE}//li[a[@title="w:Jin Chinese"]]'
            f'//li[small/i/a[contains(@title, "Taiyuan")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Northern Min": {
        "jianou": (
            f'{_VS_HIDE}//li[a[@title="w:Northern Min"]]'
            f'//li[small/i/a[contains(@title, "Jian")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Eastern Min": {
        "fuzhou": (
            f'{_VS_HIDE}//li[a[@title="w:Eastern Min"]]'
            f'//li[small/i/a[contains(@title, "Fuzhou")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Puxian Min": {
        # Outer heading is an mw-redirect; key on the Putian sub-bullet.
        "putian": (
            f'{_VS_HIDE}//li[small/i/a[contains(@title, "Putian")]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Min Nan": {
        # Hokkien -> Sinological IPA (Kaohsiung); Teochew -> Sinological IPA.
        "hokkien": (
            f'{_VS_HIDE}//li[a[@title="w:Southern Min"]]'
            f'//li[small/i/a[@title="w:Hokkien"]]'
            f'//li[small[contains(., "Sinological")'
            f' and contains(., "Kaohsiung")]]'
        ),
        "teochew": (
            f'{_VS_HIDE}//li[a[@title="w:Southern Min"]]'
            f'//li[small/i/a[@title="w:Teochew dialect"]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Leizhou Min": {
        # Leizhou is sometimes nested under Southern Min, sometimes a
        # sibling list inside vsHide; match by the Leizhou anchor only.
        "leizhou": (
            f'{_VS_HIDE}//li[small/i/a[@title="w:Leizhou Min"]]'
            f"/ul/li{_SINO}"
        ),
    },
    "Southern Pinghua": {
        "nanning": (
            f'{_VS_HIDE}//li[a[@title="w:Pinghua"'
            f' and text()="Southern Pinghua"]]'
            f'//li[contains(., "Nanning")]/ul/li{_SINO}'
        ),
    },
    "Wu": {
        "shanghai": (
            f'{_VS_HIDE}//li[a[@title="w:Wu Chinese"]]'
            f'//li[small[contains(., "Sinological")'
            f' and contains(., "Shanghai")]]'
        ),
    },
    "Xiang": {
        "changsha": (
            f'{_VS_HIDE}//li[a[@title="w:Xiang Chinese"]]'
            f'//li[small/i/a[contains(@title, "Changsha")]]'
            f"/ul/li{_SINO}"
        ),
    },
    # Old / Middle Chinese sit in their own collapsibles outside vsHide,
    # so we scope to the surrounding pronunciation box and filter by the
    # Zhengzhang Shangfang anchor.
    "Old Chinese": {
        "zhengzhang": (
            f'{_PRON_BOX}//li[a[@title="w:Old Chinese"]]'
            f'//dd[small/i/a[@title="w:Zhengzhang Shangfang"]]'
        ),
    },
    "Middle Chinese": {
        "zhengzhang": (
            f"{_PRON_BOX}//table"
            f'//tr[th[.//a[@title="w:Zhengzhang Shangfang"]]]/td[1]'
        ),
    },
}


def _normalize(key: str) -> str:
    # Match keys leniently: lowercase + strip everything that isn't
    # an ASCII letter or digit. So "Jian'ou", "jian-ou", "Jian Ou",
    # and "jianou" all resolve to "jianou".
    return re.sub(r"[^a-z0-9]+", "", key.lower())


def _selectors(language: str, dialect: str | None) -> list[str]:
    table = _SINOLOGICAL_IPA_XPATHS[language]
    if not dialect:
        return list(table.values())
    normalized = _normalize(dialect)
    for key, xpath in table.items():
        if _normalize(key) == normalized:
            return [xpath]
    raise ValueError(
        f"Unsupported dialect for {language!r}: {dialect!r}. "
        f"Expected one of {sorted(table)}."
    )


def extract_word_pron_zho(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    if config.narrow:
        # Sinological IPA on Wiktionary is phonemic (/.../). No narrow
        # form exists for these varieties, so emit nothing rather than
        # duplicating broad output.
        return
    selectors = _selectors(config.language, config.dialect)
    words = itertools.repeat(word)
    prons = (
        pron
        for selector in selectors
        for el in request.html.xpath(selector)
        for pron in yield_pron(el, IPA_XPATH_SELECTOR, config)
    )
    yield from zip(words, prons)
