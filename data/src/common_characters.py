#!/usr/bin/env python
"""Creates JSON file containing list of "Common" for each language

This module takes TSV files from data and writes a JSON file for
each language TSV file in data/tsv that lists the Unicode
typed "Common" and "Inherited" characters that appear
in each language TSV file -
common_char_summary_by_lang.

It also writes a JSON file that includes a full
"Common" and "Inherited" character set for all files -
global_common_char_summary.json.

Last, it prints an updated regex string for _generalized_check()
in split.py
"""

import os
import json
import unicodedata

from typing import Dict, List, Optional

import regex  # type: ignore
import unicodedataplus  # type: ignore

from codes import (
    TSV_DIRECTORY_PATH,
    COMMMON_CHAR_LIST_PATH,
    GLOBAL_COMMMON_CHAR_LIST_PATH,
)


def _extend_regex(
    accepted_chars: List[str], master_set: Dict[str, Dict[str, str]]
) -> str:
    extension_str = r"\s’ʔʻ"
    for char_type, symbol in master_set.items():
        if char_type == "Common":
            for char, char_symbol in symbol.items():
                if char in accepted_chars:
                    if char_symbol not in extension_str:
                        extension_str += char_symbol
            pass
        if char_type == "Inherited":
            for char, char_symbol in symbol.items():
                if char_symbol not in extension_str:
                    extension_str += char_symbol
    return extension_str


def _is_common(word: str) -> Optional[str]:
    """Returns "Common" characters if a "Common" character
    is present in the word.
    """
    regex_string = r"[\s]+"
    for char in word:
        if unicodedataplus.script(char) == "Common":
            # Checks if Common character is a space
            if not bool(regex.search(regex_string, word)):
                return char
    return None

def _inherited_check(word: str) -> Optional[str]:
    """Returns "Common" characters if a "Common" character
    is present in the word.
    """
    for char in word:
        char_type = unicodedataplus.script(char)
        if char_type == "Inherited":
            # Checks if Common character is a space
            if not bool(regex.search(r"[\s]+", word)):
                return char
    return None 

def main() -> None:
    # List of commmon type Unicode characters
    # that will be included in regex string.
    accepted_list = [
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

    # Creates a dictionary of special characters contained in each file
    master_set: Dict[str, Dict[str, Dict[str, str]]] = {}
    for src in sorted(os.listdir(TSV_DIRECTORY_PATH)):
        iso639_code = src[: src.index("_")]
        path_remainder = src[src.index("_") + 1 :]
        with open(
            f"{TSV_DIRECTORY_PATH}/{src}", "r", encoding="utf=8"
        ) as source:
            master_set[f"{iso639_code}_{path_remainder}"] = {}
            master_set[f"{iso639_code}_{path_remainder}"] = {}
            master_set[f"{iso639_code}_{path_remainder}"]["Common"] = {}
            master_set[f"{iso639_code}_{path_remainder}"]["Inherited"] = {}
            for line in source:
                word = line.split("\t", 1)[0]
                # checks if word contains Common type character
                char = _is_common(word)
                # checks if word contains Inherited type character
                inh_char = _inherited_check(word)
                # If Common character is found, character added to master_set
                # Common key
                if char is not None:
                    char_name = unicodedata.name(char)
                    if (
                        char_name
                        not in master_set[f"{iso639_code}_{path_remainder}"][
                            "Common"
                        ].keys()
                    ):
                        master_set[f"{iso639_code}_{path_remainder}"][
                            "Common"
                        ][char_name] = char
                # If Inherited character is found, character added
                # to master_set Inherited key
                if inh_char is not None:
                    inh_char_name = unicodedata.name(inh_char)
                    if (
                        inh_char_name
                        not in master_set[f"{iso639_code}_{path_remainder}"][
                            "Inherited"
                        ].keys()
                    ):
                        master_set[f"{iso639_code}_{path_remainder}"][
                            "Inherited"
                        ][inh_char_name] = inh_char
        with open(COMMMON_CHAR_LIST_PATH, "w", encoding="utf-8") as write_path:
            json.dump(master_set, write_path, ensure_ascii=False, indent=4)
    # Creates global master common/inherited set.
    global_set: Dict[str, Dict[str, str]] = {}
    global_set["Common"] = {}
    global_set["Inherited"] = {}
    for symbol in master_set.values():
        for char_type, char_symbol in symbol.items():
            if char_type == "Common":
                global_set["Common"].update(char_symbol)
            if char_type == "Inherited":
                global_set["Inherited"].update(char_symbol)
    with open(
        GLOBAL_COMMMON_CHAR_LIST_PATH, "w", encoding="utf-8"
    ) as write_path:
        json.dump(global_set, write_path, ensure_ascii=False, indent=4)
    # Prints extended regex string with acceptable
    # Common and Inherited char types for
    # _generalized_check in split.py
    print(_extend_regex(accepted_list, global_set))


if __name__ == "__main__":
    main()
