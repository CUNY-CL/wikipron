#!/usr/bin/env python
"""Identifies all languages with over 100 IPA entries on Wiktionary.

This is a tool for scraping all languages with over 100 entries from:

https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language

For each language it grabs the language name and language code (likely ISO
639-1) that Wiktionary uses.

It compares that code with those in iso639_1-to-iso639_2.json and
iso639_2.json in order to grab the appropriate ISO 639-2 or ISO 639-3 code
and language name. A dictionary containing this data is created and converted
to a JSON file (languages.json). Config settings for languages already in
languages.json are transferred to the new languages dictionary being created.

New languages that are added through this process and output to languages.json
require further processing before being imported by scrape_and_write.py:

* Casefolding must be specified
* Dialect or script information may also be specified
"""

import logging
import json
import os
import re

from typing import Dict, List

import iso639
import requests
import requests_html  # type: ignore

import wikipron
from wikipron.scrape import HTTP_HEADERS

LIB_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LANGUAGES_PATH = os.path.join(LIB_DIRECTORY, "languages.json")
COMMON_CHARS_PATH = os.path.join(LIB_DIRECTORY, "common_chars.json")
GLOBAL_COMMON_CHARS_PATH = os.path.join(
    LIB_DIRECTORY, "global_common_chars.json"
)
UNMATCHED_LANGUAGES_PATH = os.path.join(
    LIB_DIRECTORY, "unmatched_languages.json"
)
ISO_639_1_PATH = os.path.join(LIB_DIRECTORY, "iso639_1-to-iso639_2.json")
ISO_639_2_PATH = os.path.join(LIB_DIRECTORY, "iso639_2.json")
SCRAPE_DIRECTORY = os.path.dirname(LIB_DIRECTORY)
LANGUAGES_SUMMARY_PATH = os.path.join(SCRAPE_DIRECTORY, "tsv_summary.tsv")
LOGGING_PATH = os.path.join(SCRAPE_DIRECTORY, "scraping.log")
README_PATH = os.path.join(SCRAPE_DIRECTORY, "README.md")
TSV_DIRECTORY = os.path.join(SCRAPE_DIRECTORY, "tsv")
PHONES_DIRECTORY = os.path.join(
    os.path.dirname(SCRAPE_DIRECTORY), "phones/phones"
)
PHONES_README_PATH = os.path.join(
    os.path.dirname(PHONES_DIRECTORY), "README.md"
)
PHONES_SUMMARY_PATH = os.path.join(
    os.path.dirname(PHONES_DIRECTORY), "phones_summary.tsv"
)
URL = "https://en.wiktionary.org/w/api.php"


def _get_language_categories() -> List[str]:
    """Get the list of language categories from Wiktionary.

    A category looks like "Category:Bengali terms with IPA pronunciation".

    Reference:
    https://en.wiktionary.org/w/index.php?title=Category:Terms_with_IPA_pronunciation_by_language
    """
    requests_params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:Terms with IPA pronunciation by language",
        "cmlimit": "500",
    }
    language_categories = []
    while True:
        data = requests.get(
            URL, params=requests_params, headers=HTTP_HEADERS
        ).json()
        for member in data["query"]["categorymembers"]:
            category = member["title"]
            language_categories.append(category)
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        requests_params.update({"cmcontinue": continue_code})
    return language_categories


def _get_language_sizes(categories: List[str]) -> Dict[str, int]:
    """Get the map from a language to its number of pronunciation entries."""
    language_sizes = {}
    # MediaWiki API can retrieve sizes for multiple categories at a time,
    # but would complain about too many language categories for each API call.
    chunk_size = 50
    for start in range(0, len(categories), chunk_size):
        end = start + chunk_size
        requests_params = {
            "action": "query",
            "format": "json",
            "prop": "categoryinfo",
            "titles": "|".join(categories[start:end]),
        }
        data = requests.get(
            URL, params=requests_params, headers=HTTP_HEADERS
        ).json()
        for page in data["query"]["pages"].values():
            size = page["categoryinfo"]["size"]
            language_search = re.search(
                r"Category:(.+?) terms with IPA pronunciation", page["title"]
            )
            if not language_search:
                logging.warning(
                    "Could not extract language from title: %s", page["title"]
                )
                continue
            language = language_search.group(1)
            language_sizes[language] = size
    return language_sizes


def _scrape_wiktionary_language_code(lang_title: str) -> str:
    """Extracts Wiktionary language code from language page."""
    # Perhaps a bit overdetermined.
    lang_code_selector = """
    //tbody
        /tr[@class = "language-category-data"]
            /following-sibling::tr[
                th
                    /a[@title = "Wiktionary:Languages"]
            ]//td
                /code
    """
    session = requests_html.HTMLSession()
    language_page = session.get(
        f"https://en.wiktionary.org/wiki/Category:{lang_title}_language",
        timeout=10,
        headers=HTTP_HEADERS,
    )
    return language_page.html.xpath(lang_code_selector)[0].text


def _check_language_code_against_wiki(
    language_code: str, language: str
) -> None:
    """Checks if WikiPron can handle the assigned ISO language code."""
    try:
        language_inferred = wikipron.Config(key=language_code).language
    except iso639.NonExistentLanguageError:
        logging.warning("WikiPron cannot handle %r", language)
    else:
        if language_inferred != language:
            logging.warning(
                "WikiPron resolves the key %r to %r "
                "listed as %r on Wiktionary",
                language_code,
                language_inferred,
                language,
            )


def main() -> None:
    new_languages = {}
    unmatched_languages = {}
    with open(LANGUAGES_PATH, "r", encoding="utf-8") as lang_source:
        prev_languages = json.load(lang_source)
    with open(ISO_639_1_PATH, "r", encoding="utf-8") as iso1_source:
        iso639_1 = json.load(iso1_source)
    with open(ISO_639_2_PATH, "r", encoding="utf-8") as iso2_source:
        iso639_2 = json.load(iso2_source)
    categories = _get_language_categories()
    sizes = _get_language_sizes(categories)
    for wiktionary_name, size in sizes.items():
        if wiktionary_name == "Translingual":
            continue
        if size >= 100:
            wiktionary_code = _scrape_wiktionary_language_code(
                wiktionary_name.replace(" ", "_")
            )
            if wiktionary_code in iso639_1:
                iso639_code = iso639_1[wiktionary_code]["code"]
                iso639_name = iso639_1[wiktionary_code]["name"]
            elif wiktionary_code in iso639_2:
                iso639_code = wiktionary_code
                iso639_name = iso639_2[wiktionary_code]["name"]
            else:
                # No match found for the Wiktionary code.
                unmatched_languages[wiktionary_code] = {
                    "wiktionary_name": wiktionary_name
                }
                continue
            core_settings = {
                "iso639_name": iso639_name,
                "wiktionary_name": wiktionary_name,
                "wiktionary_code": wiktionary_code,
            }
            if iso639_code in prev_languages:
                # Imposes the potentially updated values on old values.
                # Retains previous non-core settings.
                new_languages[iso639_code] = {
                    **prev_languages[iso639_code],
                    **core_settings,
                }
            else:
                # Adds previously unseen language.
                new_languages[iso639_code] = {
                    **core_settings,
                    "casefold": None,
                }
            _check_language_code_against_wiki(iso639_code, wiktionary_name)
    with open(LANGUAGES_PATH, "w", encoding="utf-8") as sink:
        json.dump(new_languages, sink, indent=4, ensure_ascii=False)
    with open(UNMATCHED_LANGUAGES_PATH, "w", encoding="utf-8") as sink:
        json.dump(unmatched_languages, sink, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="WARNING"
    )
    main()
