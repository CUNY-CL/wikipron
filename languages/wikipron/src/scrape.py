#!/usr/bin/env python
"""Performs the big scrape."""


import datetime
import json
import logging
import time
import os

import requests
import wikipron


from codes import LANGUAGES_PATH, LOGGING_PATH


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
                    'Exception detected while scraping: "%s", "%s".',
                    lang,
                    tsv_path,
                )
                # Pauses execution for 10 min.
                time.sleep(600)


def build_config_and_filter_scrape_results(
    config_settings, wiki_name, dialect_suffix=""
):
    path_affix = f'../tsv/{config_settings["key"]}_{dialect_suffix}'

    phonemic_config = wikipron.Config(**config_settings)
    phonemic_path = f"{path_affix}phonemic.tsv"
    phonemic_count = _call_scrape(
        config_settings["key"], phonemic_config, phonemic_path
    )

    phonetic_config = wikipron.Config(phonetic=True, **config_settings)
    phonetic_path = f"{path_affix}phonetic.tsv"
    # Skips phonetic if phonemic failed to complete scrape.
    if phonemic_count is not None:
        phonetic_count = _call_scrape(
            config_settings["key"], phonetic_config, phonetic_path
        )
    # Remove files for languages that failed to be scraped
    # within set amount of retries. These langauges
    # will need to be run again.
    if phonemic_count is None or phonetic_count is None:
        logging.info(
            'Failed to scrape "%s", moving on to next language. %s',
            wiki_name,
            {config_settings["key"]: config_settings},
        )
        # Logging the error here would be potentially confusing
        # as encountering an error removing the phonetic TSV
        # file after the phonemic scrape fails to complete is expected.
        # Files that genuinely fail to be removed will be
        # overwritten when rerunning failed languages.
        try:
            os.remove(phonemic_path)
        except FileNotFoundError:
            pass
        try:
            os.remove(phonetic_path)
        except FileNotFoundError:
            pass
        return
    # Remove files for languages that returned nothing.
    # WikiPron is unable to scrape these languages.
    if not phonemic_count and not phonetic_count:
        logging.info(
            '"%s" returned no entries in phonemic and phonetic settings.',
            wiki_name,
        )
        os.remove(phonemic_path)
        os.remove(phonetic_path)
        return
    # Removes TSV files with less than 100 entries.
    if phonemic_count < 100:
        logging.info(
            '"%s" has less than 100 entries in phonemic transcription.',
            wiki_name,
        )
        os.remove(phonemic_path)
    if phonetic_count < 100:
        logging.info(
            '"%s" has less than 100 entries in phonetic transcription.',
            wiki_name,
        )
        os.remove(phonetic_path)


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    cut_off_date = datetime.date.today().isoformat()
    for iso639_code in languages:
        config_settings = {
            "key": iso639_code,
            "casefold": languages[iso639_code]["casefold"],
            "no_stress": True,
            "no_syllable_boundaries": True,
            "cut_off_date": cut_off_date,
        }
        if "dialect" not in languages[iso639_code]:
            build_config_and_filter_scrape_results(
                config_settings, languages[iso639_code]["wiktionary_name"]
            )
        else:
            for dialect_key in languages[iso639_code]["dialect"]:
                config_settings["dialect"] = (
                    languages[iso639_code]["dialect"][dialect_key],
                )
                build_config_and_filter_scrape_results(
                    config_settings,
                    languages[iso639_code]["wiktionary_name"],
                    dialect_key + "_",
                )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(LOGGING_PATH, mode="w"),
            logging.StreamHandler(),
        ],
        datefmt="%d-%b-%y %H:%M:%S",
        level="INFO",
    )
    main()
