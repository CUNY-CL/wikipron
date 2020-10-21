#!/usr/bin/env python

"""This script prints a tally of the phones/phonemes of a WikiPron TSV file.

For each phone/phoneme, this script prints:
- the phone/phoneme
- the number of words that have this phone/phoneme
- a few example word-pronunciation pairs for this phone/phoneme
"""

import argparse
import collections
import random

from typing import Dict, Set


def _get_cli_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filepath", help="Path to TSV scraped by WikiPron")
    args = parser.parse_args()
    return args


def _count_phones(filepath):
    phone_to_examples = collections.defaultdict(set)
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            word, pron = line.split("\t", maxsplit=1)
            example = f"( {word} | {pron} )"
            phones = pron.split()
            for phone in phones:
                phone_to_examples[phone].add(example)
    return phone_to_examples


def _pick_examples_for_display(examples: Set[str]) -> Set[str]:
    n_examples = min(len(examples), 3)
    sample = random.sample(list(examples), n_examples)
    return set(sample)


def main():
    args = _get_cli_args()
    phone_to_examples: Dict[str, Set[str]] = _count_phones(args.filepath)
    for phone, examples in sorted(
        phone_to_examples.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(
            f"{phone:<5}"
            f"{len(examples):<10}"
            f"{', '.join(_pick_examples_for_display(examples))}"
        )
    print(f"\n# unique phones: {len(phone_to_examples)}")


if __name__ == "__main__":
    main()
