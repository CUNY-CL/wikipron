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
        "key", help="key (i.e., ISO 639 code or name) for the language"
    )
    parser.add_argument(
        "--narrow",
        action="store_true",
        help="retrieves [narrow] rather than /broad/ transcriptions",
    )
    parser.add_argument(
        "--stress",
        action="store_true",
        default=True,
        help="includes stress in the transcriptions",
    )
    parser.add_argument(
        "--no-stress",
        action="store_false",
        dest="stress",
        help="removes stress from the transcriptions",
    )
    parser.add_argument(
        "--syllable-boundaries",
        action="store_true",
        default=True,
        help="includes syllable boundaries in the transcriptions",
    )
    parser.add_argument(
        "--no-syllable-boundaries",
        action="store_false",
        dest="syllable_boundaries",
        help="removes syllable boundaries in the transcriptions",
    )
    parser.add_argument(
        "--dialect",
        help="restricts to entries matching this dialect specification",
    )
    parser.add_argument(
        "--casefold",
        action="store_true",
        help="applies case-folding to the orthographic form",
    )
    parser.add_argument(
        "--cut-off-date",
        help="restricts to entries added on or before an (ISO 8601) date",
    )
    parser.add_argument(
        "--segment",
        action="store_true",
        default=True,
        help="segments the IPA pronunciation (e.g., with whitespace)",
    )
    parser.add_argument(
        "--no-segment",
        action="store_false",
        dest="segment",
        help="does not segment the IPA pronunciation",
    )
    parser.add_argument(
        "--skip-spaces-word",
        action="store_true",
        default=True,
        help="skips entries with space in orthographic form",
    )
    parser.add_argument(
        "--no-skip-spaces-word",
        dest="skip_spaces_word",
        action="store_false",
        help="does not skip entries with space in orthographic form",
    )
    parser.add_argument(
        "--skip-spaces-pron",
        action="store_true",
        default=True,
        help="skips entries with space in the transcription",
    )
    parser.add_argument(
        "--no-skip-spaces-pron",
        dest="skip_spaces_pron",
        action="store_false",
        help="does not skip entries with space in the transcript",
    )
    parser.add_argument(
        "--tone",
        action="store_true",
        default=True,
        help="includes tones in the transcriptions",
    )
    parser.add_argument(
        "--no-tone",
        action="store_false",
        dest="tone",
        help="removes tones from the transcriptions",
    )
    parser.add_argument(
        "--skip-parens",
        action="store_true",
        default=True,
        help="removes parentheses from the transcriptions",
    )
    parser.add_argument(
        "--no-skip-parens",
        action="store_false",
        dest="skip_parens",
        help="includes parentheses in the transcriptions",
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
