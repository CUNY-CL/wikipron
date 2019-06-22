#!/usr/bin/env python
"""Evaluates sequence model using multiprocessing.

This script assumes the gold and hypothesis data is stored in a two-column TSV
file, one example per line."""


import argparse
import logging
import multiprocessing
import numpy

from typing import Any, Iterator, List, Tuple


Labels = List[Any]


def _edit_distance(x: Labels, y: Labels) -> int:
    # For a more expressive version of the same, see:
    #
    #     https://gist.github.com/kylebgorman/8034009
    idim = len(x) + 1
    jdim = len(y) + 1
    table = numpy.zeros((idim, jdim), dtype=numpy.uint8)
    for i in range(1, idim):
        table[i][0] = 1
    for j in range(1, jdim):
        table[0][j] = 1
    for i in range(1, idim):
        for j in range(1, jdim):
            if x[i - 1] == y[j - 1]:
                # Match operation.
                table[i][j] = table[i - 1][j - 1]
            else:
                c1 = table[i - 1][j]
                c2 = table[i][j - 1]
                c3 = table[i - 1][j - 1]
                table[i][j] = min(c1, c2, c3) + 1
    return int(table[-1][-1])


def _score(gold: str, hypo: str) -> Tuple[int, int]:
    """Computes sufficient statistics for LER calculation."""
    gold_labels = list(gold)
    hypo_labels = list(hypo)
    edits = _edit_distance(gold_labels, hypo_labels)
    if edits:
        logging.warning("Incorrect prediction: %s (predicted: %s)", gold, hypo)
    return (edits, len(gold_labels))


def _tsv_reader(path: str) -> Iterator[Tuple[str, str]]:
    """Reads pairs of strings from a TSV filepath."""
    with open(path, "r") as source:
        for line in source:
            (gold, hypo) = line.rstrip().split("\t", 1)
            yield (gold, hypo)


def main(args):
    # Word-level measures.
    correct = 0
    incorrect = 0
    # Label-level measures.
    total_edits = 0
    total_length = 0
    # Since the edit distance algorithm is quadratic, let's do this with
    # multiprocessing.
    with multiprocessing.Pool() as pool:
        gen = pool.starmap(_score, _tsv_reader(args.tsv_path))
        for (edits, length) in gen:
            if edits == 0:
                correct += 1
            else:
                incorrect += 1
            total_edits += edits
            total_length += length
    logging.info("WER:\t%.4f", incorrect / (correct + incorrect))
    logging.info("LER:\t%.4f", total_edits / total_length)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tsv_path", help="Path to gold/hypo TSV file")
    main(parser.parse_args())
