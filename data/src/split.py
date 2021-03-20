#!/usr/bin/env python

import json
import os
import argparse

from typing import Dict

import regex  # type: ignore

from data.src.codes import LANGUAGES_PATH, TSV_DIRECTORY_PATH, COMMMON_SET_PATH


def _extend_regex(master_set: Dict[str, Dict[str, str]]) -> str:
    extension_str = r"\s’ʔʻ"
    # List of accepted commmon set characters
    accepted_set = (
        "RIGHT SINGLE QUOTATION MARK",
        "MODIFIER LETTER APOSTROPHE",
        "LEFT SINGLE QUOTATION MARK",
        "APOSTROPHE",
        "ZERO WIDTH SPACE",
        "MIDDLE DOT",
        "KATAKANA-HIRAGANA PROLONGED SOUND MARK",
        "KATAKANA MIDDLE DOT",
        "ARABIC TATWEEL",
        "TILDE",
    )
    for key, value in master_set.items():
        if key == "Common":
            for k, v in value.items():
                if k in accepted_set:
                    if v not in extension_str:
                        extension_str += v
            pass
        if key == "Inherited":
            for k, v in value.items():
                if v not in extension_str:
                    extension_str += v
    return extension_str


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
                if _generalized_check(unicode_script, word, extension):
                    print(line.rstrip(), file=output_tsv)


def main(args: argparse.Namespace) -> None:
    with open(COMMMON_SET_PATH, "r", encoding="utf-8") as common_source:
        master_common_set = json.load(common_source)
    regex_extension = _extend_regex(master_common_set)
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as lang_source:
        languages = json.load(lang_source)
    iso639_code = args.tsv_path[
        args.tsv_path.rindex("/") + 1: args.tsv_path.index("_")
    ]
    path_remainder = args.tsv_path[args.tsv_path.index("_") + 1:]
    if "script" in languages[iso639_code]:
        lang = languages[iso639_code]
        # Hacky way of filtering out the already split scripts.
        for script_prefix in lang["script"]:
            if script_prefix in args.tsv_path:
                # Then this is a previously split file.
                return
        for script_prefix, unicode_script in lang["script"].items():
            output_path = (
                f"{TSV_DIRECTORY_PATH}/{iso639_code}_{script_prefix}_"
                f"{path_remainder}"
            )
            _iterate_through_file(
                args.tsv_path, output_path, unicode_script, regex_extension
            )
        # Removes unsplit files; removing files within a for loop doesn't
        # appear to lead to an error in postprocessing.
        os.remove(args.tsv_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="sets path to TSV")
    parser.add_argument("tsv_path", help="path to TSV files")
    namespace = parser.parse_args()
    main(namespace)
