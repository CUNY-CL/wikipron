#!/usr/bin/env python
"""Runs the big scrape."""

import argparse
import contextlib
import datetime
import json
import logging
import os
import re
import unicodedata

from collections.abc import Iterator
from typing import Any

import wikipron
from wikipron.scrape import (
    _language_name_for_scraping,
    iter_page_responses,
)

LIB_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LANGUAGES_PATH = os.path.join(LIB_DIRECTORY, "languages.json")
SCRAPE_DIRECTORY = os.path.dirname(LIB_DIRECTORY)
PHONES_DIRECTORY = os.path.join(
    os.path.dirname(SCRAPE_DIRECTORY), "phones/phones"
)
LOGGING_PATH = os.path.join(SCRAPE_DIRECTORY, "scraping.log")
TSV_DIRECTORY = os.path.join(SCRAPE_DIRECTORY, "tsv")
UNSCRAPED_JSON_FILENAME = os.path.join(
    os.path.dirname(__file__), "unscraped.json"
)


def _phones_reader(path: str) -> Iterator[str]:
    # Reads phones file.
    with open(path, "r", encoding="utf-8") as source:
        for line in source:
            line = re.sub(r"\s*#.*$", "", line)  # Removes comments from line.
            yield line.rstrip()


def _filter(word: str, pron: str, phones: frozenset[str]) -> bool:
    # Determines if gloss is valid given phone set.
    these_phones = frozenset(pron.split())
    bad_phones = these_phones - phones
    if bad_phones:
        for phone in bad_phones:
            logging.warning("Bad phone:\t%s\t(%s)", phone, word)
        return False
    else:
        return True


def scrape_multi(
    configs: list[wikipron.Config],
) -> Iterator[tuple[int, tuple[str, str]]]:
    """Run extractors from several configs against a single page fetch.

    All configs must resolve to the same Wiktionary scraping category
    (per ``_language_name_for_scraping``) and share cut_off_date and
    skip_spaces_word — anything that affects which pages get fetched.
    Configs may differ in ``language`` itself when several varieties
    sit under the same scraping category (e.g. all Chinese varieties).
    Only post-parse-filtering settings (notably ``narrow`` and
    ``dialect``) may differ.
    Yields ``(config_index, (word, pron))`` so callers can route each
    pair to the right output bucket.
    """
    if not configs:
        return
    lead = configs[0]
    lead_category = _language_name_for_scraping(lead.language)
    for other in configs[1:]:
        if _language_name_for_scraping(other.language) != lead_category:
            raise ValueError(
                "scrape_multi configs must share a scraping category: "
                f"{lead.language!r} (-> {lead_category!r}) vs "
                f"{other.language!r} "
                f"(-> {_language_name_for_scraping(other.language)!r})"
            )
        for attr in ("cut_off_date", "skip_spaces_word"):
            if getattr(other, attr) != getattr(lead, attr):
                raise ValueError(
                    f"scrape_multi configs must agree on {attr!r}: "
                    f"{getattr(lead, attr)!r} vs {getattr(other, attr)!r}"
                )
    for title, request in iter_page_responses(lead):
        for idx, config in enumerate(configs):
            for word, pron in config.extract_word_pron(title, request, config):
                yield idx, (word, unicodedata.normalize("NFC", pron))


def _call_scrape_multi(
    configs: list[wikipron.Config],
    output_specs: list[dict[str, Any]],
) -> None:
    with contextlib.ExitStack() as stack:
        # buffering=1 for line-buffered, so partial output is visible
        # on disk immediately. Without it, with many output sinks
        # (e.g., several dialects x broad/narrow), per-file buffers
        # can sit unflushed for hours and a long-running scrape
        # looks dead from the outside.
        sources = [
            stack.enter_context(
                open(spec["tsv_path"], "w", encoding="utf-8", buffering=1)
            )
            for spec in output_specs
        ]
        filtered_sources: list[Any] = []
        for spec in output_specs:
            if spec["phones_set"] is not None:
                filtered_sources.append(
                    stack.enter_context(
                        open(
                            spec["tsv_filtered_path"],
                            "w",
                            encoding="utf-8",
                            buffering=1,
                        )
                    )
                )
            else:
                filtered_sources.append(None)
        for idx, (word, pron) in scrape_multi(configs):
            line = f"{word}\t{pron}"
            print(line, file=sources[idx])
            phones_set = output_specs[idx]["phones_set"]
            if phones_set is not None and _filter(word, pron, phones_set):
                print(line, file=filtered_sources[idx])


def build_scraping_config(
    config_settings: dict[str, Any], path_affix: str, phones_path_affix: str
) -> tuple[list[wikipron.Config], list[dict[str, Any]]]:
    broad_config = wikipron.Config(**config_settings)
    narrow_config = wikipron.Config(narrow=True, **config_settings)
    output_specs: list[dict[str, Any]] = []
    # Broad bucket.
    broad_spec: dict[str, Any] = {
        "tsv_path": f"{path_affix}broad.tsv",
        "phones_set": None,
        "tsv_filtered_path": None,
    }
    phones_broad = f"{phones_path_affix}broad.phones"
    if os.path.exists(phones_broad):
        logging.info(
            "Broad transcription phones found for %r at %r",
            config_settings["key"],
            phones_broad,
        )
        broad_spec["phones_set"] = frozenset(_phones_reader(phones_broad))
        broad_spec["tsv_filtered_path"] = f"{path_affix}broad_filtered.tsv"
    output_specs.append(broad_spec)
    # Narrow bucket.
    narrow_spec: dict[str, Any] = {
        "tsv_path": f"{path_affix}narrow.tsv",
        "phones_set": None,
        "tsv_filtered_path": None,
    }
    phones_narrow = f"{phones_path_affix}narrow.phones"
    if os.path.exists(phones_narrow):
        logging.info(
            "Narrow phones found for %r at %r",
            config_settings["key"],
            phones_narrow,
        )
        narrow_spec["phones_set"] = frozenset(_phones_reader(phones_narrow))
        narrow_spec["tsv_filtered_path"] = f"{path_affix}narrow_filtered.tsv"
    output_specs.append(narrow_spec)
    return [broad_config, narrow_config], output_specs


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
    if not args.fresh and os.path.exists(UNSCRAPED_JSON_FILENAME):
        with open(UNSCRAPED_JSON_FILENAME, encoding="utf-8") as f:
            unscraped_json = json.load(f)
        unscraped_codes = frozenset(unscraped_json["unscraped"])
        cut_off_date = unscraped_json["cut_off_date"]
        logging.info("`unscraped.json` detected and used")
    else:
        unscraped_codes = frozenset(languages.keys())
        # Previous cut-off dates for big scrape runs:
        # - "2020-01-15"
        # - "2022-01-24"
        cut_off_date = datetime.date.today().isoformat()
    codes_sorted = sorted((restriction_set - exclude_set) & unscraped_codes)
    remaining = codes_sorted.copy()
    # Group codes by their Wiktionary scraping category so that
    # varieties sharing one category (e.g. all Chinese varieties under
    # "Chinese terms with IPA pronunciation") are scraped in a single
    # pass over that category instead of fetching it once per code.
    groups: dict[str, list[str]] = {}
    for code in codes_sorted:
        cat = _language_name_for_scraping(languages[code]["wiktionary_name"])
        groups.setdefault(cat, []).append(code)
    for codes_in_group in groups.values():
        all_configs: list[wikipron.Config] = []
        all_specs: list[dict[str, Any]] = []
        for code in codes_in_group:
            configs, specs = _build_configs_for_code(
                code, languages[code], cut_off_date
            )
            all_configs.extend(configs)
            all_specs.extend(specs)
        _call_scrape_multi(all_configs, all_specs)
        for code in codes_in_group:
            remaining.remove(code)
        with open(UNSCRAPED_JSON_FILENAME, "w", encoding="utf-8") as f:
            unscraped = {
                "cut_off_date": cut_off_date,
                "unscraped": sorted(remaining),
            }
            json.dump(unscraped, f, indent=4)


def _build_configs_for_code(
    code: str,
    language_settings: dict[str, Any],
    cut_off_date: str,
) -> tuple[list[wikipron.Config], list[dict[str, Any]]]:
    """Build the (configs, specs) tuple for a single ISO code.

    Honors per-language overrides of ``skip_spaces_pron``,
    ``skip_spaces_word``, and ``parens`` from languages.json.
    """
    accepted = {
        "skip_spaces_pron": True,
        "skip_spaces_word": True,
        "parens": "expand",
    }
    for k, v in language_settings.items():
        if k in accepted:
            accepted[k] = v
    config_settings: dict[str, Any] = {
        "key": code,
        "stress": False,
        "syllable_boundaries": False,
        "cut_off_date": cut_off_date,
        **accepted,
    }
    configs: list[wikipron.Config] = []
    specs: list[dict[str, Any]] = []
    if "dialect" not in language_settings:
        c, s = build_scraping_config(
            config_settings,
            f"{TSV_DIRECTORY}/{code}_",
            f"{PHONES_DIRECTORY}/{code}_",
        )
        configs.extend(c)
        specs.extend(s)
    else:
        for dialect_key, dialect_value in language_settings["dialect"].items():
            config_settings["dialect"] = dialect_value
            c, s = build_scraping_config(
                config_settings,
                f"{TSV_DIRECTORY}/{code}_{dialect_key}_",
                f"{PHONES_DIRECTORY}/{code}_{dialect_key}_",
            )
            configs.extend(c)
            specs.extend(s)
    return configs, specs


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
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="forces a fresh scrape for all languages",
    )
    main(parser.parse_args())
