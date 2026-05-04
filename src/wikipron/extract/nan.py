"""Word and pron extraction for Min Nan Chinese (Southern Min)."""

import itertools
import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.zho import yield_zhpron_monospace

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, WordPronPair


# Maps the dialect string from --dialect (or languages.json) to the
# XPath predicate that picks out the matching <dd> within the
# Southern Min <li>. Keys are matched case-insensitively.
_DIALECT_PREDICATES = {
    "hokkien": 'small//a[@title="w:Hokkien"]',
    "teochew": 'small//a[@title="w:Teochew dialect"]',
    "leizhou": 'small//a[@title="w:Leizhou Min"]',
}

_PRON_XPATH_TEMPLATE = (
    '//li[a[@title="w:Southern Min"]]//dd[{dialect_predicate}]'
)


def _selector_for(dialect: typing.Optional[str]) -> str:
    if not dialect:
        # No dialect filter: union of all three known dialects.
        predicate = " or ".join(_DIALECT_PREDICATES.values())
        return _PRON_XPATH_TEMPLATE.format(dialect_predicate=predicate)
    key = dialect.strip().lower()
    if key not in _DIALECT_PREDICATES:
        raise ValueError(
            f"Unsupported Min Nan dialect: {dialect!r}. "
            f"Expected one of: {sorted(_DIALECT_PREDICATES)}."
        )
    return _PRON_XPATH_TEMPLATE.format(
        dialect_predicate=_DIALECT_PREDICATES[key]
    )


def extract_word_pron_nan(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    # Min Nan pronunciations on Wiktionary are non-IPA romanizations
    # (POJ, Peng'im, Leizhou Pinyin), so the broad-vs-narrow IPA
    # distinction does not apply; emit nothing for narrow runs to
    # avoid producing duplicates of the broad output.
    if config.narrow:
        return
    selector = _selector_for(config.dialect)
    words = itertools.repeat(word)
    prons = (
        pron
        for dd in request.html.xpath(selector)
        for pron in yield_zhpron_monospace(dd, config)
    )
    yield from zip(words, prons)
