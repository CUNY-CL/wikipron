# This function will keep the "../tsv/README.md" table in
# alphabetical order according to Wiktionary language name.


def readme_insert(lang_dict, row_string):
    with open("../tsv/README.md", "r+") as readme_file:
        readme_list = []
        readme_text = readme_file.read()
        readme_list.extend(readme_text.splitlines(True))
        length = len(readme_list)
        wiki_name_of_last_entry = readme_list[-1].split("|")[4][1:-1]
        # If the table is only a newline, a row of headers,
        # and a formatting row;
        # or if the Wiktionary name of the last entry
        # is alphabetically prior to the name we are adding
        if (
              length == 3 or
              lang_dict["wiktionary_name"] > wiki_name_of_last_entry
            ):
            # Write the input string to the end
            readme_file.write(row_string)
        else:
            for i in range(3, length):
                isolated_name = readme_list[i].split("|")[4][1:-1]
                # Replace old row
                if isolated_name == lang_dict["wiktionary_name"]:
                    readme_list[i] = row_string
                    break
                # Insert new row
                if isolated_name > lang_dict["wiktionary_name"]:
                    readme_list.insert(i, row_string)
                    break
            # Rewrite the entire readme
            readme_file.seek(0)
            readme_file.truncate()
            readme_file.write(''.join(readme_list))
