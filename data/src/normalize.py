#!/usr/bin/env python
"""In-place unicode normalization.

Takes a file and normalizes it "in place." In order to avoid the issues of
reading and writing to the same file at the same time, this script puts the 
normalized version of the file argument in a tempfile, then uses that
tempfile to rewrite the original file.
"""

import argparse
import tempfile
import unicodedata


def main(args: argparse.Namespace) -> None:
    with tempfile.TemporaryFile(mode="w+") as tf:
        with open(args.file_name, "r") as rf:
            for line in rf:
                print(unicodedata.normalize(args.norm, line), end="", file=tf)
        tf.seek(0)
        with open(args.file_name, "w") as wf:
            for line in tf:
                print(line, end="", file=wf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_name", help="file to modify")
    parser.add_argument(
        "norm",
        choices=["NFC", "NFD", "NFKC", "NFKD"],
        help="desired unicode normalization form",
    )
    main(parser.parse_args())
