import wikipron
from language_samples import LANGUAGES
from datetime import datetime

def main():
  # Readme file needs to have a blank line below table headers to ensure this gets written to correct place. 
  readme_file = open("readme_test.md", "a")

  for iso639_code in LANGUAGES:
    print('Currently running:', LANGUAGES[iso639_code]["wiktionary_name"], iso639_code, str(datetime.now()))

    row = [iso639_code, LANGUAGES[iso639_code]["iso639_name"], LANGUAGES[iso639_code]["wiktionary_name"], str(LANGUAGES[iso639_code]["casefold"])]
    phonemic_count = 0
    phonetic_count = 0
    phonemic_file = open(iso639_code + '.tsv', 'w')
    phonetic_file = open(iso639_code + '_phonetic' + '.tsv', 'w')

    config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], no_stress=True, no_syllable_boundaries=True)
    for (word, pron) in wikipron.scrape(config):
      phonemic_count += 1
      print(f"{word}\t{pron}", file=phonemic_file)

    phonetic_config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], phonetic=True, no_stress=True, no_syllable_boundaries=True)
    for (word, pron) in wikipron.scrape(phonetic_config):
      phonetic_count += 1
      print(f"{word}\t{pron}", file=phonetic_file)
      

    if phonemic_count >= phonetic_count:
      # Will create link to non-existent tsv file when config call fails - as with 'yue'
      row = [f"[TSV File]({iso639_code}.tsv)"] + row
      row.extend(["Phonemic", str(phonemic_count)])
    else:
      row = [f"[TSV File]({iso639_code}_phonetic.tsv)"] + row
      row.extend(["Phonetic", str(phonetic_count)])

    readme_string = "| " + " | ".join(row) + " |\n"
    readme_file.write(readme_string)
    phonemic_file.close()
    phonetic_file.close()
    
  readme_file.close()

if __name__ == "__main__":
  main()