#!/usr/bin/env python

import os
import json
import csv

from codes import LANGUAGES_PATH, README_PATH, LANGUAGES_SUMMARY_PATH


def _wiki_name_and_transcription_level(ele):
    return ele[3] + ele[5]


def _handle_wiki_name(language, file_path, modifiers):
    name = language["wiktionary_name"]
    for modifier in modifiers:
        if modifier in language:
            key = file_path[file_path.index("_") + 1: file_path.rindex("_")]
            values = language[modifier][key]
            if "|" in values:
                values = values.replace(" |", ",")
            name += f" ({values})"
    return name


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    readme_list = []
    languages_summary_list = []
    path = "../tsv"
    modifiers = ["dialect", "script"]
    for file_path in os.listdir(path):
        # Filter out README.md.
        if file_path.endswith(".md"):
            continue
        with open(f"{path}/{file_path}", "r") as tsv:
            num_of_entries = sum(1 for line in tsv)
        iso639_code = file_path[: file_path.index("_")]
        transcription_level = file_path[
            file_path.rindex("_") + 1: file_path.index(".")
        ].capitalize()

        wiki_name = _handle_wiki_name(
            languages[iso639_code], file_path, modifiers
        )

        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            wiki_name,
            str(languages[iso639_code]["casefold"]),
            transcription_level,
            str(num_of_entries),
        ]
        # TSV and README have different first column.
        languages_summary_list.append([file_path] + row)
        readme_list.append([f"[TSV](tsv/{file_path})"] + row)

    # Sort by Wiktionary language name,
    # with phonemic entries before phonetic.
    languages_summary_list.sort(key=_wiki_name_and_transcription_level)
    readme_list.sort(key=_wiki_name_and_transcription_level)

    # Write the TSV.
    with open(LANGUAGES_SUMMARY_PATH, "w") as source:
        tsv_writer_object = csv.writer(
            source, delimiter="\t", lineterminator="\n"
        )
        tsv_writer_object.writerows(languages_summary_list)
    # Write the README.
    with open(README_PATH, "w") as source:
        headers = [
            [
                "Link",
                "ISO 639-2 Code",
                "ISO 639 Language Name",
                "Wiktionary Language Name",
                "Case-folding",
                "Phonetic/Phonemic",
                "# of entries",
            ],
            [
                ":----",
                ":----:",
                ":----:",
                ":----:",
                ":----:",
                ":----:",
                "----:",
            ],
        ]
        readme_list = headers + readme_list
        formatted_and_converted_to_strings = [
            "| " + " | ".join(ele) + " |\n" for ele in readme_list
        ]
        source.writelines(formatted_and_converted_to_strings)


if __name__ == "__main__":
    main()
