#!/usr/bin/env python
"""Keeps only exceptionally pronounced Spanish words.

Spanish spelling predicts pronunciation well, so most of the Spanish data is
redundant with a rule-based G2P. After the scrape, this replaces the Spanish
TSVs with the words that have at least one pronunciation not following the
rules in ``spa_rules`` (mostly loanwords); all of the pronunciations of such
words are kept. The unfiltered TSVs are kept in ``spa_raw/`` so the filter can
be re-run without scraping again.

It also writes ``kokoro/es_loanwords.tsv``, the Castilian exceptions as
Spanish respellings in the format read by kokoro.cpp's
``SpanishLoanwords::load()``.
"""

import argparse
import datetime
import logging
import os
import shutil

from collections.abc import Iterator

try:
    from . import spa_rules
except ImportError:
    import spa_rules  # type: ignore[import-not-found,no-redef]

SCRAPE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TSV_DIRECTORY = os.path.join(SCRAPE_DIRECTORY, "tsv")
RAW_DIRECTORY = os.path.join(SCRAPE_DIRECTORY, "spa_raw")
KOKORO_PATH = os.path.join(SCRAPE_DIRECTORY, "kokoro", "es_loanwords.tsv")

# Scraped buckets filtered down to exceptional words.
BUCKETS = ("broad", "broad_filtered", "narrow", "narrow_filtered")
# Extra broad scrape with stress marks, used to check stress placement.
STRESSED_BUCKET = "broad_stressed"
# kokoro.cpp's Spanish G2P is Castilian.
KOKORO_DIALECT = "ca"

_FRONT = frozenset("ei")
_VOWELS = frozenset("aeiou")
_ACCENTED = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
# Broad phone to Spanish spelling; context-dependent ones are handled in
# _respell_phone. IPA symbols without a Spanish spelling (e.g. ʃ) are written
# as is: kokoro.cpp passes unknown symbols through as consonants.
_SPELLING = {
    "b": "b",
    "β": "b",
    "d": "d",
    "ð": "d",
    "f": "f",
    "j": "i",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "ŋ": "n",
    "ɱ": "n",
    "ɲ": "ñ",
    "p": "p",
    "s": "s",
    "t": "t",
    "t͡ʃ": "ch",
    "w": "u",
    "w̝": "u",
    "x": "j",
    "ʃ": "ʃ",
    "ʎ": "ll",
    "θ": "z",
}
# Vowel-like symbols that the respelling cannot express.
_UNSPELLABLE = frozenset("əɐɨʉɯɔɛæøœyʏɒɑʌɪʊː")


def raw_path(raw_dir: str, dialect: str, bucket: str) -> str:
    return os.path.join(raw_dir, f"spa_{dialect}_{bucket}.tsv")


def _read(path: str) -> Iterator[tuple[str, str]]:
    with open(path, "r", encoding="utf-8") as source:
        for line in source:
            word, pron = line.rstrip("\n").split("\t", 1)
            yield word, pron


def _respell_phone(phones: tuple[str, ...], i: int) -> str | None:
    phone = phones[i]
    nxt = phones[i + 1] if i + 1 < len(phones) else ""
    if phone in ("ɡ", "g", "ɣ"):
        return "gu" if nxt in _FRONT else "g"
    if phone == "ɾ":
        return None if i == 0 else "r"
    if phone == "r":
        return "r" if i == 0 or phones[i - 1] in ("l", "n", "s") else "rr"
    if phone == "ʝ":
        return "y" if nxt[:1] in _VOWELS or nxt in ("j", "w") else None
    if phone in _VOWELS:
        return phone
    return _SPELLING.get(phone)


def respell(pron: str) -> str | None:
    """Spanish respelling of a stressed broad pronunciation, if possible.

    The stressed vowel always gets a written accent, which kokoro.cpp's G2P
    uses for stress. Returns None when the pronunciation has no faithful
    respelling.
    """
    phones, stressed = spa_rules.parse_pron(pron)
    if any(ch in _UNSPELLABLE for phone in phones for ch in phone):
        return None
    out: list[str] = []
    for i, phone in enumerate(phones):
        spelled = _respell_phone(phones, i)
        if spelled is None:
            return None
        # "gw" rather than "gu", whose u is silent before e, i.
        nxt = phones[i + 1] if i + 1 < len(phones) else ""
        if phone in ("w", "w̝") and out and out[-1] == "g" and nxt in _FRONT:
            spelled = "w"
        if i in stressed and spelled in _ACCENTED:
            spelled = _ACCENTED[spelled]
        out.append(spelled)
    return "".join(out)


def filter_dialect(
    raw_dir: str, tsv_dir: str, dialect: str
) -> tuple[set[str], int]:
    """Writes the exceptional words of a dialect to the scrape TSVs.

    Returns the set of exceptional words and the number of words judged.
    """
    stressed = raw_path(raw_dir, dialect, STRESSED_BUCKET)
    source = (
        stressed
        if os.path.exists(stressed)
        else raw_path(raw_dir, dialect, "broad")
    )
    rows = list(_read(source))
    words = spa_rules.irregular_words(rows, dialect)
    for bucket in BUCKETS:
        path = raw_path(raw_dir, dialect, bucket)
        if not os.path.exists(path):
            continue
        with open(
            os.path.join(tsv_dir, f"spa_{dialect}_{bucket}.tsv"),
            "w",
            encoding="utf-8",
        ) as sink:
            for word, pron in _read(path):
                if word in words:
                    print(f"{word}\t{pron}", file=sink)
    return words, len({word for word, _ in rows})


def write_kokoro(raw_dir: str, words: set[str], path: str) -> int:
    """Writes the kokoro.cpp loanword table; returns the number of entries."""
    stressed = raw_path(raw_dir, KOKORO_DIALECT, STRESSED_BUCKET)
    if not os.path.exists(stressed):
        logging.warning("No stressed scrape at %r; skipping kokoro", stressed)
        return 0
    entries: dict[str, str] = {}
    for word, pron in _read(stressed):
        key = word.lower()
        if word not in words or key in entries:
            continue
        respelling = respell(pron)
        # The respelling must read back as the pronunciation.
        if respelling is None or not spa_rules.is_regular(
            respelling, pron, KOKORO_DIALECT
        ):
            logging.info("No respelling:\t%s\t%s", word, pron)
            continue
        entries[key] = respelling
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as sink:
        print(
            "# Spanish words with exceptional pronunciations, as Spanish "
            "respellings for kokoro.cpp.",
            file=sink,
        )
        print(
            "# Generated by wikipron data/scrape/lib/spa_exceptions.py on "
            f"{datetime.date.today().isoformat()} from Wiktionary "
            "(CC BY-SA 4.0).",
            file=sink,
        )
        for key in sorted(entries):
            print(f"{key}\t{entries[key]}", file=sink)
    return len(entries)


def apply(
    tsv_dir: str = TSV_DIRECTORY,
    raw_dir: str = RAW_DIRECTORY,
    kokoro_path: str = KOKORO_PATH,
) -> None:
    """Moves freshly scraped Spanish TSVs aside and filters them."""
    os.makedirs(raw_dir, exist_ok=True)
    for dialect in spa_rules.DIALECTS:
        for bucket in BUCKETS:
            scraped = os.path.join(tsv_dir, f"spa_{dialect}_{bucket}.tsv")
            if os.path.exists(scraped):
                shutil.move(scraped, raw_path(raw_dir, dialect, bucket))
    kokoro_words: set[str] = set()
    for dialect in spa_rules.DIALECTS:
        if not os.path.exists(raw_path(raw_dir, dialect, "broad")):
            logging.warning("No raw Spanish %r scrape in %r", dialect, raw_dir)
            continue
        words, total = filter_dialect(raw_dir, tsv_dir, dialect)
        logging.info(
            "Spanish %r: kept %d exceptional of %d words",
            dialect,
            len(words),
            total,
        )
        if dialect == KOKORO_DIALECT:
            kokoro_words = words
    count = write_kokoro(raw_dir, kokoro_words, kokoro_path)
    logging.info("Wrote %d kokoro entries to %r", count, kokoro_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tsv_dir", default=TSV_DIRECTORY)
    parser.add_argument("--raw_dir", default=RAW_DIRECTORY)
    parser.add_argument("--kokoro_path", default=KOKORO_PATH)
    args = parser.parse_args()
    apply(args.tsv_dir, args.raw_dir, args.kokoro_path)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
