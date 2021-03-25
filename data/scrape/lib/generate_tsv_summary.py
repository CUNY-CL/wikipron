#!/usr/bin/env python

import csv
import json
import logging
import os

from typing import Any, Dict, List

from data.scrape.lib.codes import (
    LANGUAGES_PATH,
    README_PATH,
    LANGUAGES_SUMMARY_PATH,
    TSV_DIRECTORY,
)


def _wiki_name_and_transcription_level(ele: List[str]) -> str:
    return ele[3] + ele[7]


def _handle_modifiers(
    language: Dict[str, Any],
    file_path: str,
):
    dialects = language.get("dialect", {})
    start = file_path.index("_") + 1
    end = file_path.rindex("_phon") + 1
    script_key = file_path[start : file_path.index("_", start)]
    dialect_key = file_path[
        file_path.index("_", start) + 1 : file_path.rindex("_", start, end)
    ]
    script = language["script"][script_key]
    dialect = dialects.get(dialect_key, "").replace(" |", ",")
    return script, dialect


def _handle_transcription_level(file_path: str) -> str:
    trans = file_path[
        file_path.index("phone") : file_path.index(".")
    ].capitalize()
    if "_" in trans:
        trans = trans[: trans.index("_")]
    return trans


def main() -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)
    readme_list = []
    summaries = []
    for file_path in os.listdir(TSV_DIRECTORY):
        with open(
            f"{TSV_DIRECTORY}/{file_path}", "r", encoding="utf-8"
        ) as tsv:
            num_of_entries = sum(1 for line in tsv)
        # Removes files with less than 100 entries.
        if num_of_entries < 100:
            # Logs count of entries to check whether Wikipron scraped any data.
            logging.info(
                "%r (count: %d) has less than 100 entries",
                file_path,
                num_of_entries,
            )
            os.remove(f"{TSV_DIRECTORY}/{file_path}")
            continue
        iso639_code = file_path[: file_path.index("_")]
        transcription_level = _handle_transcription_level(file_path)
        wiki_name = languages[iso639_code]["wiktionary_name"]
        filtered = "filtered" in file_path
        script, dialect = _handle_modifiers(languages[iso639_code], file_path)
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
            "| :---- |" + " :----: |" * 8 + " ----: |",
            file=sink,
        )
        for (
            link,
            code,
            iso_name,
            wiki_name,
            script,
            dialect,
            is_filtered,
            phon,
            casefold,
            count,
        ) in readme_list:
            print(
                f"| {link} | {code} | {iso_name} | {wiki_name} | {script} "
                f"| {dialect} | {is_filtered} | {phon} | {casefold} "
                f"| {count:,} |",
                file=sink,
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
