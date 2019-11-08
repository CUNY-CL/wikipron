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


def _call_scrape(lang_settings, config, tsv_path):
    for unused_retries in range(10):
        count = 0
        with open(tsv_path, "w") as source:
            try:
                for (word, pron) in wikipron.scrape(config):
                    count += 1
                    print(f"{word}\t{pron}", file=source)
                return count
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                logger.info(
                    'Exception detected while scraping: "%s", "%s".',
                    lang_settings["key"],
                    tsv_path,
                )
                # Pauses execution for 10 min.
                time.sleep(600)
    logger.info(
        'Failed to scrape "%s" within 10 retries. %s',
        lang_settings["key"],
        lang_settings,
    )
    return 0


def _build_config_and_filter_files(
    config_settings, wiki_name, dialect_suffix=""
):
    path_affix = f'../tsv/{config_settings["key"]}_{dialect_suffix}'

    phonemic_config = wikipron.Config(**config_settings)
    phonemic_path = f"{path_affix}phonemic.tsv"
    phonemic_count = _call_scrape(
        config_settings, phonemic_config, phonemic_path
    )

    phonetic_config = wikipron.Config(phonetic=True, **config_settings)
    phonetic_path = f"{path_affix}phonetic.tsv"
    phonetic_count = _call_scrape(
        config_settings, phonetic_config, phonetic_path
    )

    # Removes TSVs with less than 100 lines.
    # Log language name and count to check whether Wikipron scraped any data.
    if phonemic_count < 100:
        logger.info(
            (
                '"%s" (count: %s) has less than '
                "100 entries in phonemic transcription."
            ),
            wiki_name,
            phonemic_count,
        )
        os.remove(phonemic_path)
    if phonetic_count < 100:
        os.remove(phonetic_path)
        logger.info(
            (
                '"%s" (count: %s) has less than '
                "100 entries in phonetic transcription."
            ),
            wiki_name,
            phonetic_count,
        )


def main():
    with open(LANGUAGES_PATH, "r") as source:
        languages = json.load(source)
    cut_off_date = datetime.date.today().isoformat()
    for iso639_code in languages:
        logger.info(
            'Current language: "%s"',
            languages[iso639_code]["wiktionary_name"],
        )
        config_settings = {
            "key": iso639_code,
            "casefold": languages[iso639_code]["casefold"],
            "no_stress": True,
            "no_syllable_boundaries": True,
            "cut_off_date": cut_off_date,
        }
        if "dialect" not in languages[iso639_code]:
            _build_config_and_filter_files(
                config_settings, languages[iso639_code]["wiktionary_name"]
            )
        else:
            for (dialect_key, dialect_value) in languages[iso639_code][
                "dialect"
            ].items():
                config_settings["dialect"] = dialect_value
                _build_config_and_filter_files(
                    config_settings,
                    languages[iso639_code]["wiktionary_name"],
                    dialect_key + "_",
                )


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    fh = logging.FileHandler(LOGGING_PATH, mode="a")
    formatter = logging.Formatter(
        "%(filename)s %(levelname)s: %(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    main()
