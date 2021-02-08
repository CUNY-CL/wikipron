#!/usr/bin/env python

import collections
import json
import operator
import os
import sys

import regex  # type: ignore
import unicodedataplus

from typing import Dict, Tuple, Union

from data.src.codes import LANGUAGES_PATH, TSV_DIRECTORY_PATH


def _generalized_check(script: str, word: str) -> bool:
    prop = (
        "Block" if script == "Katakana" or script == "Hiragana" else "Script"
    )
    regex_string = rf"^[\p{{{prop}={script}}}']+$"
    return bool(regex.match(regex_string, word))


def _detect_best_script_name(
    word: str, strict: bool = True
) -> Union[Tuple[str, float], None]:
    """Returns the most likely script name (rather than ISO 15924 code) the
    word belongs to along with the corresponding confidence expressed as a
    maximum likelihood estimate computed over the `word` sample. If `strict`
    is enabled, then all the characters must belong to the same script and
    `(None, None)` is returned on failure.

    Example: "ژۇرنال" -> ("Arabic", 1.0).
    """
    script_counts: Dict[str, float] = collections.defaultdict(float)
    for char in word:
        script_counts[unicodedataplus.script(char)] += 1.0
    script_probs = [(s, script_counts[s] / len(word)) for s in script_counts]
    script_probs.sort(key=operator.itemgetter(1), reverse=True)
    if strict and len(script_probs) != 1:
        return None
    else:
        # The script names in Unicode data tables have underscores instead of
        # whitespace to enable parsing. See:
        #   https://www.unicode.org/Public/13.0.0/ucd/Scripts.txt
        return script_probs[0][0].replace("_", " "), script_probs[0][1]


def _iterate_through_file(
    tsv_path: str, output_path: str, unicode_script: str
) -> None:
    with open(tsv_path, "r", encoding="utf-8") as source:
        with open(output_path, "w", encoding="utf-8") as output_tsv:
            for line in source:
                word = line.split("\t", 1)[0]
                if _generalized_check(unicode_script, word):
                    print(line.rstrip(), file=output_tsv)


def main() -> None:
    tsv_path = sys.argv[1]
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as lang_source:
        languages = json.load(lang_source)
    iso639_code = tsv_path[tsv_path.rindex("/") + 1 : tsv_path.index("_")]
    transcription_level = tsv_path[tsv_path.rindex("phone") :]
    if "script" in languages[iso639_code]:
        lang = languages[iso639_code]
        # Hacky way of filtering out the already split scripts.
        for script_prefix in lang["script"]:
            if script_prefix in tsv_path:
                # Then this is a previously split file.
                return
        for script_prefix, unicode_script in lang["script"].items():
            output_path = (
                f"{TSV_DIRECTORY_PATH}/{iso639_code}_{script_prefix}_"
                f"{transcription_level}"
            )
            _iterate_through_file(tsv_path, output_path, unicode_script)
        # Removes unsplit files; removing files within a for loop doesn't
        # appear to lead to an error in postprocessing.
        os.remove(tsv_path)


if __name__ == "__main__":
    main()
