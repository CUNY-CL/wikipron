#!/usr/bin/env python

import csv
import json
import logging
import os

from typing import Any, Dict, List

from data.src.codes import LANGUAGES_PATH, PHONES_DIRECTORY_PATH


def _wiki_name_and_transcription_level(ele: List[str]) -> str:
    return ele[3] + ele[4]


def _handle_wiki_name(
    language: Dict[str, Any], file_path: str, modifiers: List[str]
) -> str:
    name = language["wiktionary_name"]
    for modifier in modifiers:
        if modifier in language:
            key = file_path[file_path.index("_") + 1 : file_path.rindex("_phone")]
            if not key:
                logging.info(
                    "Failed to isolate key for %r modifier in %r",
                    modifier,
                    file_path,
                )
                continue
            values = language[modifier][key]
            if "|" in values:
                values = values.replace(" |", ",")
            name += f" ({values})"
    return name


def main() -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)
    readme_list = []
    languages_summary_list = []
    path = "../phones"
    modifiers = ["dialect", "script"]

    for file_path in os.listdir(path):
        # Filters out README.md.
        if file_path.endswith(".md"):
            continue
        with open(f"{path}/{file_path}", "r", encoding="utf-8") as phone_list:
            num_of_entries = sum(1 for line in phone_list)
        iso639_code = file_path[: file_path.index("_")]
        transcription_level = file_path[
            file_path.index("phone") : file_path.index(
                "."
            )  # or should I change to `file_path.index("_") + 1`
        ].capitalize()
        wiki_name = _handle_wiki_name(languages[iso639_code], file_path, modifiers)
        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            wiki_name,
            transcription_level,
            num_of_entries,
        ]
        readme_list.append([f"[phone](phones/{file_path})"] + row)
    # Sorts by Wiktionary language name, with phonemic entries before phonetic
    # ones.
    readme_list.sort(key=_wiki_name_and_transcription_level)
    # Writes the README.
    with open(PHONES_DIRECTORY_PATH, "w", encoding="utf-8") as sink:
        print(
            "| Link | ISO 639-2 Code | ISO 639 Language Name "
            "| Wiktionary Language Name |"
            "| Phonetic/Phonemic | # of phones |",
            file=sink,
        )
        print(
            "| :---- | :----: | :----: | :----: | :----: | :----: |",
            file=sink,
        )
        for link, code, iso_name, wiki_name, ph, count in readme_list:
            print(
                f"| {link} | {code} | {iso_name} | {wiki_name} | {ph} "
                f"| {count:,} |",
                file=sink,
            )


if __name__ == "__main__":
    logging.basicConfig(format="%(filename)s %(levelname)s: %(message)s", level="INFO")
    main()
