#!/usr/bin/env python
"""Filters TSVs through a whitelist file.

This script takes lines from a source TSV and writes only lines with
pronunciations containing characters found in the whitelist file to a new TSV."""

import argparse
import re
import sys

from typing import FrozenSet, Iterator


def whitelist_reader(path: str) -> Iterator[str]:
    """Reads in whitelist file."""
    with open(path, "r") as source:
        for line in source:
            # Removes comments from line.
            line = re.sub("\s.*", "", line)
            yield line


def filter_and_write(tsv_path: str, phones: FrozenSet[str], output_path: str) -> None:
    """Creates TSV filtered by whitelist."""
    with open(tsv_path, "r") as source, open(output_path, "w") as output:
        for line in source:
            pron = line.split("\t")[1]
            these_prons = frozenset(pron.split())
            if phones.issuperset(these_prons):
                print(line, file=output, end='')


def main(args: argparse.Namespace) -> None:
    whitelist_phones = frozenset(whitelist_reader(args.whitelist_path))
    filter_and_write(args.tsv_path, whitelist_phones, args.output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv_path", help="path to TSV file to be filtered")
    parser.add_argument("whitelist_path", help="path to whitelist")
    parser.add_argument("output_path", help="path for new TSV")
    main(parser.parse_args())
