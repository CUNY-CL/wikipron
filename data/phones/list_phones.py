#!/usr/bin/env python

"""This script prints a tally of the phones/phonemes of a WikiPron TSV file.

For each phone/phoneme, this script prints:
- the phone/phoneme
- the number of words that have this phone/phoneme
- a few example word-pronunciation pairs for this phone/phoneme
"""

import argparse
import collections
import ipapy
import random
import unicodedata

from typing import Dict, List, Set


def _count_phones(filepath: str) -> Dict[str, Set[str]]:
    """Count the phones in the given TSV file.

    phone_to_examples as Dict[str, Set[str]] is the most straightforward
    data structure for our purposes. It's not memory-efficient
    (with the same word-pron pair appearing in different phones' sets),
    but anything fancier doesn't seem worth the work.
    """
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


def _pick_examples_for_display(examples: Set[str]) -> List[str]:
    """Pick examples of word-pron pairs for display.

    We could have exposed the maximum number of examples to display
    (set to be 3 now) for each phone to the command-line interface,
    but it doesn't seem worth it for the time being.
    """
    n_examples = min(len(examples), 3)
    # Using list() here because Python 3.9 has deprecated the use
    # of an _unordered_ set as the input to random.sample.
    sample = random.sample(list(examples), n_examples)
    return sample


def main(args: argparse.Namespace):
    phone_to_examples: Dict[str, Set[str]] = _count_phones(args.filepath)
    invalid_phones = set()
    for phone, examples in sorted(
        phone_to_examples.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(
            f"{phone:<5}"
            " # "
            f"{len(examples):<10}"
            f"{', '.join(_pick_examples_for_display(examples))}"
        )
        if not ipapy.is_valid_ipa(phone):
            invalid_phones.add(phone)
    print(f"\n# unique phones: {len(phone_to_examples)}")

    # Check the phoneme inventory for invalid IPA representations.
    if len(invalid_phones) and args.filepath.endswith("phonemic.tsv"):
        print(f"--- WARNING: {len(invalid_phones)} Invalid phones:")
        for phone in invalid_phones:
            print(f"{phone}")
            for i, c in enumerate(ipapy.invalid_ipa_characters(phone)):
                print(
                    "\tBad char: ", i, "%04x" % ord(c), unicodedata.category(c), end=" "
                )
                print(unicodedata.name(c))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filepath", help="Path to TSV scraped by WikiPron")
    args = parser.parse_args()
    main(args)
