#!/usr/bin/env python
"""Splits TSV files into new TSV files.

This module identifies the orthographic script present in each file
in data/tsv, splits the file by orthogrpahy and writes,
a new file that is labeled by the orthography that is present in the file.
"""

import argparse
import json
import os

import regex  # type: ignore

from data.scrape.lib.codes import LANGUAGES_PATH, TSV_DIRECTORY


def _generalized_check(script: str, word: str, extension: str) -> bool:
    prop = (
        "Block" if script == "Katakana" or script == "Hiragana" else "Script"
    )
    regex_string = rf"^[\p{{{prop}={script}}}{extension}]+$"
    return bool(regex.match(regex_string, word))


def _iterate_through_file(
    tsv_path: str, output_path: str, unicode_script: str, extension: str
) -> None:
    with open(tsv_path, "r", encoding="utf-8") as source:
        with open(output_path, "w", encoding="utf-8") as output_tsv:
            for line in source:
                word = line.split("\t", 1)[0]
                # Quick fix for egy_phonemic glottal stop filter problem
                if "egy_phonemic.tsv" in tsv_path:
                    if _generalized_check(
                        unicode_script, word, extension + "."
                    ):
                        print(line.rstrip(), file=output_tsv)
                else:
                    if _generalized_check(unicode_script, word, extension):
                        print(line.rstrip(), file=output_tsv)


def main(args: argparse.Namespace) -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as lang_source:
        languages = json.load(lang_source)
    iso639_code = args.tsv_path[
        args.tsv_path.rindex("/") + 1 : args.tsv_path.index("_")
    ]
    path_remainder = args.tsv_path[args.tsv_path.index("_") + 1 :]
    if "script" in languages[iso639_code]:
        lang = languages[iso639_code]
        # Hacky way of filtering out the already split scripts.
        for script_prefix in lang["script"]:
            if script_prefix in args.tsv_path:
                # Then this is a previously split file.
                return
        for script_prefix, unicode_script in lang["script"].items():
            output_path = (
                f"{TSV_DIRECTORY}/{iso639_code}_{script_prefix}_"
                f"{path_remainder}"
            )
            _iterate_through_file(
                args.tsv_path, output_path, unicode_script, args.regex_string
            )
        # Removes unsplit files; removing files within a for loop doesn't
        # appear to lead to an error in postprocessing.
        os.remove(args.tsv_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regex_string", help="regex string produced by common_characters.py"
    )
    parser.add_argument("tsv_path", help="path to TSV file")
    main(parser.parse_args())
