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

OTHER_VALID_IPA = frozenset(
    phone
    for phone in ipapy.UNICODE_TO_IPA.keys()
    if not ipapy.is_valid_ipa(unicodedata.normalize("NFD", phone))
)


def _count_phones(filepath: str) -> Dict[str, Set[str]]:
    """Count the phones in the given TSV file.

    phone_to_examples as Dict[str, Set[str]] is the most straightforward
    data structure for our purposes. It's not memory-efficient
    (with the same word-pron pair appearing in different phones' sets),
    but anything fancier doesn't seem worth the work.
    """
    phone_to_examples = collections.defaultdict(set)
    with open(filepath, encoding="utf-8") as source:
        for line in source:
            line = line.strip()
            if not line:
                continue
            word, pron = line.split("\t", maxsplit=1)
            example = f"({word} | {pron})"
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
    return random.sample(list(examples), n_examples)


def _check_ipa_phonemes(phone_to_examples: Dict[str, Set[str]], filepath: str):
    """Given the phonemes checks whether they are represented in the IPA.

    This will catch problematic phonemes, according to the current IPA standard
    supported by `ipapy`. In addition, it is likely to complain about highly
    specific allophones, which are likely to be present in languages which have
    highly phonetic representation of their phoneme inventory. For a current
    IPA chart, please see:

        https://www.internationalphoneticassociation.org/IPAcharts/IPA_chart_orig/IPA_charts_E.html
    """
    bad_ipa_phonemes = frozenset(
        phone
        for phone in phone_to_examples.keys()
        if not (
            ipapy.is_valid_ipa(unicodedata.normalize("NFD", phone))
            or phone in OTHER_VALID_IPA
        )
    )
    if len(bad_ipa_phonemes) and filepath.endswith("phonemic.tsv"):
        logging.warning("Found %d invalid IPA phones:", len(bad_ipa_phonemes))
        phoneme_id = 1
        for phoneme in bad_ipa_phonemes:
            bad_chars = [
                f"[%d %04x %s %s]"
                % (i, ord(c), unicodedata.category(c), unicodedata.name(c))
                for i, c in enumerate(ipapy.invalid_ipa_characters(phoneme))
            ]
            logging.warning(
                "[%d] Non-IPA transcription: %s (%s)",
                phoneme_id,
                phoneme,
                " ".join(bad_chars),
            )
            phoneme_id += 1


def main(args: argparse.Namespace):
    phone_to_examples: Dict[str, Set[str]] = _count_phones(args.tsv_path)
    for phone, examples in sorted(
        phone_to_examples.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(
            f"{phone}\t# {len(examples):10,}: "
            f"{', '.join(_pick_examples_for_display(examples))}"
        )
    print(f"\n# unique phones: {len(phone_to_examples)}")
    _check_ipa_phonemes(phone_to_examples, args.filepath)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level="INFO")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tsv_path", help="path to TSV file")
    main(parser.parse_args())
