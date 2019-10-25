import os
import json
import csv

from codes import LANGUAGES_PATH, README_PATH, LANGUAGES_SUMMARY_PATH


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    readme_list = []
    languages_summary_list = []
    path = "../tsv"
    for file in os.listdir(path):
        # Filter out README.md file
        if file.endswith(".md"):
            continue
        with open(f"{path}/{file}", "r") as tsv:
            num_of_entries = sum(1 for line in tsv)
        iso639_code = file[: file.index("_")]
        transcription_level = file[
            file.rindex("_") + 1: file.index(".")
        ].capitalize()
        wiki_name = languages[iso639_code]["wiktionary_name"]
        if "dialect" in languages[iso639_code]:
            dialect_key = file[file.index("_") + 1: file.rindex("_")]
            dialects = languages[iso639_code]["dialect"][dialect_key]
            if "|" in dialects:
                dialects = dialects.replace(" |", ",")
            wiki_name += f" ({dialects})"

        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            wiki_name,
            str(languages[iso639_code]["casefold"]),
            transcription_level,
            str(num_of_entries),
        ]
        # TSV and README have different first column.
        languages_summary_list.append([file] + row)
        readme_list.append([f"[TSV]({file})"] + row)

    # Sort by wiktionary language name,
    # with phonemic entries before phonetic
    def sorting(ele):
        return ele[3] + ele[5]
    languages_summary_list.sort(key=sorting)
    readme_list.sort(key=sorting)

    # Write the TSV
    with open(LANGUAGES_SUMMARY_PATH, "w") as source:
        tsv_writer_object = csv.writer(source, delimiter="\t")
        tsv_writer_object.writerows(languages_summary_list)
    # Write the README
    with open(README_PATH, "w") as source:
        headers = [
            [
                "Link", "ISO 639-2 Code", "ISO 639 Language Name",
                "Wiktionary Language Name", "Case-folding",
                "Phonetic/Phonemic", "# of entries",
            ],
            [
                ":----", ":----:", ":----:", ":----:",
                ":----:", ":----:", "----:",
            ]
        ]
        readme_list = headers + readme_list
        formatted_and_converted_to_strings = [
            "| " + " | ".join(ele) + " |\n" for ele in readme_list
        ]
        source.writelines(formatted_and_converted_to_strings)


if __name__ == "__main__":
    main()
