#!/usr/bin/env python
"""Identifies all languages with over 100 IPA entries on Wiktionary.

This is a tool for scraping all languages with over 100 entries from:

https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language

For each language it grabs the language name and language code (likely ISO
639-1) that Wiktionary uses.

It compares that code  with those in iso-639-3_20190408.tsv in order to grab the
appropriate ISO 639-2 or ISO 639-3 code and language name. A dictionary
containing this data is created and converted to a JSON file
(languages.json). Config settings for languages already in
languages.json are transferred to the new languages dictionary being created.

New languages that are added through this process and outputted to languages.json
require further processing before being imported by scrape_and_write.py:

* Casefolding needs to be specified
* Dialect information may also need to be added manually
"""

# TODO Generate and use a lookup table for the iso639-3 tsv file

import csv
import logging
import json
import re

import requests
import requests_html

# Set CUT_OFF_DATE below.
# CUT_OFF_DATE can be no later than the date
# at which you plan to begin scraping.
CUT_OFF_DATE = "2019-11-01"


# Grabs title of Wikitionary language page if it has more than 100 entries.
def _cat_info(cat_title):
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
                v["title"][0 : isolate_language_category.start()]
            )


# Runs through Wikitionary languages with IPA.
def _cat_members():
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


# Uses title of Wiktionary language page to grab
# Wiktionary language name and Wiktionary language code
def _scrape_wiktionary_info(lang_title):
    name = None
    code = None
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
            # Wiktionary name does not always correspond with ISO language name
            # Wiktionary: Ancient Greek; ISO: Greek, Ancient (to 1453)
            code = lang_table[i].text
            code = code.split("\n")[1]
            break
        i += 1
    return (name, code)


def main():
    new_languages = {}
    unmatched_languages = {}
    basic_config_options = {
        "casefold": None,
        "no_stress": True,
        "no_syllable_boundaries": True,
        "cut_off_date": CUT_OFF_DATE
    }
    with open("languages.json", "r") as source:
        prev_languages = json.load(source)
    with open("iso-639-3_20190408.tsv", "r") as source:
        iso_list = csv.reader(source, delimiter="\t")
        for (lang_page_title) in _cat_members():
            logging.info('Working on: "%s"', lang_page_title)
            lang = {}
            iso639_name = None
            iso639_code = None
            # lang_page_title may come out with a space as in:
            # "Category:Ancient Greek"
            # space replaced with _
            (wiktionary_name, wiktionary_code) = _scrape_wiktionary_info(
                lang_page_title.replace(" ", "_")
            )
            for row in iso_list:
                # Catches ISO 639-3 (row[0]), ISO-639-2 B (row[1])
                # and ISO 639-2 T (row[2]), ISO 639-1 (row[3])
                # Converts all to ISO-639-2 B (row[1]) if available
                # If not available converts to ISO 639-3 (row[0])
                if wiktionary_code in row[0:4]:
                    iso639_name = row[6]
                    iso639_code = row[1] if row[1] else row[0]
                    break
            if iso639_code:
                # Wiki name and code may have changed since last running.
                # iso639_name will likely not
                # (unless we have changed/updated the tsv),
                # but is included in the dict below for when adding
                # new languages to languages.json
                potentially_updated = {
                    "iso639_name": iso639_name,
                    "wiktionary_name": wiktionary_name,
                    "wiktionary_code": wiktionary_code,
                }
                # If language already in languages.json
                if iso639_code in prev_languages:
                    # Impose the potentially updated values on old values.
                    lang[iso639_code] = {
                        **prev_languages[iso639_code],
                        **potentially_updated,
                    }
                    # Update cut off date
                    lang[iso639_code]["cut_off_date"] = CUT_OFF_DATE
                    new_languages.update(lang)
                else:
                    # Adding a new language to languages.json
                    lang[iso639_code] = {
                        **potentially_updated,
                        **basic_config_options,
                    }
                    new_languages.update(lang)
            else:
                # Could not find a match for the wikitionary code
                # in our ISO 639-3 tsv.
                lang[wiktionary_code] = {
                    "wiktionary_name": wiktionary_name,
                }
                unmatched_languages.update(lang)
            source.seek(0)
    with open("languages.json", "w") as json_file:
        json_dict = json.dumps(new_languages, indent=4)
        json_file.write(json_dict)
    # All languages that failed to be matched with data in ISO 639 TSV file.
    with open("unmatched_languages.json", "w") as unmatched:
        unnmatched_json_dict = json.dumps(unmatched_languages, indent=4)
        unmatched.write(unnmatched_json_dict)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
