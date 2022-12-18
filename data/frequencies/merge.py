#!/usr/bin/env python
"""Merges downloaded frequency data with pronunciation data."""

import argparse
import csv
import json
import logging
import os

from typing import Dict

from grab_wortschatz_data import WORTSCHATZ_DICT_PATH


def write_frequency_tsv(
    wiki_tsv_prefix: str,
    level: str,
    frequencies_dict: Dict[str, int],
    args: argparse.Namespace,
) -> None:
    # Complete WikiPron TSV paths.
    basename = f"{wiki_tsv_prefix}_{level}.tsv"
    source_path = os.path.join(args.source_pron_dir, basename)
    sink_path = os.path.join(args.dest_dir, basename)
    # Will try to overwrite narrow and broad WikiPron TSVs for all Wortschatz
    # languages. WikiPron may not have both a narrow and broad TSV for all
    # languages.
    try:
        # This is written to be run after remove_duplicates_and_split.sh
        # and retain sorted order.
        with open(source_path, "r", encoding="utf-8") as wiki_file:
            wiki_tsv = csv.reader(
                wiki_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            with open(sink_path, "w") as source:
                # Our TSVs may be two or three columns
                # depending on if merge.py has been run.
                for word, pron, *prev_count in wiki_tsv:
                    # Check if WikiPron word is in Wortschatz frequencies
                    # else set frequency to 0.
                    if word in frequencies_dict:
                        print(
                            f"{word}\t{pron}\t{frequencies_dict[word]}",
                            file=source,
                        )
                    else:
                        print(f"{word}\t{pron}\t0", file=source)
    except FileNotFoundError as err:
        logging.info("File not found: %s", err)


def main(args: argparse.Namespace) -> None:
    with open(WORTSCHATZ_DICT_PATH, "r", encoding="utf-8") as langs:
        languages = json.load(langs)
    levels = [
        "narrow",
        "broad",
        "narrow_filtered",
        "broad_filtered",
    ]
    os.makedirs(args.dest_dir, exist_ok=True)
    for freq_file in os.listdir(args.source_freq_dir):
        word_freq_dict = {}
        # For accessing correct language in wortschatz_languages.json.
        file_to_match = freq_file.rsplit("-", 1)[0]
        logging.info("Currently working on: %s", file_to_match)

        freq_path = os.path.join(args.source_freq_dir, freq_file)
        with open(freq_path, "r", encoding="utf-8") as tsv:
            frequencies_tsv = csv.reader(
                tsv, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in frequencies_tsv:
                # Wortschatz TSVs are not uniformly formatted.
                # Some have 3 columns, some have 4.
                try:
                    word = row[2].casefold()
                    freq = int(row[3])
                except IndexError:
                    word = row[1].casefold()
                    freq = int(row[2])
                if word not in word_freq_dict:
                    word_freq_dict[word] = freq
                else:
                    word_freq_dict[word] = word_freq_dict[word] + freq
        for wiki_tsv_prefix in languages[file_to_match]["file_prefixes"]:
            for level in levels:
                write_frequency_tsv(
                    wiki_tsv_prefix, level, word_freq_dict, args
                )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest-dir",
        required=True,
        help="destination directory where the merged data is created",
    )
    parser.add_argument(
        "--source-pron-dir",
        required=True,
        help="source directory of pronunciation data as TSV files",
    )
    parser.add_argument(
        "--source-freq-dir",
        default="tsv",
        help=(
            "source directory of frequency data "
            "unpacked from the downloaded Wortschatz files"
        ),
    )
    main(parser.parse_args())
