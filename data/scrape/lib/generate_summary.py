#!/usr/bin/env python

import csv
import json
import logging
import operator
import os
from typing import Any, Dict

import pandas

from codes import (LANGUAGES_PATH, LANGUAGES_SUMMARY_PATH, README_PATH,
                   TSV_DIRECTORY)


def _handle_modifiers(
    language: Dict[str, Any],
    file_path: str,
):
    dialects = language.get("dialect", {})
    start = file_path.index("_") + 1
    if "broad" in file_path:
        end = file_path.rindex("_broad") + 1
    else:
        end = file_path.rindex("_narrow") + 1
    script_key = file_path[start : file_path.index("_", start)]
    dialect_key = file_path[
        file_path.index("_", start) + 1 : file_path.rindex("_", start, end)
    ]
    script = language["script"][script_key]
    dialect = dialects.get(dialect_key, "").replace(" |", ",")
    return script, dialect


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
        if "broad" in file_path:
            transcription_level = "Broad"
        else:
            transcription_level = "Narrow"
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
    # Sorts by path to TSV.
    summaries.sort(key=operator.itemgetter(0))
    readme_list.sort(key=operator.itemgetter(0))
    # Writes the TSV.
    with open(LANGUAGES_SUMMARY_PATH, "w", encoding="utf-8") as sink:
        tsv_writer = csv.writer(sink, delimiter="\t", lineterminator="\n")
        tsv_writer.writerows(summaries)
    # Writes the README.
    with open(README_PATH, "w", encoding="utf-8") as sink:
        print(
            "| Link | ISO 639-3 Code | ISO 639 Language Name "
            "| Wiktionary Language Name | Script | Dialect | Filtered "
            "| Narrow/Broad | Case-folding | # of entries |",
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
    table = pandas.read_csv(
        LANGUAGES_SUMMARY_PATH,
        sep="\t",
        names=[
            "link",
            "iso_639_2_code",
            "iso_639_language_name",
            "wiktionary_language_name",
            "script",
            "dialect",
            "filtered",
            "narrow_broad",
            "case_folding",
            "no_entries",
        ],
    )
    # Somewhat arbitrarily, we use the ISO 639-2 code as the "real" label for
    # languages.
    languages = table.iso_639_2_code.nunique()
    print(f"Languages:\t{languages:,}")
    broad_files = table["narrow_broad"].value_counts()["Broad"]
    narrow_files = table["narrow_broad"].value_counts()["Narrow"]
    # We don't currently have any case where multiple languages have a
    # "southern" vs. a "northern" dialect, but just in case, we use this
    # slightly more complex logic here.
    dialects = table.groupby(["iso_639_2_code", "dialect"]).ngroups
    print(f"Dialects:\t{dialects:,}")
    df = table[table["dialect"] != ""]
    grouped_counts = (
        df.groupby(["iso_639_2_code", "dialect", "narrow_broad"])
        .size()
        .unstack(fill_value=0)
    )
    narrow_pairs_files = grouped_counts["Narrow"].sum()
    broad_pairs_files = grouped_counts["Broad"].sum()
    scripts = table.script.nunique()
    print(f"Scripts:\t{scripts:,}")
    # We only count "unfiltered" pronunciations, since filtered ones are a
    # strict subset thereof. Note that this gives us a smaller number than
    # previously reported, but it seems more correct.
    entries = table[~table.filtered].no_entries.sum()
    print(f"Entries:\t{entries:,}")

    bullet_list = (
        f"* Languages: {languages} \n"
        f"\t* Broad transcription files: {broad_files} \n"
        f"\t* Narrow transcription files: {narrow_files} \n"
        f"* Languages & dialects: {dialects} \n"
        f"\t* Broad transcription files: {broad_pairs_files} \n"
        f"\t* Narrow transcription files: {narrow_pairs_files} \n"
        f"* Scripts: {scripts} \n"
        f"* Pronunciations: {entries:,}\n\n"
    )
    with open(README_PATH, "r") as original:
        data = original.read()
    with open(README_PATH, "w") as modified:
        modified.write(bullet_list + data)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
