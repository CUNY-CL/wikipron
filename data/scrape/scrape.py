#!/usr/bin/env python
"""Performs the big scrape."""

import argparse
import datetime
import json
import logging
import os
import re

from typing import Any, Dict, FrozenSet, Iterator

import wikipron  # type: ignore

from data.scrape.lib.codes import (
    LANGUAGES_PATH,
    LOGGING_PATH,
    PHONES_DIRECTORY,
    TSV_DIRECTORY,
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
    with open(tsv_path, "w", encoding="utf-8") as source:
        scrape_results = wikipron.scrape(config)
        # Given phones, opens up a second TSV for scraping.
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


def _build_scraping_config(
    config_settings: Dict[str, Any], path_affix: str, phones_path_affix: str
) -> None:
    # Configures broad TSV.
    broad_config = wikipron.Config(**config_settings)
    broad_path = f"{path_affix}broad.tsv"
    # Checks for broad phones file.
    phones_broad = f"{phones_path_affix}broad.phones"
    if os.path.exists(phones_broad):
        logging.info(
            "Broad transcription phones found for %r at %r",
            config_settings["key"],
            phones_broad,
        )
        broad_path_filtered = f"{path_affix}broad_filtered.tsv"
        phoneme_set = frozenset(_phones_reader(phones_broad))
        _call_scrape(
            config_settings,
            broad_config,
            broad_path,
            phoneme_set,
            broad_path_filtered,
        )
    else:
        _call_scrape(config_settings, broad_config, broad_path)
    # Configures narrow TSV.
    narrow_config = wikipron.Config(narrow=True, **config_settings)
    narrow_path = f"{path_affix}narrow.tsv"
    # Checks for narrow phones file.
    phones_narrow = f"{phones_path_affix}narrow.phones"
    if os.path.exists(phones_narrow):
        logging.info(
            "Narrow phones found for %r at %r",
            config_settings["key"],
            phones_narrow,
        )
        narrow_path_filtered = f"{path_affix}narrow_filtered.tsv"
        phone_set = frozenset(_phones_reader(phones_narrow))
        _call_scrape(
            config_settings,
            narrow_config,
            narrow_path,
            phone_set,
            narrow_path_filtered,
        )
    else:
        _call_scrape(config_settings, narrow_config, narrow_path)


def main(args: argparse.Namespace) -> None:
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as source:
        languages = json.load(source)
    codes = frozenset(languages.keys())
    if args.restriction:
        # Cleans entry.
        restriction_set = frozenset(
            re.split(r"[;,\s]+\s*", args.restriction.strip(";, "))
        )
        if len(restriction_set) == 1 and not list(restriction_set)[0]:
            # Checks for empty entry.
            logging.fatal("Restriction flag raised but no language provided")
            exit(1)
        if not restriction_set.issubset(codes):
            for key in restriction_set - codes:
                logging.fatal("%r is not a valid ISO code", key)
            exit(1)
    else:
        restriction_set = codes
    if args.exclude:
        # Cleans entry.
        exclude_set = frozenset(
            re.split(r"[;,\s]+\s*", args.exclude.strip(";, "))
        )
        if len(exclude_set) == 1 and not list(exclude_set)[0]:
            # Checks for empty entry.
            logging.fatal("Exclude flag raised but no language provided")
            exit(1)
        if not exclude_set.issubset(codes):
            for key in exclude_set - codes:
                logging.fatal("%r is not a valid ISO code", key)
            exit(1)
    else:
        exclude_set = frozenset()
    codes = restriction_set - exclude_set
    # "2020-01-15" (Big Scrape 3).
    cut_off_date = datetime.date.today().isoformat()
    wikipron_accepted_settings = {
        "casefold": False,
        "skip_spaces_pron": True,
        "skip_spaces_word": True,
    }
    for code in codes:
        language_settings = languages[code]
        for k, v in language_settings.items():
            if k in wikipron_accepted_settings:
                wikipron_accepted_settings[k] = v
        config_settings = {
            "key": code,
            "stress": False,
            "syllable_boundaries": False,
            "cut_off_date": cut_off_date,
            **wikipron_accepted_settings,
        }
        if "dialect" not in language_settings:
            _build_scraping_config(
                config_settings,
                f"{TSV_DIRECTORY}/{config_settings['key']}_",
                f"{PHONES_DIRECTORY}/{config_settings['key']}_",
            )
        else:
            for (dialect_key, dialect_value) in language_settings[
                "dialect"
            ].items():
                config_settings["dialect"] = dialect_value
                _build_scraping_config(
                    config_settings,
                    f"{TSV_DIRECTORY}/{config_settings['key']}_{dialect_key}_",
                    f"{PHONES_DIRECTORY}/{config_settings['key']}_{dialect_key}_",
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
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--restriction",
        type=str,
        help="restricts scrape to specified language(s)",
    )
    group.add_argument(
        "--exclude",
        type=str,
        help="excludes specified language(s)",
    )
    main(parser.parse_args())
