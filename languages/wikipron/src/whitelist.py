#!/usr/bin/env python

import sys
import re


def whitelist_reader(path):
    """Reads in whitelist file"""
    with open(path, "r") as source:
        for line in source:
            yield line.rstrip().split()[0]


def filter(tsv_path, phonemes, output_path):
    """Creates tsv filtered by whitelist"""
    with open(tsv_path, "r") as source:
        with open(output_path, "w") as output:
            for line in source:
                pron = set(line.split("\t")[1].split())
                if phonemes.issuperset(pron):
                    print(line.rstrip(), file=output)
                else:
                    pass


def main() -> None:
    tsv_path = sys.argv[1]
    iso639_code = tsv_path[tsv_path.rindex("/") + 1:tsv_path.index("_")]
    dialect = re.search("_(.*)_", tsv_path)
    if dialect:
        whitelist_path = f"../whitelist/{iso639_code}_{dialect[1]}_phonemic.whitelist"
        output_path = f"../tsv/{iso639_code}_{dialect[1]}_filtered_phonemic.tsv"
    else:
        whitelist_path = f"../whitelist/{iso639_code}_phonemic.whitelist"
        output_path = f"../tsv/{iso639_code}_filtered_phonemic.tsv"
    try:
        whitelist_phonemes = set(whitelist_reader(whitelist_path))
        whitelist_phonemes.add(" ")
        filter(tsv_path, whitelist_phonemes, output_path)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()
