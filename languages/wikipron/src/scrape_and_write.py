import wikipron
from readme_insert import readme_insert
from time import sleep
import requests
import os
import json
import logging


def call_scrape(lang, config, filename_suffix):
    retries = 0

    while retries < 10:
        file = open(f"../tsv/{lang}{filename_suffix}.tsv", "w")
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
        ):
            logging.info(
                "Exception detected while scraping: '%s', '%s'. Restarting.",
                lang, filename_suffix
            )
            # Pause execution for 10 min.
            sleep(600)
            retries += 1
            # Need to close file for it to be truncated when re-opening
            file.close()

    file.close()
    return None


def main():
    logging.basicConfig(
        format="%(module)s %(levelname)s: %(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level="INFO"
    )
    languages_file = open("languages.json", "r")
    LANGUAGES = json.load(languages_file)

    for iso639_code in LANGUAGES:
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
        phonemic_count = call_scrape(iso639_code, phonemic_config, "_phonemic")

        phonetic_config = wikipron.Config(
            key=iso639_code,
            casefold=LANGUAGES[iso639_code]["casefold"],
            phonetic=True,
            no_stress=True,
            no_syllable_boundaries=True
        )
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
            logging.info(
                "Failed to scrape '%s', moving on to next language.",
                LANGUAGES[iso639_code]["wiktionary_name"]
            )
            if os.path.exists(phonemic_path):
                os.remove(phonemic_path)
            if os.path.exists(phonetic_path):
                os.remove(phonetic_path)
            continue
        # Remove files for languages that failed to call scrape altogether
        # or for which wikipron returned nothing
        elif phonemic_count == 0 and phonetic_count == 0:
            logging.info(
                "'%s', returned no entries in phonemic and phonetic settings.",
                LANGUAGES[iso639_code]["wiktionary_name"]
            )
            os.remove(phonemic_path)
            os.remove(phonetic_path)
            continue
        # Remove empty tsv files
        elif phonemic_count == 0:
            logging.info(
                "'%s', has no entries in phonemic transcription.",
                LANGUAGES[iso639_code]["wiktionary_name"]
            )
            os.remove(phonemic_path)
        elif phonetic_count == 0:
            logging.info(
                "'%s', has no entries in phonetic transcription.",
                LANGUAGES[iso639_code]["wiktionary_name"]
            )
            os.remove(phonetic_path)

        # Create link to appropriate tsv file, mark as phonetic or phonemic
        if phonemic_count >= phonetic_count:
            row = [f"[TSV]({iso639_code}_phonemic.tsv)"] + row
            row.extend(["Phonemic", str(phonemic_count)])
        else:
            row = [f"[TSV]({iso639_code}_phonetic.tsv)"] + row
            row.extend(["Phonetic", str(phonetic_count)])

        readme_row_string = "| " + " | ".join(row) + " |\n"
        readme_insert(LANGUAGES[iso639_code], readme_row_string)


if __name__ == "__main__":
    main()
