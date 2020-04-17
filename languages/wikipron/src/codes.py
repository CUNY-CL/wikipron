#!/usr/bin/env python
"""Identifies all languages with over 100 IPA entries on Wiktionary.

This is a tool for scraping all languages with over 100 entries from:

https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language

For each language it grabs the language name and language code (likely ISO
639-1) that Wiktionary uses.

It compares that code  with those in iso-639-3_20190408.tsv in order to grab
the appropriate ISO 639-2 or ISO 639-3 code and language name. A dictionary
containing this data is created and converted to a JSON file (languages.json).
Config settings for languages already in languages.json are transferred to the
new languages dictionary being created.

New languages that are added through this process and output to languages.json
require further processing before being imported by scrape_and_write.py:
* Casefolding must be specified
* Dialect information may also be specified
"""

# TODO: Generate and use a lookup table for the iso639-3 TSV file.

import csv
import logging
import json
import re

from typing import Iterator, Tuple

import requests
import requests_html  # type: ignore


LANGUAGES_PATH = "languages.json"
UNMATCHED_LANGUAGES_PATH = "unmatched_languages.json"
README_PATH = "../README.md"
LANGUAGES_SUMMARY_PATH = "../languages_summary.tsv"
LOGGING_PATH = "scraping.log"
ISO_TSV_PATH = "iso-639-3_20190408.tsv"
HBS_PATH = "../tsv/hbs_"
JPN_PATH = "../tsv/jpn_"


def _cat_info(cat_title: str) -> Iterator[str]:
    """Grabs title of Wiktionary language pages if it has > 100 entries."""
    cat_info_params = {
        "action": "query",
        "format": "json",
        "titles": cat_title,
        "prop": "categoryinfo",
    }
    data = requests.get(
        "https://en.wiktionary.org/w/api.php?", params=cat_info_params
    ).json()
    pages = data["query"]["pages"]
    for (k, v) in pages.items():
        num_of_pages = v["categoryinfo"]["pages"]
        if num_of_pages >= 100:
            isolate_language_category = re.search(
                r"(\s+)terms(\s+)", v["title"]
            )
            yield (
                v["title"][: isolate_language_category.start()]  # type: ignore
            )


def _cat_members() -> Iterator[str]:
    """Yields Wiktionary languages with IPA data."""
    cat_member_params = {
        "action": "query",
        "cmtitle": "Category:Terms with IPA pronunciation by language",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json",
    }
    while True:
        data = requests.get(
            "https://en.wiktionary.org/w/api.php?", params=cat_member_params
        ).json()
        for member in data["query"]["categorymembers"]:
            yield from _cat_info(member["title"])
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        cat_member_params["cmcontinue"] = continue_code


def _scrape_wiktionary_info(lang_title: str) -> Tuple[str, str]:
    """Extracts Wiktionary language name and code from language page."""
    name = ""
    code = ""
    session = requests_html.HTMLSession()
    language_page = session.get(
        f"https://en.wiktionary.org/wiki/{lang_title}_language", timeout=10
    )
    lang_table = language_page.html.find(
        ".language-category-info > tbody > tr"
    )
    i = 0
    while i < len(lang_table):
        if "Canonical name" in lang_table[i].text:
            name = lang_table[i].text
            name = name.split("\n")[1]
        elif "Language code" in lang_table[i].text:
            # Canonical name (should) always be filled already.
            # We grab Wiktionary language code as our entry point
            # to compare/confirm with ISO 639 TSV File because
            # Wiktionary name does not always correspond with
            # ISO language name.
            # Wiktionary: Ancient Greek; ISO: Greek, Ancient (to 1453).
            code = lang_table[i].text
            code = code.split("\n")[1]
            break
        i += 1
    return (name, code)


def main() -> None:
    new_languages = {}
    unmatched_languages = {}
    with open(LANGUAGES_PATH, "r") as source:
        prev_languages = json.load(source)
    with open(ISO_TSV_PATH, "r") as source:
        iso_list = csv.reader(source, delimiter="\t")
        for lang_page_title in _cat_members():
            logging.info('Working on: "%s"', lang_page_title)
            lang = {}
            iso639_name = ""
            iso639_code = ""
            # lang_page_title may come out with a space as in:
            # "Category:Ancient Greek"
            # space replaced with _
            (wiktionary_name, wiktionary_code) = _scrape_wiktionary_info(
                lang_page_title.replace(" ", "_")
            )
            for row in iso_list:
                # Catches ISO 639-3 (row[0]), ISO-639-2 B (row[1])
                # and ISO 639-2 T (row[2]), ISO 639-1 (row[3]);
                # converts all to ISO-639-2 B (row[1]) if available;
                # if not available converts to ISO 639-3 (row[0]).
                if wiktionary_code in row[0:4]:
                    iso639_name = row[6]
                    iso639_code = row[1] if row[1] else row[0]
                    break
            if iso639_code:
                # Wiki name and code may have changed since last running. The
                # iso639_name will likely not (unless we have changed/updated
                # the ISO 639-3 TSV), but is included in the dict below for
                # when adding new languages to languages.json.
                potentially_updated = {
                    "iso639_name": iso639_name,
                    "wiktionary_name": wiktionary_name,
                    "wiktionary_code": wiktionary_code,
                }
                # If language already in languages.json:
                if iso639_code in prev_languages:
                    # Imposes the potentially updated values on old values.
                    # Retains previously set casefold setting.
                    lang[iso639_code] = {
                        **prev_languages[iso639_code],
                        **potentially_updated,
                    }
                    new_languages.update(lang)
                else:
                    # Adds new language to languages.json.
                    lang[iso639_code] = {
                        **potentially_updated,
                        "casefold": None,
                    }
                    new_languages.update(lang)
            else:
                # No match found for the Wiktionary code in the ISO 639-3 TSV.
                lang[wiktionary_code] = {"wiktionary_name": wiktionary_name}
                unmatched_languages.update(lang)
            source.seek(0)
    with open(LANGUAGES_PATH, "w") as json_file:
        json_dict = json.dumps(new_languages, indent=4)
        json_file.write(json_dict)
    # All languages that failed to be matched with data in ISO 639 TSV file.
    with open(UNMATCHED_LANGUAGES_PATH, "w") as unmatched:
        unnmatched_json_dict = json.dumps(unmatched_languages, indent=4)
        unmatched.write(unnmatched_json_dict)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
