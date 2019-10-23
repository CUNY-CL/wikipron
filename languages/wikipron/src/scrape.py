#!/usr/bin/env python
"""Performs the big scrape."""


import json
import logging
import time
import os

import requests
import wikipron


LANGUAGES_PATH = "languages.json"

def _call_scrape(lang, config, filename_suffix):
    for unused_retries in range(10):
        with open(f"../tsv/{lang}{filename_suffix}.tsv", "w") as source:
            count = 0
            try:
                for (word, pron) in wikipron.scrape(config):
                    count += 1
                    print(f"{word}\t{pron}", file=source)
                return count
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                logging.info(
                    'Exception detected while scraping: "%s", "%s". Restarting.',
                    lang,
                    filename_suffix,
                )
                # Pauses execution for 10 min.
                time.sleep(600)


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    for iso639_code in languages:
        phonemic_config = wikipron.Config(
            key=iso639_code,
            casefold=languages[iso639_code]["casefold"],
            no_stress=True,
            no_syllable_boundaries=True,
        )
        phonemic_count = _call_scrape(
            iso639_code, phonemic_config, "_phonemic"
        )
        phonetic_config = wikipron.Config(
            key=iso639_code,
            casefold=languages[iso639_code]["casefold"],
            phonetic=True,
            no_stress=True,
            no_syllable_boundaries=True,
        )
        # Skips phonetic if phonemic failed to complete scrape.
        if phonemic_count is not None:
            phonetic_count = _call_scrape(
                iso639_code, phonetic_config, "_phonetic"
            )
        phonemic_path = f"../tsv/{iso639_code}_phonemic.tsv"
        phonetic_path = f"../tsv/{iso639_code}_phonetic.tsv"
        # Remove files for languages that failed to be scraped
        # within set amount of retries.
        if phonemic_count is None or phonetic_count is None:
            logging.info(
                'Failed to scrape "%s", moving on to next language.',
                languages[iso639_code]["wiktionary_name"],
            )
            if os.path.exists(phonemic_path):
                os.remove(phonemic_path)
            if os.path.exists(phonetic_path):
                os.remove(phonetic_path)
            continue
        # Remove files for languages that returned nothing
        elif phonemic_count == 0 and phonetic_count == 0:
            logging.info(
                '"%s", returned no entries in phonemic and phonetic settings.',
                languages[iso639_code]["wiktionary_name"],
            )
            os.remove(phonemic_path)
            os.remove(phonetic_path)
            continue
        # Removes empty TSV files.
        elif phonemic_count == 0:
            logging.info(
                '"%s", has no entries in phonemic transcription.',
                languages[iso639_code]["wiktionary_name"],
            )
            os.remove(phonemic_path)
        elif phonetic_count == 0:
            logging.info(
                '"%s", has no entries in phonetic transcription.',
                languages[iso639_code]["wiktionary_name"],
            )
            os.remove(phonetic_path)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level="INFO",
    )
    main()
