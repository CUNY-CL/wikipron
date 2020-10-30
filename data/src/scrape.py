#!/usr/bin/env python
"""Performs the big scrape."""

import argparse
import datetime
import json
import logging
import os
import time
import re

from typing import Any, Dict, FrozenSet, Iterator

import requests
import wikipron  # type: ignore

from data.src.codes import (
    LANGUAGES_PATH,
    LOGGING_PATH,
    TSV_DIRECTORY_PATH,
    PHONES_DIRECTORY_PATH,
)


def _phones_reader(path: str) -> Iterator[str]:
    # Reads phones file.
    with open(path, "r", encoding="utf-8") as source:
        for line in source:
            line = re.sub(r"\s*#.*$", "", line)  # Removes comments from line.
            yield line.rstrip()


def _filter(word: str, pron: str, phones: FrozenSet[str]) -> bool:
    # Determines if gloss is valid given phone set.
    these_phones = frozenset(pron.split())
    bad_phones = these_phones - phones
    if bad_phones:
        for phone in bad_phones:
            logging.warning("Bad phone:\t%s\t(%s)", phone, word)
        return False
    else:
        return True


def _call_scrape(
    lang_settings: Dict[str, str],
    config: wikipron.Config,
    tsv_path: str,
    phones_set: FrozenSet[str] = None,
    tsv_filtered_path: str = "",
) -> None:
    for unused_retries in range(10):
        with open(tsv_path, "w", encoding="utf-8") as source:
            try:
                scrape_results = wikipron.scrape(config)
                # Given phones, opens up a second tsv for scraping.
                if phones_set:
                    with open(
                        tsv_filtered_path, "w", encoding="utf-8"
                    ) as source_filtered:
                        for (word, pron) in scrape_results:
                            line = f"{word}\t{pron}"
                            if _filter(word, pron, phones_set):
                                print(line, file=source_filtered)
                            print(line, file=source)
                else:
                    for (word, pron) in scrape_results:
                        print(f"{word}\t{pron}", file=source)
                return
            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ):
                logging.info(
                    "Exception detected while scraping: %r, %r, %r",
                    lang_settings["key"],
                    tsv_path,
                    tsv_filtered_path,
                )
                # Pauses execution for 10 min.
                time.sleep(600)
    # Log and remove TSVs for languages that failed.
    logging.info(
        "Failed to scrape %r with 10 retries (%s)",
        lang_settings["key"],
        lang_settings,
    )
    # Checks if second TSV was opened.
    try:
        os.remove(tsv_filtered_path)
    except OSError:
        pass
    os.remove(tsv_path)


def _build_scraping_config(
    config_settings: Dict[str, Any], path_affix: str, phones_path_affix: str
) -> None:
    # Configures phonemic TSV.
    phonemic_config = wikipron.Config(**config_settings)
    phonemic_path = f"{path_affix}phonemic.tsv"
    # Checks for phonemic phones file.
    phones_phonemic = f"{phones_path_affix}phonemic.phones"
    if os.path.exists(phones_phonemic):
        logging.info(
            "Phonemic phones found for %r at %r",
            config_settings["key"],
            phones_phonemic,
        )
        phonemic_path_filtered = f"{path_affix}phonemic_filtered.tsv"
        phoneme_set = frozenset(_phones_reader(phones_phonemic))
        _call_scrape(
            config_settings,
            phonemic_config,
            phonemic_path,
            phoneme_set,
            phonemic_path_filtered,
        )
    else:
        _call_scrape(config_settings, phonemic_config, phonemic_path)

    # Configures phonetic TSV.
    phonetic_config = wikipron.Config(phonetic=True, **config_settings)
    phonetic_path = f"{path_affix}phonetic.tsv"
    # Checks for phonetic phones file.
    phones_phonetic = f"{phones_path_affix}phonetic.phones"
    if os.path.exists(phones_phonetic):
        logging.info(
            "Phonetic phones found for %r at %r",
            config_settings["key"],
            phones_phonetic,
        )
        phonetic_path_filtered = f"{path_affix}phonetic_filtered.tsv"
        phone_set = frozenset(_phones_reader(phones_phonetic))
        _call_scrape(
            config_settings,
            phonetic_config,
            phonetic_path,
            phone_set,
            phonetic_path_filtered,
        )
    else:
        _call_scrape(config_settings, phonetic_config, phonetic_path)


def main(args: argparse.Namespace) -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)

    codes = list(languages.keys())

    # Verifies language code for --restriction is valid.
    if args.restriction:
        # Cleans entry.
        keys = re.split(r"[;,\s]+\s*", args.restriction[0].strip(";, "))
        if not keys[0]:
            # Checks for empty entry.
            logging.fatal("Restriction flag raised but no language provided")
            exit(1)
        rset = frozenset(args.restriction)
        lset = frozenset(codes)
        eset = rset - lset
        if eset:
            for key in eset:
                logging.fatal("%r is not a valid ISO code", key)
            exit(1)
        codes = list(rset)

    # "2020-01-15" (Big Scrape 3).
    cut_off_date = datetime.date.today().isoformat()
    wikipron_accepted_settings = {
        "casefold": False,
        "no_skip_spaces_pron": False,
        "no_skip_spaces_word": False,
    }

    for code in codes:
        language_settings = languages[code]
        for k, v in language_settings.items():
            if k in wikipron_accepted_settings:
                wikipron_accepted_settings[k] = v
        config_settings = {
            "key": code,
            "no_stress": True,
            "no_syllable_boundaries": True,
            "cut_off_date": cut_off_date,
            **wikipron_accepted_settings,
        }
        if "dialect" not in language_settings:
            _build_scraping_config(
                config_settings,
                f"{TSV_DIRECTORY_PATH}/{config_settings['key']}_",
                f"{PHONES_DIRECTORY_PATH}/{config_settings['key']}_",
            )
        else:
            for (dialect_key, dialect_value) in language_settings[
                "dialect"
            ].items():
                config_settings["dialect"] = dialect_value
                _build_scraping_config(
                    config_settings,
                    f"{TSV_DIRECTORY_PATH}/{config_settings['key']}_{dialect_key}_",
                    f"{PHONES_DIRECTORY_PATH}/{config_settings['key']}_{dialect_key}_",
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--restriction",
        type=str,
        nargs="+",
        help="restricts scrape to specified language(s)",
    )
    main(parser.parse_args())
