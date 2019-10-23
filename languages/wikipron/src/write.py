import os
import json

def _readme_insert(wiki_name, row_string):
    with open("../tsv/README.md", "r+") as source:
        readme_list = []
        readme_text = source.read()
        readme_list.extend(readme_text.splitlines(True))
        length = len(readme_list)
        wiki_name_of_last_entry = readme_list[-1].split("|")[4][1:-1]
        # If the table is only a newline, a row of headers, and a formatting row
        # or if the Wiktionary name of the last entry is alphabetically prior to
        # the name we are adding.
        if (
            length == 3
            or wiki_name > wiki_name_of_last_entry
        ):
            # Write the input string to the end
            source.write(row_string)
        else:
            for i in range(3, length):
                isolated_name = readme_list[i].split("|")[4][1:-1]
                # Replaces old row.
                if (
                    isolated_name == wiki_name
                    and row_string.split("|")[6][1:-1] in readme_list[i]
                ):
                    readme_list[i] = row_string
                    break
                # Inserts new row.
                if isolated_name > wiki_name:
                    readme_list.insert(i, row_string)
                    break
            # Rewrite the entire README.
            source.seek(0)
            source.truncate()
            source.write("".join(readme_list))


LANGUAGES_PATH = "languages.json"
with open(LANGUAGES_PATH, "r") as source:
    languages = json.load(source)
readme_tsv_list = []
path = "../tsv"
for file in os.listdir(path):
    # Filters out sole README.md file
    if file.endswith(".tsv"):
        iso639_code = file[:file.find("_")]
        transcription_level = file[file.find("_") + 1:file.find(".")].capitalize()
        with open(f"{path}/{file}", "r") as tsv:
            num_of_entries = sum(1 for line in tsv)

        row = [
            iso639_code,
            languages[iso639_code]["iso639_name"],
            languages[iso639_code]["wiktionary_name"],
            str(languages[iso639_code]["casefold"]),
            transcription_level,
            str(num_of_entries),
        ]
        # TSV of the README will only have the name of the file in the link column.
            # TODO Add additional config options to tsv? Where should the tsv output to?
                # Add main()
        readme_tsv_list.append([file] + row)
        readme_row_string = (
            "| " + " | ".join([f"[TSV]({file})"] + row) + " |\n"
        )
        _readme_insert(languages[iso639_code]["wiktionary_name"], readme_row_string)

# Write the TSV of the README
with open("readme_tsv.tsv", "w") as readme_tsv:
    # Sort by wiktionary language name.
    def sorting(ele):
        return ele[3]
    readme_tsv_list.sort(key=sorting)
    for lang_row in readme_tsv_list:
        tsv_string = "\t".join(lang_row)
        print(tsv_string, file=readme_tsv)