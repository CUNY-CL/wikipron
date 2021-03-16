#!/usr/bin/env python
"""Creates json file containing list of "Common" for each language

This module takes TSV files from data and return a json file for 
each language TSV file in data/tsv that lists the unicode 
typed "Common" characters that appear ineach language TSV file.
"""
import os
import json

import regex  # type: ignore
from typing import Optional, Dict
import unicodedata
import unicodedataplus  # type: ignore

from codes import TSV_DIRECTORY_PATH  # type: ignore


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


def main() -> None:
    with open(
        "common_characters_summary.json", "w", encoding="utf-8"
    ) as out_path:
        # Creates a dictionary of special characters contained in each file
        master_set: Dict[str, Dict[str, str]] = {}
        for src in sorted(os.listdir(TSV_DIRECTORY_PATH)):
            print(src)
            iso639_code = src[: src.index("_")]
            path_remainder = src[src.index("_") + 1 :]
            with open(
                f"{TSV_DIRECTORY_PATH}/{src}", "r", encoding="utf=8"
            ) as source:
                master_set[f"{iso639_code}_{path_remainder}"] = {}
                for line in source:
                    word = line.split("\t", 1)[0]
                    char = _common_check(word)
                    if char is not None:
                        char_name = unicodedata.name(char)
                        if (
                            char_name
                            not in master_set[
                                f"{iso639_code}_{path_remainder}"
                            ].keys()
                        ):
                            master_set[f"{iso639_code}_{path_remainder}"][
                                char_name
                            ] = char

        json_object = json.dumps(master_set, ensure_ascii=False, indent=4)
        print(json_object, file=out_path)


if __name__ == "__main__":
    main()
