#!/usr/bin/env python

import csv
import json
import logging
import os
import tempfile

from typing import Dict

from grab_wortschatz_data import WORTSCHATZ_DICT_PATH


def write_frequency_tsv(
    wiki_tsv_affix: str,
    level: str,
    frequencies_dict: Dict[str, int],
) -> None:
    # Complete WikiPron TSV paths.
    basename = f"{wiki_tsv_affix}_{level}"
    source_path = f"{basename}.tsv"
    sink_path = f"{basename}_freq.tsv"
    # Will try to overwrite phonetic and phonemic WikiPron TSVs
    # for all Wortschatz languages. WikiPron may not have both a
    # phonetic and phonemic TSV for all languages.
    try:
        # This is written to be run after remove_duplicates_and_split.sh
        # and retain sorted order.
        with open(source_path, "r", encoding="utf-8") as wiki_file:
            wiki_tsv = csv.reader(
                wiki_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            with tempfile.NamedTemporaryFile(
                mode="w", dir="../tsv", delete=False
            ) as source:
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
                temp_path = source.name
        os.replace(temp_path, sink_path)
    except FileNotFoundError as err:
        logging.info("File not found: %s", err)


def main() -> None:
    with open(WORTSCHATZ_DICT_PATH, "r", encoding="utf-8") as langs:
        languages = json.load(langs)
    levels = [
        "phonetic",
        "phonemic",
        "phonetic_filtered",
        "phonemic_filtered",
    ]
    for freq_file in os.listdir("tsv"):
        word_freq_dict = {}
        # For accessing correct language in wortschatz_languages.json.
        file_to_match = freq_file.rsplit("-", 1)[0]
        logging.info("Currently working on: %s", file_to_match)

        with open(f"tsv/{freq_file}", "r", encoding="utf-8") as tsv:
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
        for wiki_tsv_path in languages[file_to_match]["path"]:
            for level in levels:
                write_frequency_tsv(wiki_tsv_path, level, word_freq_dict)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
