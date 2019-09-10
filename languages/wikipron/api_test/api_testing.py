# The alternative to outputting two tsv files is to construct lists in each scrape call of all tuples, compare lengths, and then run another for loop writing the larger list to a tsv file. 

# Should I set enconding for these with open statements?

import wikipron
from language_samples import languages

# Needs new line at start.
readme_string = '''
| Link | ISO 639-2 Code | ISO 639 Language Name | Wiktionary Language Name | Case-folding | Phonetic/Phonemic | # of entries |
| :---- | :----: | :----: | :----: | :----:| :----: | ----: |
'''

for iso639_code in languages:
  row = [iso639_code, languages[iso639_code]["iso639_name"], languages[iso639_code]["wiktionary_name"], str(languages[iso639_code]["casefold"])]
  phonemic_iterator = 0
  phonetic_iterator = 0

  config = wikipron.Config(key=iso639_code, casefold=languages[iso639_code]["casefold"])
  for (word, pron) in wikipron.scrape(config):
    phonemic_iterator += 1
    with open(iso639_code + ".tsv", "a") as phonemic_file:
      phonemic_file.write(f"{word}\t{pron}\n")

  phonetic_config = wikipron.Config(key=iso639_code, casefold=languages[iso639_code]["casefold"], phonetic=True)
  for (word, pron) in wikipron.scrape(phonetic_config):
    phonetic_iterator += 1
    with open(iso639_code + "_phonetic" + ".tsv", "a") as phonetic_file:
      phonetic_file.write(f"{word}\t{pron}\n")

  # Perhaps should do something if they  are equal.
  if phonemic_iterator >= phonetic_iterator:
    row = [f"[TSV File]({iso639_code}.tsv)"] + row
    row.extend(["Phonemic", str(phonemic_iterator)])
  else:
    row = [f"[TSV File]({iso639_code}_phonetic.tsv)"] + row
    row.extend(["Phonetic", str(phonetic_iterator)])

  readme_string += "| " + " | ".join(row) + " |\n"

  with open("readme_test.md", "a") as readme_file:
    readme_file.write(readme_string)
  
  # Resetting readme_string is only useful after the first language as we no longer need to append headers. 
  readme_string = ''

readme_file.close()