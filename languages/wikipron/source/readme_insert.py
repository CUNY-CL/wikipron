"""
This is a helper function that is useful only
when want to add to an already built
README table and keep the table
alphabetical according to Wiktionary language name.
If the README table has no language entries and
we know that we are only going to run scrape_and_write.py once
with languages obtained through running codes.py,
then opening the file for appending and running
readme_file.write(readme_string)
is preferable as the languages will already be
in alphabetical order according to their
Wikitionary language name.
"""


def readme_insert(lang_dict, row_string):
    with open("../README.md", "r+") as readme_file:
        readme_list = []
        readme_text = readme_file.read()
        readme_list.extend(readme_text.splitlines(True))
        length = len(readme_list)
        if length <= 3 or lang_dict["wiktionary_name"] > readme_list[length - 1].split("|")[4][1:-1]:
            # Write the input string to the end
            readme_file.write(row_string)
        else:
            for i in range(3, length):
                isolated_name = readme_list[i].split("|")[4][1:-1]
                if isolated_name == lang_dict["wiktionary_name"]:
                    readme_list[i] = row_string
                    break
                if isolated_name > lang_dict["wiktionary_name"]:
                    readme_list.insert(i, row_string)
                    break
            # Rewrite the entire readme
            readme_file.seek(0)
            readme_file.truncate()
            readme_file.write(''.join(readme_list))
