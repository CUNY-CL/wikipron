#!/usr/bin/env python
"""Makes test file.

Using gold data and the model output, this script creates a three-column TSV
file in which each row contains a word, its gold pronunciation, and the
predicted pronunciation, assuming that the input files have the words listed
in the same order."""

import argparse
import contextlib
import logging

from data.scrape.lib.codes import LOGGING_PATH


def main(args: argparse.Namespace) -> None:
    with contextlib.ExitStack() as stack:
        gf = stack.enter_context(open(args.gold, "r"))
        pf = stack.enter_context(open(args.pred, "r"))
        wf = stack.enter_context(open(args.out, "w"))
        for lineno, (g_line, p_line) in enumerate(zip(gf, pf), 1):
            g_word, g_pron = g_line.rstrip().split("\t", 2)
            p_word, p_pron = p_line.rstrip().split("\t", 2)
            # Ensures the gold data and predictions have the same words.
            if g_word != p_word:
                logging.error("%s != %s (line %d)", g_word, p_word, lineno)
                exit(1)
            print(f"{g_word}\t{p_pron}\t{g_pron}", file=wf)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOGGING_PATH, mode="a"),
            logging.StreamHandler(),
        ],
        level="INFO",
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "gold", help="TSV with words and correct pronunciations"
    )
    parser.add_argument(
        "pred", help="TSV with words and predicted pronunciations"
    )
    parser.add_argument("out", help="output file")
    main(parser.parse_args())
