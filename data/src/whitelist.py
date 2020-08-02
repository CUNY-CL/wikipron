#!/usr/bin/env python
"""Filters TSVs through a whitelist file.

This script takes lines from a source TSV and writes only entries whose
pronunciations only contain phones found on the whitelist into a new TSV file.
"""

import argparse
import logging
import re

from typing import FrozenSet, Iterator


def _whitelist_reader(path: str) -> Iterator[str]:
    """Reads in whitelist file."""
    with open(path, "r") as source:
        for line in source:
            line = re.sub(r"\s*#.*$", "", line)  # Removes comments from line.
            yield line.rstrip()


def _filter_write(
    input_tsv_path: str, phones: FrozenSet[str], output_tsv_path: str
) -> None:
    """Creates TSV filtered by whitelist."""
    with open(input_tsv_path, "r") as source, open(
        output_tsv_path, "w"
    ) as sink:
        for line in source:
            line = line.rstrip()
            (word, pron, *_) = line.split("\t", 2)
            these_phones = frozenset(pron.split())
            bad_phones = these_phones - phones
            if bad_phones:
                for phone in bad_phones:
                    logging.warning("Bad phone:\t%s\t(%s)", phone, word)
            else:
                print(line, file=sink)


def main(args: argparse.Namespace) -> None:
    whitelist_phones = frozenset(_whitelist_reader(args.whitelist_path))
    _filter_write(args.input_tsv_path, whitelist_phones, args.output_tsv_path)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tsv_path")
    parser.add_argument("whitelist_path")
    parser.add_argument("output_tsv_path")
    main(parser.parse_args())
