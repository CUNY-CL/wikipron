#!/usr/bin/env python

"""This script prints a tally of the phones/phonemes of a WikiPron TSV file.

For each phone/phoneme, this script prints:
- the phone/phoneme
- the number of words that have this phone/phoneme
- a few example word-pronunciation pairs for this phone/phoneme
"""

import argparse
import collections
import logging
import random
import unicodedata

from typing import Dict, List, Set

import ipapy


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


def _check_ipa_phonemes(
    phone_to_examples: Dict[str, Set[str]], args: argparse.Namespace
):
    """Given the phonemes checks whether they are represented in IPA.

    This will catch problematic phonemes, such as `ú` which are not valid
    according to the current IPA standard supported by `ipapy`. In addition, it
    is likely to complain about highly specific allophones, which are likely
    to be present in languages which have highly phonetic representation of
    their phoneme inventory. For current IPA chart please see:
      https://www.internationalphoneticassociation.org/IPAcharts/IPA_chart_orig/IPA_charts_E.html
    """
    bad_ipa_phonemes = set()
    for phone in phone_to_examples.keys():
        if not ipapy.is_valid_ipa(phone):
            bad_ipa_phonemes.add(phone)

    logger = logging.getLogger(__name__)
    if len(bad_ipa_phonemes) and args.filepath.endswith("phonemic.tsv"):
        logger.warning(f"Found {len(bad_ipa_phonemes)} invalid IPA phonemes:")
        if not logger.isEnabledFor(logging.WARNING):
            return  # Do nothing. Warnings are not logged.
        phoneme_id = 1
        for phoneme in bad_ipa_phonemes:
            bad_chars = [
                f"[%d %04x %s %s]"
                % (i, ord(c), unicodedata.category(c), unicodedata.name(c))
                for i, c in enumerate(ipapy.invalid_ipa_characters(phoneme))
            ]
            logger.warning(
                f"[{phoneme_id}] Problematic: "
                f"{phoneme} {', '.join(bad_chars)}"
            )
            phoneme_id += 1


def main(args: argparse.Namespace):
    phone_to_examples: Dict[str, Set[str]] = _count_phones(args.filepath)
    for phone, examples in sorted(
        phone_to_examples.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(
            f"{phone:<5}"
            " # "
            f"{len(examples):<10}"
            f"{', '.join(_pick_examples_for_display(examples))}"
        )
    print(f"\n# unique phones: {len(phone_to_examples)}")
    _check_ipa_phonemes(phone_to_examples, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filepath", help="Path to TSV scraped by WikiPron")
    args = parser.parse_args()
    main(args)