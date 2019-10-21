import argparse
import logging
import sys

from typing import List

import wikipron
from wikipron.config import Config
from wikipron.scrape import scrape


def _get_cli_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=wikipron.__doc__)
    parser.add_argument(
        "key", help="Key (i.e., name or ISO-639 code) for the language"
    )
    parser.add_argument(
        "--phonetic",
        action="store_true",
        help=(
            "Retrieve the [phonetic] transcriptions "
            "rather than the /phonemic/ ones."
        ),
    )
    parser.add_argument(
        "--no-stress",
        action="store_true",
        help="Remove stress marks in pronunciations.",
    )
    parser.add_argument(
        "--no-syllable-boundaries",
        action="store_true",
        help="Remove syllable boundary marks in pronunciations.",
    )
    parser.add_argument(
        "--dialect",
        help=(
            "Retrieve entries that have this dialect specification. "
            "If not given, then all dialects are included in the output. "
            "The dialect name is found together with the IPA transcription, "
            'e.g., "UK" or "US" in "(UK, US) IPA: /təˈmɑːtəʊ/". '
            'To include more than one dialect, use a pipe "|" to separate '
            'the dialect names, e.g., --dialect="General American | US".'
        ),
    )
    parser.add_argument(
        "--require-dialect-label",
        action="store_true",
        help=(
            "Include only entries that have a dialect specification. "
            "If applied, then --dialect must also be used."
        ),
    )
    parser.add_argument(
        "--casefold",
        action="store_true",
        help="Apply case-folding to the orthography.",
    )
    parser.add_argument(
        "--cut-off-date",
        help=(
            "Retrieve only entries that were added to Wiktionary "
            "on or before this date (in ISO format, e.g., 2018-10-23). "
            "If not given, today's date is used."
        ),
    )
    parser.add_argument(
        "--no-segment",
        action="store_true",
        help="Disable IPA segmentation with added whitespace.",
    )
    return parser.parse_args(args)


def _scrape_and_write(config: Config) -> None:
    for i, (word, pron) in enumerate(scrape(config), 1):
        print(f"{word}\t{pron}")
        # TODO: Still logging "X pronunciations scraped" to stdout?
        if i % 100 == 0:
            logging.info("%d pronunciations scraped", i)


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level="INFO")
    args = _get_cli_args(sys.argv[1:])
    config = Config(**args.__dict__)
    _scrape_and_write(config)
