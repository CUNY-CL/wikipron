#!/usr/bin/env python

import csv
import json
import logging
import os

from typing import Any, Dict, List

from data.src.codes import LANGUAGES_PATH, README_PATH, LANGUAGES_SUMMARY_PATH


def _wiki_name_and_transcription_level(ele: List[str]) -> str:
    return ele[3] + ele[7]

def _get_modifiers(
    language: Dict[str, Any], modifier: str
) -> Dict:
    try:
        return language[modifier]
    except KeyError:
        return {}

def _handle_script(
    language: Dict[str, Any], file_path: str
) -> Dict:
    scripts = _get_modifiers(language, "script")
    key = file_path[
        file_path.index("_") + 1 : file_path.rindex("_phone")
    ]
    if "_" in key:
        key = key[:key.index("_")]
    if key in scripts:
        return scripts[key]
    else:
        return ""

def _handle_dialect(
    language: Dict[str, Any], file_path: str
) -> Dict:
    dialects = _get_modifiers(language, "dialect")
    key = file_path[
        file_path.index("_") + 1 : file_path.rindex("_phone")
    ]
    if "_" in key:
        key = key[key.index("_")+1:]
    if key in dialects:
        return dialects[key]
    else:
        return ""

def _handle_wiki_name(
    language: Dict[str, Any], file_path: str, modifiers: List[str]
) -> str:
    name = language["wiktionary_name"]
    for modifier in modifiers:
        if modifier in language:           
            #print(modifier, language, "\n")
            key = file_path[
                file_path.index("_") + 1 : file_path.rindex("_phone")
            ]
            if not key:
                logging.info(
                    "Failed to isolate key for %r modifier in %r",
                    modifier,
                    file_path,
                )
                continue
            # TODO: remove temporary solution after #365.
            if "_" in key:
                script_key, dialect_key = key.split("_")
                if modifier == "dialect":
                    values = language[modifier][dialect_key]
                elif modifier == "script":
                    values = language[modifier][script_key]
            else:
                values = language[modifier][key]
            if "|" in values:
                values = values.replace(" |", ",")
            name += f" ({values})"
    return name


def main() -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)
    readme_list = []
    summaries = []
    path = "../../data/tsv"
    modifiers = ["dialect", "script"]
    for file_path in os.listdir(path):
        # Filters out README.md.
        if file_path.endswith(".md"):
            continue
        with open(f"{path}/{file_path}", "r", encoding="utf-8") as tsv:
            num_of_entries = sum(1 for line in tsv)
        # Removes files with less than 100 entries.
        if num_of_entries < 100:
            # Logs count of entries to check whether Wikipron scraped any data.
            logging.info(
                "%r (count: %d) has less than 100 entries",
                file_path,
                num_of_entries,
            )
            os.remove(f"{path}/{file_path}")
            continue
        iso639_code = file_path[: file_path.index("_")]
        transcription_level = file_path[
            file_path.index("phone") : file_path.index(".")
        ].capitalize()
        wiki_name = _handle_wiki_name(
            languages[iso639_code], file_path, modifiers
        )	
        filtered = True if "filtered" in file_path else False
        script = _handle_script(languages[iso639_code], file_path)
        dialect = _handle_dialect(languages[iso639_code], file_path)
        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            wiki_name,
            script,
            dialect,
            filtered,
            transcription_level,
            languages[iso639_code]["casefold"],
            num_of_entries,
        ]
        # TSV and README have different first column.
        summaries.append([file_path] + row)
        readme_list.append([f"[TSV](tsv/{file_path})"] + row)
    # Sorts by Wiktionary language name.
    summaries.sort(key=_wiki_name_and_transcription_level)
    readme_list.sort(key=_wiki_name_and_transcription_level)
    # Writes the TSV.
    with open(LANGUAGES_SUMMARY_PATH, "w", encoding="utf-8") as sink:
        tsv_writer = csv.writer(sink, delimiter="\t", lineterminator="\n")
        tsv_writer.writerows(summaries)
    # Writes the README.
    with open(README_PATH, "w", encoding="utf-8") as sink:
        print(
            "| Link | ISO 639-2 Code | ISO 639 Language Name "
            "| Wiktionary Language Name | Script | Dialect | Filtered "
            "| Phonetic/Phonemic | Case-folding | # of entries |",
            file=sink,
        )
        print(
            "| :---- | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | ----: |",
            file=sink,
        )
        for link, code, iso_name, wiki_name, script, dialect, fi, ph, cf, count in readme_list:
            print(
                f"| {link} | {code} | {iso_name} | {wiki_name} | {script} | {dialect} | {fi} | {ph} | {cf} "
                f"| {count:,} |",
                file=sink,
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
