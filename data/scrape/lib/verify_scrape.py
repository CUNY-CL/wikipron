#!/usr/bin/env python
"""Verify a re-scraped TSV against a previous version.

Net line count can hide a *partial* scrape: if a block of category pages
is skipped, a contiguous run of words is deleted while the total barely
moves (the deletions are masked by the tens of thousands of unchanged
lines). This script compares word *sets* -- not just counts -- and flags
contiguous runs of dropped words, which is the signature of a skipped
page batch.

Typical use, right after re-scraping and before committing (run from
``data/scrape/``)::

    ./lib/verify_scrape.py tsv/tha_thai_broad.tsv

That compares the working-tree file (NEW) against its committed (HEAD)
version (OLD). To compare against a different commit or an explicit
file::

    ./lib/verify_scrape.py tsv/tha_thai_broad.tsv --against v2.2.0
    ./lib/verify_scrape.py tsv/tha_thai_broad.tsv --old /tmp/old.tsv

To tell genuine Wiktionary attrition from a partial scrape, probe a
sample of the dropped words against live Wiktionary -- if they still
extract with the current code, they were skipped, not deleted upstream
(``--key``/``--narrow`` are inferred from the filename when omitted)::

    ./lib/verify_scrape.py tsv/tha_thai_broad.tsv --probe 20

Exit status is 1 when a partial scrape is suspected (a contiguous
dropped-run at least ``--min-run`` long, or -- with ``--probe`` -- most
sampled drops still extract), else 0, so it can gate a workflow.
"""

import argparse
import collections
import os
import subprocess
import sys
import unicodedata

import requests

import wikipron
from wikipron.html_utils import HTMLResponse
from wikipron.scrape import HTTP_HEADERS, _PAGE_TEMPLATE


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _read_working(path: str) -> list[str]:
    with open(path, encoding="utf-8") as source:
        return source.read().splitlines()


def _read_git(ref: str, path: str) -> list[str]:
    toplevel = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    rel = os.path.relpath(os.path.abspath(path), toplevel)
    shown = subprocess.run(
        ["git", "-C", toplevel, "show", f"{ref}:{rel}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return shown.stdout.splitlines()


def _pairs(lines: list[str]) -> list[tuple[str, str]]:
    # (word, pron) for non-empty TSV lines; words NFC-normalized so a
    # normalization difference is not mistaken for a dropped word.
    out = []
    for line in lines:
        if not line.strip() or "\t" not in line:
            continue
        word, pron = line.split("\t", 1)
        out.append((_nfc(word), pron))
    return out


def _word_to_prons(pairs: list[tuple[str, str]]) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = collections.defaultdict(set)
    for word, pron in pairs:
        mapping[word].add(pron)
    return mapping


def _ordered_unique_words(pairs: list[tuple[str, str]]) -> list[str]:
    seen: set[str] = set()
    order: list[str] = []
    for word, _ in pairs:
        if word not in seen:
            seen.add(word)
            order.append(word)
    return order


def _dropped_runs(
    old_order: list[str], new_words: set[str]
) -> list[tuple[str, str, int]]:
    """Contiguous runs (in OLD file order) of words absent from NEW.

    Files are byte-sorted by ``postprocess``, so a contiguous run here is
    a contiguous alphabetical block -- i.e. a plausibly skipped batch.
    Returns ``(first_word, last_word, length)`` sorted longest-first.
    """
    runs: list[tuple[int, int]] = []
    start = None
    for i, word in enumerate(old_order):
        absent = word not in new_words
        if absent and start is None:
            start = i
        elif not absent and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(old_order) - 1))
    sized = [(old_order[a], old_order[b], b - a + 1) for a, b in runs]
    sized.sort(key=lambda run: -run[2])
    return sized


def _infer_key_narrow(
    path: str, key: str | None, narrow: bool
) -> tuple[str, bool]:
    base = os.path.basename(path)
    inferred_key = key or base.split("_", 1)[0]
    inferred_narrow = narrow or ("narrow" in base)
    return inferred_key, inferred_narrow


def _probe(
    dropped: list[str], key: str, narrow: bool, n: int
) -> tuple[int, int]:
    config = wikipron.Config(key=key, narrow=narrow)
    step = max(1, len(dropped) // n)
    sample = dropped[::step][:n]
    print(
        f"\nProbing {len(sample)} dropped words live (key={key!r}, "
        f"narrow={narrow}):"
    )
    still_extracts = 0
    for word in sample:
        try:
            response = requests.get(
                _PAGE_TEMPLATE.format(word=word),
                headers=HTTP_HEADERS,
                timeout=30,
            )
        except requests.exceptions.RequestException as error:
            print(f"  {word}: request error ({error})")
            continue
        pairs = list(
            config.extract_word_pron(word, HTMLResponse(response), config)
        )
        if pairs:
            still_extracts += 1
        verdict = "STILL EXTRACTS" if pairs else "gone/empty upstream"
        print(f"  {word}: {verdict} ({len(pairs)} pron)")
    return still_extracts, len(sample)


def main(args: argparse.Namespace) -> int:
    new_lines = _read_working(args.new)
    if args.old is not None:
        old_lines = _read_working(args.old)
        old_label = args.old
    else:
        old_lines = _read_git(args.against, args.new)
        old_label = f"{args.against}:{args.new}"

    old_pairs = _pairs(old_lines)
    new_pairs = _pairs(new_lines)
    old_map = _word_to_prons(old_pairs)
    new_map = _word_to_prons(new_pairs)
    old_words = set(old_map)
    new_words = set(new_map)
    dropped = sorted(old_words - new_words)
    gained = sorted(new_words - old_words)
    common = old_words & new_words
    changed = [w for w in common if old_map[w] != new_map[w]]

    print(f"OLD  {old_label}")
    print(f"NEW  {args.new}")
    print(
        f"\nlines:  old {len(old_pairs):>7}   new {len(new_pairs):>7}   "
        f"({len(new_pairs) - len(old_pairs):+d})"
    )
    print(
        f"words:  old {len(old_words):>7}   new {len(new_words):>7}   "
        f"({len(new_words) - len(old_words):+d})"
    )
    print(f"\n  dropped (in old, not new): {len(dropped)}")
    print(f"  gained  (in new, not old): {len(gained)}")
    print(f"  common words:              {len(common)}")
    print(f"  common words, pron changed:{len(changed)}")

    runs = _dropped_runs(_ordered_unique_words(old_pairs), new_words)
    big = [r for r in runs if r[2] >= args.min_run]
    print(f"\ncontiguous dropped-runs (>= {args.min_run} words): {len(big)}")
    for first, last, length in big[:10]:
        print(f"    len={length:>4}   [{first} .. {last}]")

    partial_suspected = bool(big)
    if partial_suspected:
        in_runs = sum(length for _, _, length in big)
        print(
            f"\n  WARNING: partial scrape suspected. {in_runs} dropped "
            f"words fall in contiguous blocks.\n     Genuine attrition is "
            f"scattered; contiguous alphabetical blocks mean a\n     "
            f"skipped page batch. Re-run the scrape for this language."
        )
    else:
        print(
            "\n  OK: no large contiguous dropped-runs; drops look like "
            "scattered attrition."
        )

    if args.probe and dropped:
        key, narrow = _infer_key_narrow(args.new, args.key, args.narrow)
        extracts, sampled = _probe(dropped, key, narrow, args.probe)
        print(
            f"\n  {extracts}/{sampled} sampled dropped words STILL extract "
            f"with current code."
        )
        if sampled and extracts / sampled >= 0.5:
            partial_suspected = True
            print(
                "  WARNING: most dropped words still exist upstream -> they "
                "were skipped, not deleted. Re-run the scrape."
            )

    return 1 if partial_suspected else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("new", help="path to the re-scraped (new) TSV")
    parser.add_argument(
        "--against",
        default="HEAD",
        help="git ref to compare against (default: HEAD)",
    )
    parser.add_argument(
        "--old",
        default=None,
        help="explicit old TSV file (overrides --against)",
    )
    parser.add_argument(
        "--min-run",
        type=int,
        default=15,
        help="flag contiguous dropped-runs at least this long "
        "(default: 15)",
    )
    parser.add_argument(
        "--probe",
        type=int,
        default=0,
        metavar="N",
        help="probe N sampled dropped words against live Wiktionary",
    )
    parser.add_argument(
        "--key", default=None, help="ISO code for --probe (else inferred)"
    )
    parser.add_argument(
        "--narrow",
        action="store_true",
        help="use narrow transcription for --probe (else inferred)",
    )
    sys.exit(main(parser.parse_args()))
