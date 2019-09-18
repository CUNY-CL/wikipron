import wikipron
from language_samples import LANGUAGES
from datetime import datetime
from time import sleep
import requests
import os



# Readme should be up a diretory.
# TSV files should be in a sister directory.
# This should be in a 'source' directory.

# Change this to while true.
def call_scrape(lang, config, file_extension, retries=0):
  if retries > 3:
    return None

  # Will truncate already existing files if timeout occurs
  file = open(f"{lang}{file_extension}.tsv", "w")
  count = 0
  try: 
    for (word, pron) in wikipron.scrape(config):
      count += 1
      print(f"{word}\t{pron}", file=file)
  except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
    print("Timeout or connection error detected during scrape.", lang, str(datetime.now()), err)
    # Pause execution for 15 min.
    sleep(900)
    retries += 1
    file.close()
    return call_scrape(lang, config, file_extension, retries)

  file.close()
  return count


def main():
  readme_file = open("readme_test.md", "a")

  for iso639_code in LANGUAGES:
    print('Currently running:', LANGUAGES[iso639_code]["wiktionary_name"], iso639_code, str(datetime.now()))

    row = [iso639_code, LANGUAGES[iso639_code]["iso639_name"], LANGUAGES[iso639_code]["wiktionary_name"], str(LANGUAGES[iso639_code]["casefold"])]

    phonemic_config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], no_stress=True, no_syllable_boundaries=True)
    phonetic_config = wikipron.Config(key=iso639_code, casefold=LANGUAGES[iso639_code]["casefold"], phonetic=True, no_stress=True, no_syllable_boundaries=True)

    phonemic_count = call_scrape(iso639_code, phonemic_config, "_phonemic")
    phonetic_count = call_scrape(iso639_code, phonetic_config, "_phonetic")

    # Remove files for languages that failed to be scraped in 4 tries.
    if phonemic_count == None or phonetic_count == None:
      print(f"TOO MANY RETRIES ON {iso639_code} MOVING ON TO NEXT.")
      os.remove(f"{iso639_code}_phonemic.tsv")
      os.remove(f"{iso639_code}_phonetic.tsv")
      continue
    # Remove files for languages that failed to call scrape altogether, or for which wikipron returned nothing
    elif phonemic_count == 0 and phonetic_count == 0:
      print(f"FAILED TO SCRAPE {iso639_code}.")
      os.remove(f"{iso639_code}_phonemic.tsv")
      os.remove(f"{iso639_code}_phonetic.tsv")
      continue 
    # Remove empty tsv files
    elif phonemic_count == 0:
      print(f"{iso639_code} HAS NO ENTRIES IN PHONEMIC TRANSCRIPTION")
      os.remove(f"{iso639_code}_phonemic.tsv")
    elif phonetic_count == 0:
      print(f"{iso639_code} HAS NO ENTRIES IN PHONETIC TRANSCRIPTION")
      os.remove(f"{iso639_code}_phonetic.tsv")

    # Create link to appropriate tsv file, mark as phonetic or phonemic
    if phonemic_count >= phonetic_count:
      row = [f"[TSV]({iso639_code}_phonemic.tsv)"] + row
      row.extend(["Phonemic", str(phonemic_count)])
    else:
      row = [f"[TSV]({iso639_code}_phonetic.tsv)"] + row
      row.extend(["Phonetic", str(phonetic_count)])


    readme_string = "| " + " | ".join(row) + " |\n"
    readme_file.write(readme_string)
    
  readme_file.close()

if __name__ == "__main__":
  main()