#!/usr/bin/env python

import json
import os
import sys

import regex  # type: ignore


def _generalized_check(script: str, word: str) -> bool:
    prop = (
        "Block" if script == "Katakana" or script == "Hiragana" else "Script"
    )
    regex_string = rf"^\p{{{prop}={script}}}+$"
    return bool(regex.match(regex_string, word))


def _iterate_through_file(
    tsv_path: str, output_path: str, unicode_script: str
) -> None:
    with open(tsv_path, "r") as source:
        with open(output_path, "w") as output_tsv:
            for line in source:
                word = line.split("\t", 1)[0]
                if _generalized_check(unicode_script, word):
                    print(line.rstrip(), file=output_tsv)


def main() -> None:
    tsv_path = sys.argv[1]
    with open("languages.json", "r") as lang_source:
        languages = json.load(lang_source)
    iso639_code = tsv_path[tsv_path.rindex("/") + 1:tsv_path.index("_")]
    transcription_level = tsv_path[tsv_path.rindex("_") + 1:]
    if "script" in languages[iso639_code]:
        lang = languages[iso639_code]
        # Hacky way of filtering out the already split scripts.
        for script_prefix in lang["script"]:
            if script_prefix in tsv_path:
                # Then this is a previously split file.
                return
        for script_prefix, unicode_script in lang["script"].items():
            output_path = (
                f"../tsv/{iso639_code}_{script_prefix}_"
                f"{transcription_level}"
            )
            _iterate_through_file(tsv_path, output_path, unicode_script)
        # Removes unsplit files; removing files within a for loop doesn't
        # appear to lead to an error in postprocessing.
        os.remove(tsv_path)


if __name__ == "__main__":
    main()
