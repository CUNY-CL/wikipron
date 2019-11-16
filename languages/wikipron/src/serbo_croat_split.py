import re
import os
import logging

from codes import SERB_CROAT_PATH


def _contains_latin(word):
    return bool(re.search("[\u0000-\u007F]", word))


def _split_file(path_prefix, path_affix, data):
    with open(f"{path_prefix}latin_{path_affix}", "w") as latin_file:
        with open(f"{path_prefix}cyrillic_{path_affix}", "w") as cyrillic_file:
            for line in data:
                pron = line.split("\t", 1)[0]
                if _contains_latin(pron):
                    print(line.rstrip(), file=latin_file)
                else:
                    print(line.rstrip(), file=cyrillic_file)


# There is currently no hbs_phonetic.tsv
def main():
    phonetic = "phonetic.tsv"
    phonemic = "phonemic.tsv"

    try:
        with open(f"{SERB_CROAT_PATH}{phonetic}") as serb_croat_data:
            _split_file(SERB_CROAT_PATH, phonetic, serb_croat_data)
        os.remove(f"{SERB_CROAT_PATH}{phonetic}")
    except FileNotFoundError as err:
        logging.info(
            "No Serbo-Croatian phonetic tsv: %s", err,
        )

    try:
        with open(f"{SERB_CROAT_PATH}{phonemic}") as serb_croat_data:
            _split_file(SERB_CROAT_PATH, phonemic, serb_croat_data)
        os.remove(f"{SERB_CROAT_PATH}{phonemic}")
    except FileNotFoundError as err:
        logging.info(
            "No Serbo-Croatian phonemic tsv: %s", err,
        )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
