#!/usr/bin/env python
"""Creates JSON file containing list of "Common" for each language.

This module takes TSV files from data and prints an updated regex string to be
passed to `split.py`.

If --json is enabled, it also writes JSON files which indicate which 
"Common" and "Inherited" characters appear in each language."""

import argparse
import json
import os
import unicodedata

from typing import Dict, List, Optional

import regex  # type: ignore
import unicodedataplus  # type: ignore

from codes import (
    COMMON_CHARS_PATH,
    GLOBAL_COMMON_CHARS_PATH,
    TSV_DIRECTORY,
)

# List of commmon type Unicode characters included in the regex string.
COMMON_ACCEPTED = [
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
]


def _extend_regex(
    accepted_chars: List[str], common_chars: Dict[str, Dict[str, str]]
) -> str:
    extension = ["\s", "’", "ʔ", "ʻ"]
    for char_type, symbol in common_chars.items():
        if char_type == "Common":
            for char, char_symbol in symbol.items():
                if char in accepted_chars:
                    if char_symbol not in extension:
                        extension.append(char_symbol)
            pass
        if char_type == "Inherited":
            for char, char_symbol in symbol.items():
                if char_symbol not in extension:
                    extension.append(char_symbol)
    return "".join(extension)


def _is_common(word: str) -> Optional[str]:
    """Returns any Common characters."""
    for char in word:
        if unicodedataplus.script(char) == "Inherited":
            # Space characters don't count.
            if regex.search(r"[\s]+", word):
                continue
            return char
    return None


def _inherited_check(word: str) -> Optional[str]:
    """Returns any Inherited characters."""
    for char in word:
        if unicodedataplus.script(char) == "Inherited":
            # Space characters don't count.
            if regex.search(r"[\s]+", word):
                continue
            return char
    return None


def main(args: argparse.Namespace) -> None:
    # Creates a dictionary of special characters contained in each file.
    common_chars: Dict[str, Dict[str, Dict[str, str]]] = {}
    for src in sorted(os.listdir(TSV_DIRECTORY)):
        iso639_code = src[: src.index("_")]
        path_remainder = src[src.index("_") + 1 :]
        with open(f"{TSV_DIRECTORY}/{src}", "r", encoding="utf=8") as source:
            ptr = common_chars[f"{iso639_code}_{path_remainder}"] = {}
            ptr["Common"] = {}
            ptr["Inherited"] = {}
            for line in source:
                word = line.split("\t", 1)[0]
                # Checks if word contains Common character.
                char = _is_common(word)
                # Checks if word contains Inherited character.
                inh_char = _inherited_check(word)
                if char is not None:
                    char_name = unicodedata.name(char)
                    if char_name not in ptr["Common"]:
                        ptr["Common"][char_name] = char
                if inh_char is not None:
                    inh_char_name = unicodedata.name(inh_char)
                    if inh_char_name not in ptr["Inherited"]:
                        ptr["Inherited"][inh_char_name] = inh_char
        if args.summaries:
            with open(COMMON_CHARS_PATH, "w", encoding="utf-8") as sink:
                json.dump(common_chars, sink, ensure_ascii=False, indent=4)
    # Creates global common_chars common/inherited set.
    global_common_chars: Dict[str, Dict[str, str]] = {}
    global_common_chars["Common"] = {}
    global_common_chars["Inherited"] = {}
    for symbol in common_chars.values():
        for char_type, char_symbol in symbol.items():
            if char_type in ("Common", "Inherited"):
                global_common_chars[char_type].update(char_symbol)
    if args.summaries:
        with open(GLOBAL_COMMON_CHARS_PATH, "w", encoding="utf-8") as sink:
            json.dump(global_common_chars, sink, ensure_ascii=False, indent=4)
    # Prints extended regex string to stdout.
    print(_extend_regex(COMMON_ACCEPTED, global_common_chars))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summaries", action="store_true", help="write JSON summaries?"
    )
    main(parser.parse_args())
