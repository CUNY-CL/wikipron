readme_list = []
# Sample inputs
# inp = "Basque"
# inp_str = "| [TSV](tsv_files/baq_phonemic.tsv) | baq | Basque | Basque | True | Phonemic | 220 |\n"

with open("../README.md", "r+") as readme_file:
    text = readme_file.read()
    readme_list.extend(text.splitlines(True))
    length = len(readme_list)
    # If the list is empty, or the last entry in the readme is alphabetically prior to the input string
    if length <= 3 or inp > readme_list[length - 1].split("|")[4][1:-1]:
        # Write the input string to the end
        readme_file.write(inp_str)
    else:    
        for j in range(3, length):
            isolated_name = readme_list[j].split("|")[4][1:-1]
            if isolated_name == inp:
                readme_list[j] = inp_str
                break
            if isolated_name > inp:
                readme_list.insert(j, inp_str)
                break
        # Rewrite the entire readme
        readme_file.seek(0)
        readme_file.truncate()
        readme_file.write(''.join(readme_list))