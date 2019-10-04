import wikipron
from datetime import datetime
from time import sleep
import requests
import os
import json


def call_scrape(lang, config, file_extension):
    retries = 0

    while retries < 10:
        file = open(f"../tsv/{lang}{file_extension}.tsv", "w")
        count = 0
        try:
            for (word, pron) in wikipron.scrape(config):
                count += 1
                print(f"{word}\t{pron}", file=file)
            file.close()
            return count
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ) as err:
            print(
                "Timeout or connection error detected during scrape.",
                lang, file_extension,
                str(datetime.now()),
                err
            )
            # Pause execution for 30 min.
            sleep(1800)
            retries += 1
            # Need to close file for it to be truncated when re-opening
            file.close()
            pass

    file.close()
    return None


def main():
    readme_file = open("../README.md", "a")
    languages_file = open("languages.json", "r")
    LANGUAGES = json.load(languages_file)

    for iso639_code in LANGUAGES:
        print(
            'Currently running:',
            LANGUAGES[iso639_code]["wiktionary_name"],
            iso639_code,
            str(datetime.now())
        )

        row = [
            iso639_code, LANGUAGES[iso639_code]["iso639_name"],
            LANGUAGES[iso639_code]["wiktionary_name"],
            str(LANGUAGES[iso639_code]["casefold"])
        ]

        phonemic_config = wikipron.Config(
            key=iso639_code,
            casefold=LANGUAGES[iso639_code]["casefold"],
            no_stress=True,
            no_syllable_boundaries=True
        )
        phonetic_config = wikipron.Config(
            key=iso639_code,
            casefold=LANGUAGES[iso639_code]["casefold"],
            phonetic=True,
            no_stress=True,
            no_syllable_boundaries=True
        )

        phonemic_count = call_scrape(iso639_code, phonemic_config, "_phonemic")
        # Skip phonetic if phonemic failed to complete scrape
        if phonemic_count is not None:
            phonetic_count = call_scrape(
                iso639_code,
                phonetic_config,
                "_phonetic"
            )

        phonemic_path = f"../tsv/{iso639_code}_phonemic.tsv"
        phonetic_path = f"../tsv/{iso639_code}_phonetic.tsv"
        # Remove files for languages that failed to be scraped
        # within set amount of retries.
        if phonemic_count is None or phonetic_count is None:
            print(f"TOO MANY RETRIES ON {iso639_code} MOVING ON TO NEXT.")
            if os.path.exists(phonemic_path):
                os.remove(phonemic_path)
            if os.path.exists(phonetic_path):
                os.remove(phonetic_path)
            continue
        # Remove files for languages that failed to call scrape altogether
        # or for which wikipron returned nothing
        elif phonemic_count == 0 and phonetic_count == 0:
            print(f"FAILED TO SCRAPE {iso639_code}.")
            os.remove(phonemic_path)
            os.remove(phonetic_path)
            continue
        # Remove empty tsv files
        elif phonemic_count == 0:
            print(f"{iso639_code} HAS NO ENTRIES IN PHONEMIC TRANSCRIPTION")
            os.remove(phonemic_path)
        elif phonetic_count == 0:
            print(f"{iso639_code} HAS NO ENTRIES IN PHONETIC TRANSCRIPTION")
            os.remove(phonetic_path)

        # Create link to appropriate tsv file, mark as phonetic or phonemic
        if phonemic_count >= phonetic_count:
            row = [f"[TSV](tsv/{iso639_code}_phonemic.tsv)"] + row
            row.extend(["Phonemic", str(phonemic_count)])
        else:
            row = [f"[TSV](tsv/{iso639_code}_phonetic.tsv)"] + row
            row.extend(["Phonetic", str(phonetic_count)])

        readme_row_string = "| " + " | ".join(row) + " |\n"
        readme_file.write(readme_row_string)

    readme_file.close()


if __name__ == "__main__":
    main()
