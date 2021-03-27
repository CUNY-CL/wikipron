#!/usr/bin/env python
"""In-place Unicode normalization.

Takes a file and applies the specified Unicode normalization "in place." In 
order to avoid the issues of reading and writing to the same file at the same
time, this script puts the normalized version of the file argument in a
tempfile, then uses that tempfile to rewrite the original file."""

import argparse
import shutil
import tempfile
import unicodedata


def main(args: argparse.Namespace) -> None:
    with open(args.path, "r") as source, tempfile.NamedTemporaryFile(
        mode="w+", delete=False
    ) as sink:
        for line in source:
            print(unicodedata.normalize(args.norm, line), end="", file=sink)
    shutil.move(sink.name, args.path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="file to modify")
    parser.add_argument(
        "--norm",
        choices=["NFC", "NFD", "NFKC", "NFKD"],
        required=True,
        help="desired Unicode normalization form",
    )
    main(parser.parse_args())
