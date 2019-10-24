#!/usr/bin/env python
"""Performs the big scrape."""


import json
import logging
import time
import os

import requests
import wikipron


LANGUAGES_PATH = "languages.json"

def _call_scrape(lang, config, tsv_path):
    for unused_retries in range(10):
        with open(tsv_path, "w") as source:
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
                    tsv_path,
                )
                # Pauses execution for 10 min.
                time.sleep(600)


def build_config_and_filter_scrape_results(config_settings, wiki_name, dialect_extension=''):
    phonemic_config = wikipron.Config(
        **config_settings,
    )
    phonemic_path = f"../tsv/{config_settings['key']}{dialect_extension}_phonemic.tsv"
    phonemic_count = _call_scrape(
        config_settings["key"], phonemic_config, phonemic_path
    )

    phonetic_config = wikipron.Config(
        phonetic=True,
        **config_settings,
    )
    phonetic_path = f"../tsv/{config_settings['key']}{dialect_extension}_phonetic.tsv"
    # Skips phonetic if phonemic failed to complete scrape.
    if phonemic_count is not None:
        phonetic_count = _call_scrape(
            config_settings["key"], phonetic_config, phonetic_path
        )
    
    # Remove files for languages that failed to be scraped
    # within set amount of retries.
    if phonemic_count is None or phonetic_count is None:
        logging.info(
            'Failed to scrape "%s", moving on to next language. %s',
            wiki_name,
            { config_settings["key"]: config_settings }
        )
        if os.path.exists(phonemic_path):
            os.remove(phonemic_path)
        if os.path.exists(phonetic_path):
            os.remove(phonetic_path)
        return
    # Remove files for languages that returned nothing
    elif phonemic_count == 0 and phonetic_count == 0:
        logging.info(
            '"%s", returned no entries in phonemic and phonetic settings.',
            wiki_name,
        )
        os.remove(phonemic_path)
        os.remove(phonetic_path)
        return
    # Removes TSV files with less than 100 entries.
    if phonemic_count < 100:
        logging.info(
            '"%s", has less than 100 entries in phonemic transcription.',
            wiki_name,
        )
        os.remove(phonemic_path)
    if phonetic_count < 100:
        logging.info(
            '"%s", has less than 100 entries in phonetic transcription.',
            wiki_name,
        )
        os.remove(phonetic_path)    


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    for iso639_code in languages:
        config_settings = {
            "key": iso639_code,
            "casefold": languages[iso639_code]["casefold"],
            "no_stress": languages[iso639_code]["no_stress"],
            "no_syllable_boundaries": languages[iso639_code]["no_syllable_boundaries"],
            "cut_off_date": languages[iso639_code]["cut_off_date"],
        }
        # Assumes we will not want to scrape solely for 'eng'/'spa',
        # but always for 'eng'/'spa' with dialect specification.
        if "dialect" in languages[iso639_code]:
            config_settings["require_dialect_label"] = languages[iso639_code]["require_dialect_label"]
            for dialect_key in languages[iso639_code]["dialect"]:
                config_settings["dialect"] = languages[iso639_code]["dialect"][dialect_key]
                build_config_and_filter_scrape_results(config_settings, languages[iso639_code]["wiktionary_name"], dialect_key)
        else:
            build_config_and_filter_scrape_results(config_settings, languages[iso639_code]["wiktionary_name"])
                



if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler("scraping.log", mode="w"),
            logging.StreamHandler()
        ],
        datefmt="%d-%b-%y %H:%M:%S",
        level="INFO",
    )
    main()
