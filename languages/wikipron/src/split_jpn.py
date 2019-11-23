#!/usr/bin/env python

import re
import os
import logging

from codes import JPN_PATH


# Filters out kanji that may have snuck in
# as a result of inconsistencies in Wiktionary
# hiragana html elements.
def _contains_kanji(word):
    reg = r"[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]"
    return bool(re.search(reg, word))


def _all_hiragana(word):
    return bool(re.match("^[\u3040-\u309F]+$", word))


# Including half-width katakana forms does not catch
# additional words.
def _all_katakana(word):
    return bool(re.match("^[\u30A0-\u30FF]+$", word))


def _split_file(path_prefix, path_affix, data):
    with open(f"{path_prefix}hira_{path_affix}", "w") as hira_file:
        with open(f"{path_prefix}kana_{path_affix}", "w") as kana_file:
            for line in data:
                word = line.split("\t", 1)[0].rstrip()
                if _contains_kanji(word):
                    continue
                if _all_hiragana(word):
                    print(line.rstrip(), file=hira_file)
                    continue
                elif _all_katakana(word):
                    print(line.rstrip(), file=kana_file)
                    continue
                # Terms with a mixture of hiragana and katakana, for example:
                # https://en.wiktionary.org/wiki/%E3%83%A2%E3%83%92%E3%82%AB%E3%83%B3%E5%88%88%E3%82%8A
                logging.info(
                    '"%s" is neither purely Hiragana nor Katakana.', word
                )


def main():
    phonetic_affix = "phonetic.tsv"
    phonemic_affix = "phonemic.tsv"

    try:
        with open(f"{JPN_PATH}{phonetic_affix}") as jpn_data:
            _split_file(JPN_PATH, phonetic_affix, jpn_data)
        os.remove(f"{JPN_PATH}{phonetic_affix}")
    except FileNotFoundError as err:
        logging.info(
            'No Japanese phonetic TSV: %s', err,
        )

    try:
        with open(f"{JPN_PATH}{phonemic_affix}") as jpn_data:
            _split_file(JPN_PATH, phonemic_affix, jpn_data)
        os.remove(f"{JPN_PATH}{phonemic_affix}")
    except FileNotFoundError as err:
        logging.info(
            'No Japanese phonemic TSV: %s', err,
        )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
