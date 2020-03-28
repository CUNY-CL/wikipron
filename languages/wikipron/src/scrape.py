#!/usr/bin/env python
"""Performs the big scrape."""


import datetime
import json
import logging
import os
import time

import requests
import wikipron


from codes import LANGUAGES_PATH, LOGGING_PATH


def _call_scrape(lang_settings, config, tsv_path):
    for unused_retries in range(10):
        with open(tsv_path, "w") as source:
            try:
                for (word, pron) in wikipron.scrape(config):
                    print(f"{word}\t{pron}", file=source)
                return
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                logging.info(
                    'Exception detected while scraping: "%s", "%s".',
                    lang_settings["key"],
                    tsv_path,
                )
                # Pauses execution for 10 min.
                time.sleep(600)
    # Log and remove TSVs for languages that failed
    # to be scraped within 10 retries.
    logging.info(
        'Failed to scrape "%s" within 10 retries. %s',
        lang_settings["key"],
        lang_settings,
    )
    os.remove(tsv_path)


def _build_scraping_config(
    config_settings, wiki_name, dialect_suffix=""
):
    path_affix = f'../tsv/{config_settings["key"]}_{dialect_suffix}'

    phonemic_config = wikipron.Config(**config_settings)
    phonemic_path = f"{path_affix}phonemic.tsv"
    _call_scrape(config_settings, phonemic_config, phonemic_path)

    phonetic_config = wikipron.Config(phonetic=True, **config_settings)
    phonetic_path = f"{path_affix}phonetic.tsv"
    _call_scrape(config_settings, phonetic_config, phonetic_path)


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    # "2020-01-15" (Big Scrape 3)
    cut_off_date = datetime.date.today().isoformat()
    for iso639_code in languages:
        # config_settings = {
        #     "key": iso639_code,
        #     "casefold": languages[iso639_code]["casefold"],
        #     "no_stress": True,
        #     "no_syllable_boundaries": True,
        #     "cut_off_date": cut_off_date,
        # }
        config_settings = {
            **languages[iso639_code],
            "cut_off_date": cut_off_date,
        }
        if "dialect" not in languages[iso639_code]:
            _build_scraping_config(
                config_settings, languages[iso639_code]["wiktionary_name"]
            )
        else:
            for (dialect_key, dialect_value) in languages[iso639_code][
                "dialect"
            ].items():
                # Overwrite dialect list if present
                config_settings["dialect"] = dialect_value
                _build_scraping_config(
                    config_settings,
                    languages[iso639_code]["wiktionary_name"],
                    dialect_key + "_",
                )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(LOGGING_PATH, mode="a"),
            logging.StreamHandler(),
        ],
        datefmt="%d-%b-%y %H:%M:%S",
        level="INFO",
    )
    main()
