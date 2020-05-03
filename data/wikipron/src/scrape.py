#!/usr/bin/env python
"""Performs the big scrape."""

import argparse
import datetime
import json
import logging
import os
import time

from typing import Any, Dict

import requests
import wikipron  # type: ignore


from codes import LANGUAGES_PATH, LOGGING_PATH


def _call_scrape(
    lang_settings: Dict[str, str], config: wikipron.Config, tsv_path: str
) -> None:
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
    config_settings: Dict[str, Any], wiki_name: str, dialect_suffix: str = ""
) -> None:
    path_affix = f'../tsv/{config_settings["key"]}_{dialect_suffix}'
    phonemic_config = wikipron.Config(**config_settings)
    phonemic_path = f"{path_affix}phonemic.tsv"
    _call_scrape(config_settings, phonemic_config, phonemic_path)
    phonetic_config = wikipron.Config(phonetic=True, **config_settings)
    phonetic_path = f"{path_affix}phonetic.tsv"
    _call_scrape(config_settings, phonetic_config, phonetic_path)


def main(args) -> None:
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)

    ###Checks restriction codes are valid.
    if args.restriction: 
        for key in args.restriction:
            try:
                assert key in languages 
            except AssertionError:
                print("Language restrictions must be valid ISO code.")
                exit()
    ###

    # "2020-01-15" (Big Scrape 3).
    cut_off_date = datetime.date.today().isoformat()
    wikipron_accepted_settings = {
        "casefold": False,
        "no_skip_spaces_pron": False,
        "no_skip_spaces_word": False,
    }

    for iso639_code in languages:

        ###Checks for language restrictions
        if args.restriction and iso639_code not in args.restriction:
            continue
        ###

        language_settings = languages[iso639_code]
        for k, v in language_settings.items():
            if k in wikipron_accepted_settings:
                wikipron_accepted_settings[k] = v
        config_settings = {
            "key": iso639_code,
            "no_stress": True,
            "no_syllable_boundaries": True,
            "cut_off_date": cut_off_date,
            **wikipron_accepted_settings,
        }
        if "dialect" not in language_settings:
            _build_scraping_config(
                config_settings, language_settings["wiktionary_name"]
            )
        else:
            for (dialect_key, dialect_value) in language_settings[
                "dialect"
            ].items():
                config_settings["dialect"] = dialect_value
                _build_scraping_config(
                    config_settings,
                    language_settings["wiktionary_name"],
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

    ###Add parser to limit scope of scrape. 
    parser = argparse.ArgumentParser()
    parser.add_argument('--restriction', type=str, nargs= '*', default=False, help='Specify language restrictions for scrape')
    args = parser.parse_args()
    ###   
    
    main(args)
