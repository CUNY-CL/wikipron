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
        "key", help="Key (i.e., ISO 639 code or name) for the language"
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
        "--stress",
        action="store_true",
        dest="stress",
        default=True,
        help="Include stress marks in pronunciations.",
    )
    parser.add_argument(
        "--no-stress",
        action="store_false",
        dest="stress",
        help="Remove stress marks from pronunciations.",
    )
    parser.add_argument(
        "--syllable-boundaries",
        action="store_true",
        dest="syllable_boundaries",
        default=True,
        help="Include syllable boundary marks in pronunciations.",
    )
    parser.add_argument(
        "--no-syllable-boundaries",
        action="store_false",
        dest="syllable_boundaries",
        help="Remove syllable boundary marks from pronuncations.",
    )
    parser.add_argument(
        "--dialect",
        help=(
            "Retrieve entries that have this dialect specification. "
            "If not given, then all dialects are included in the output. "
            "The dialect name can be found together with the IPA transcription"
            " in the Wiktionary entries, "
            'e.g., "UK" or "US" in "(UK, US) IPA: /təˈmɑːtəʊ/". '
            'To include more than one dialect, use a pipe "|" to separate '
            'the dialect names, e.g., --dialect="General American | US". '
            "Note that whether or not --dialect is used, all entries that "
            "have no dialects specified are included in the output."
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
            "If not given, today's date is used. "
            "Explicitly setting a cut-off date is useful if you want a "
            "relatively stable dataset no matter when you initiate a "
            "scraping run."
        ),
    )
    parser.add_argument(
        "--segment",
        action="store_true",
        dest="segment",
        default=True,
        help=(
            "Segment the IPA pronunciation by whitespace and,"
            "to the extent possible, with a diacritic (either combining "
            "or modifier) immediately following the parent symbol. "
            'For example, "kʰæt" is segmented as "kʰ æ t", with kʰ '
            "conveniently segmented as an aspirated k for modeling purposes. "
        ),
    )
    parser.add_argument(
        "--no-segment",
        action="store_false",
        dest="segment",
        help=(
            "To avoid segmenting the IPA pronunciation by whitespace,"
            "apply this flag."
        ),
    )
    parser.add_argument(
        "--no-skip-spaces-word",
        action="store_true",
        help="Skip spaces in the orthography",
    )
    parser.add_argument(
        "--no-skip-spaces-pron",
        action="store_true",
        help="Skip spaces in the transcription",
    )
    parser.add_argument(
        "--tone",
        action="store_true",
        dest="tone",
        default=True,
        help=("Include tones in pronunciations."),
    )
    parser.add_argument(
        "--no-tone",
        action="store_false",
        dest="tone",
        help=("Remove tones from pronunciations."),
    )
    return parser.parse_args(args)


def _scrape_and_write(config: Config) -> None:
    for i, (word, pron) in enumerate(scrape(config), 1):
        print(f"{word}\t{pron}")
        if i % 100 == 0:
            logging.info("%d pronunciations scraped", i)


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level="INFO")
    args = _get_cli_args(sys.argv[1:])
    config = Config(**args.__dict__)
    _scrape_and_write(config)
