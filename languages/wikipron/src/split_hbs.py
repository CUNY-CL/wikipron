#!/usr/bin/env python

# import re
import os
import logging

from codes import HBS_PATH


def _all_latin(word):
    try:
        word.encode("iso8859_2")
        return True
    except UnicodeEncodeError:
        return False


def _all_cyrillic(word):
    try:
        word.encode("iso8859_5")
        return True
    except UnicodeEncodeError:
        return False


def _split_file(path_prefix, path_affix, data):
    with open(f"{path_prefix}latn_{path_affix}", "w") as latin_file:
        with open(f"{path_prefix}cyrl_{path_affix}", "w") as cyrillic_file:
            for line in data:
                pron = line.split("\t", 1)[0]
                if _all_latin(pron):
                    print(line.rstrip(), file=latin_file)
                    continue
                elif _all_cyrillic(pron):
                    print(line.rstrip(), file=cyrillic_file)
                    continue
                logging.info('"%s" is neither Latin nor Cyrllic.', pron)


# There is currently no hbs_phonetic.tsv
def main():
    phonetic_affix = "phonetic.tsv"
    phonemic_affix = "phonemic.tsv"

    try:
        with open(f"{HBS_PATH}{phonetic_affix}") as serb_croat_data:
            _split_file(HBS_PATH, phonetic_affix, serb_croat_data)
        os.remove(f"{HBS_PATH}{phonetic_affix}")
    except FileNotFoundError as err:
        logging.info("No Serbo-Croatian phonetic TSV: %s", err)

    try:
        with open(f"{HBS_PATH}{phonemic_affix}") as serb_croat_data:
            _split_file(HBS_PATH, phonemic_affix, serb_croat_data)
        os.remove(f"{HBS_PATH}{phonemic_affix}")
    except FileNotFoundError as err:
        logging.info("No Serbo-Croatian phonemic TSV: %s", err)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
