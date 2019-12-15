#!/usr/bin/env python

import csv
import json
import logging
import os
import tempfile


def rewrite_wikipron_tsv(
    wiki_tsv_affix, transcription_level, frequencies_dict
):
    # Complete WikiPron TSV path.
    file_to_target = wiki_tsv_affix + transcription_level
    # Will try to overwrite phonetic and phonemic Wikipron TSVs
    # for all Wortschatz languages. WikiPron may not have both a
    # phonetic and phonemic TSV for all languages.
    try:
        # This is written to be run after remove_duplicates.sh
        # and retain sorted order.
        with open(file_to_target, "r") as wiki_file:
            wiki_tsv = csv.reader(
                wiki_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            with tempfile.NamedTemporaryFile(
                mode="w", dir="../../tsv", delete=False
            ) as source:
                for word, pron in wiki_tsv:
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
        os.replace(temp_path, file_to_target)
    except FileNotFoundError as err:
        logging.info("File not found: %s", err)


def main():
    with open("wortschatz_languages.json", "r") as langs:
        languages = json.load(langs)

    word_freq_dict = {}
    transcription = ["_phonetic.tsv", "_phonemic.tsv"]

    for freq_file in os.listdir("freq_tsvs"):
        # For accessing correct language in wortschatz_languages.json.
        file_to_match = freq_file.rsplit("-", 1)[0]
        logging.info("Currently working on: %s", file_to_match)

        with open(f"freq_tsvs/{freq_file}", "r") as tsv:
            frequencies_tsv = csv.reader(
                tsv, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in frequencies_tsv:
                # Wortschatz TSVs are not uniformly formatted.
                # Some have 3 columns, some have 4.
                try:
                    word = row[2].lower()
                    freq = int(row[3])
                except IndexError:
                    word = row[1].lower()
                    freq = int(row[2])
                # Filter out numbers in Wortschatz data.
                if str.isalpha(word):
                    if word not in word_freq_dict:
                        word_freq_dict[word] = freq
                    else:
                        word_freq_dict[word] = word_freq_dict[word] + freq

        for wiki_tsv_path in languages[file_to_match]["path"]:
            for level in transcription:
                rewrite_wikipron_tsv(wiki_tsv_path, level, word_freq_dict)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
