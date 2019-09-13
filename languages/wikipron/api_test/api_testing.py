import wikipron
from language_samples import LANGUAGES
from datetime import datetime
from time import sleep
import requests
import os

def call_scrape(lang, config, file, retries=0):
  if retries >= 3:
    return None

  count = 0
  try: 
    for (word, pron) in wikipron.scrape(config):
      count += 1
      print(f"{word}\t{pron}", file=file)
  except requests.exceptions.ReadTimeout as err:
    print("Timeout error detected during scrape.", lang, err)
    # Pause execution for 15 min.
    sleep(900)
    retries += 1
    return call_scrape(lang, config, file, retries)

  return count



def main():
  readme_file = open("readme_test.md", "a")

  for iso639_code in LANGUAGES:
    print('Currently running:', LANGUAGES[iso639_code]["wiktionary_name"], iso639_code, str(datetime.now()))

    row = [iso639_code, LANGUAGES[iso639_code]["iso639_name"], LANGUAGES[iso639_code]["wiktionary_name"], str(LANGUAGES[iso639_code]["casefold"])]

    phonemic_config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], no_stress=True, no_syllable_boundaries=True)
    phonetic_config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], phonetic=True, no_stress=True, no_syllable_boundaries=True)

    phonemic_file = open(iso639_code + ".tsv", "w")
    phonetic_file = open(iso639_code + "_phonetic" + ".tsv", "w")

    phonemic_count = call_scrape(iso639_code, phonemic_config, phonemic_file)
    phonetic_count = call_scrape(iso639_code, phonetic_config, phonetic_file)

    # Remove files for languages that failed to be scraped in 4 tries.
    if phonemic_count == None or phonetic_count == None:
      print(f"TOO MANY RETRIES ON {iso639_code} MOVING ON TO NEXT.")
      os.remove(iso639_code + ".tsv")
      os.remove(iso639_code + "_phonetic" + ".tsv")
      continue
    # Remove files for languages that failed to call scrape
    elif phonemic_count == 0 and phonetic_count == 0:
      print(f"FAILED TO CALL SCRAPE ON {iso639_code}.")
      os.remove(iso639_code + ".tsv")
      os.remove(iso639_code + "_phonetic" + ".tsv")
      continue      


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