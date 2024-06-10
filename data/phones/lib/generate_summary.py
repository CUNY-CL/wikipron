#!/usr/bin/env python

import csv
import json
import logging
import operator
import os

from typing import Any, Dict

LIB_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PHONES_DIRECTORY = os.path.normpath(os.path.join(LIB_DIRECTORY, os.pardir))
PHONES_README_PATH = os.path.join(PHONES_DIRECTORY, "README.md")
PHONES_SUMMARY_PATH = os.path.join(PHONES_DIRECTORY, "summary.tsv")
PHONES_PHONES_DIRECTORY = os.path.join(PHONES_DIRECTORY, "phones")
LANGUAGES_PATH = os.path.normpath(
    os.path.join(PHONES_DIRECTORY, os.pardir, "scrape/lib/languages.json")
)


def _handle_wiki_name(language: Dict[str, Any], file_path: str) -> str:
    name = language["wiktionary_name"]
    if "dialect" in language:
        key = file_path[file_path.index("_") + 1 : file_path.rindex("_")]
        if not key:
            logging.info(
                "Failed to isolate key for dialect modifier in %r",
                file_path,
            )
        values = language["dialect"][key]
        if "|" in values:
            values = values.replace(" |", ",")
        name += f" ({values})"
    return name


def main() -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)
    readme_list = []
    phones_summaries = []
    for file_path in os.listdir(PHONES_PHONES_DIRECTORY):
        with open(
            f"{PHONES_PHONES_DIRECTORY}/{file_path}", "r", encoding="utf-8"
        ) as phone_list:
            # We exclude blank lines and comments.
            num_of_entries = sum(
                1
                for line in phone_list
                if line.strip() and not line.startswith("#")
            )
        iso639_code = file_path[: file_path.index("_")]
        if "broad" in file_path:
            transcription_level = "Broad"
        else:
            transcription_level = "Narrow"
        wiki_name = _handle_wiki_name(languages[iso639_code], file_path)
        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            wiki_name,
            transcription_level,
            num_of_entries,
        ]
        phones_summaries.append([file_path] + row)
        readme_list.append([f"[phone](phones/{file_path})"] + row)
    # Sorts by path to TSV.
    phones_summaries.sort(key=operator.itemgetter(0))
    readme_list.sort(key=operator.itemgetter(0))
    with open(PHONES_SUMMARY_PATH, "w", encoding="utf-8") as sink:
        tsv_writer_object = csv.writer(
            sink, delimiter="\t", lineterminator="\n"
        )
        tsv_writer_object.writerows(phones_summaries)
    # Writes the README.
    with open(PHONES_README_PATH, "w", encoding="utf-8") as sink:
        print(
            "See the [HOWTO](HOWTO.md) for the steps to generate phone lists.",
            file=sink,
        )
        print(
            "| Link | ISO 639-3 Code | ISO 639 Language Name "
            "| Wiktionary Language Name "
            "| Narrow/broad | # of phones |",
            file=sink,
        )
        print("| :---- " * 5 + "| ----: |", file=sink)
        for link, code, iso_name, wiki_name, ph, count in readme_list:
            print(
                f"| {link} | {code} | {iso_name} | {wiki_name} | {ph} "
                f"| {count:,} |",
                file=sink,
            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
