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
"""
import os
import json
import unicodedata

from typing import Dict, Optional

import regex  # type: ignore
import unicodedataplus  # type: ignore

from codes import TSV_DIRECTORY_PATH


def _common_check(word: str) -> Optional[str]:
    """Returns "Common" characters if a "Common" character
    is present in the word.
    """
    regex_string = r"[\s]+"
    for char in word:
        char_type = unicodedataplus.script(char)
        if char_type == "Common":
            # Checks if Common character is a space
            if not bool(regex.search(regex_string, word)):
                return char
    return None


def _inherited_check(word: str) -> Optional[str]:
    """Returns "Common" characters if a "Common" character
    is present in the word.
    """
    regex_string = r"[\s]+"
    for char in word:
        char_type = unicodedataplus.script(char)
        if char_type == "Inherited":
            # Checks if Common character is a space
            if not bool(regex.search(regex_string, word)):
                return char
    return None


def main() -> None:
    with open(
        "common_char_summary_by_lang.json", "w", encoding="utf-8"
    ) as out_path:
        # Creates a dictionary of special characters contained in each file
        master_set: Dict[str, Dict[str, Dict[str, str]]] = {}
        for src in sorted(os.listdir(TSV_DIRECTORY_PATH)):
            iso639_code = src[: src.index("_")]
            path_remainder = src[src.index("_") + 1:]
            with open(
                f"{TSV_DIRECTORY_PATH}/{src}", "r", encoding="utf=8"
            ) as source:
                master_set[f"{iso639_code}_{path_remainder}"] = {}
                master_set[f"{iso639_code}_{path_remainder}"] = {}
                master_set[f"{iso639_code}_{path_remainder}"]["Common"] = {}
                master_set[f"{iso639_code}_{path_remainder}"]["Inherited"] = {}
                for line in source:
                    word = line.split("\t", 1)[0]
                    char = _common_check(word)
                    inh_char = _inherited_check(word)
                    if char is not None:
                        char_name = unicodedata.name(char)
                        if (
                            char_name
                            not in master_set[
                                f"{iso639_code}_{path_remainder}"
                            ]["Common"].keys()
                        ):
                            master_set[f"{iso639_code}_{path_remainder}"][
                                "Common"
                            ][char_name] = char
                    if inh_char is not None:
                        inh_char_name = unicodedata.name(inh_char)
                        if (
                            inh_char_name
                            not in master_set[
                                f"{iso639_code}_{path_remainder}"
                            ]["Inherited"].keys()
                        ):
                            master_set[f"{iso639_code}_{path_remainder}"][
                                "Inherited"
                            ][inh_char_name] = inh_char
        json_object = json.dumps(master_set, ensure_ascii=False, indent=4)
        print(json_object, file=out_path)

    # Create global master common/inherited set.
    global_set: Dict[str, Dict[str, str]] = {}
    global_set["Common"] = {}
    global_set["Inherited"] = {}
    for value in master_set.values():
        for k, v in value.items():
            if k == "Common":
                global_set["Common"].update(v)
            if k == "Inherited":
                global_set["Inherited"].update(v)
    with open(
        "global_common_char_summary.json", "w", encoding="utf-8"
    ) as out_path:
        json_object = json.dumps(global_set, ensure_ascii=False, indent=4)
        print(json_object, file=out_path)


if __name__ == "__main__":
    main()
