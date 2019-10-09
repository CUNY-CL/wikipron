"""
This is a tool for scraping all languages with over 100 entries from:
https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language
For each language it grabs the language name and
language code (likely ISO 639-1) that Wiktionary uses.
It compares that code  with those in "./iso-639-3_20190408.tsv"
in order to grab the appropriate ISO 639-2 or ISO 639-3 code and language name.
A dictionary containing this data is created and
converted to a JSON file (languages.json).
Casefolding settings for languages already in languages.json
are transferred to the new languages dictionary being created.

New languages that are added through this process
and outputted to languages.json require further processing
before being imported into scrape_and_write.py.
Casefolding still needs to be specified.
Dialect information and other config options need
to be added manually as well.
"""

import requests
import requests_html
import re
import csv
import json
import logging


def cat_info(cat_title):
    cat_info_params = {
        "action": "query",
        "format": "json",
        "titles": cat_title,
        "prop": "categoryinfo"
    }
    data = requests.get(
        "https://en.wiktionary.org/w/api.php?",
        params=cat_info_params
    ).json()
    pages = data["query"]["pages"]

    for k, v in pages.items():
        num_of_pages = v["categoryinfo"]["pages"]
        if num_of_pages >= 100:
            isolate_language_category = re.search(
                r"(\s+)terms(\s+)",
                v["title"]
            )
            yield (
                v["title"][0:isolate_language_category.start()],
                num_of_pages
            )


def cat_members():
    cat_member_params = {
        "action": "query",
        "cmtitle": "Category:Terms with IPA pronunciation by language",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }
    while True:
        data = requests.get(
            "https://en.wiktionary.org/w/api.php?",
            params=cat_member_params
        ).json()
        for member in data["query"]["categorymembers"]:
            yield from cat_info(member["title"])
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        cat_member_params["cmcontinue"] = continue_code


def scrape_wiktionary_info(lang_title):
    name = None
    code = None

    session = requests_html.HTMLSession()
    language_page = session.get(
        f"https://en.wiktionary.org/wiki/{lang_title}_language",
        timeout=10
    )
    lang_table = language_page.html.find(
        '.language-category-info > tbody > tr'
    )

    i = 0
    while i < len(lang_table):
        if "Canonical name" in lang_table[i].text:
            name = lang_table[i].text
            name = name.split('\n')[1]
        elif "Language code" in lang_table[i].text:
            # Canonical name (should) always be filled already.
            # We grab Wiktionary language code as our entry point
            # to compare/confirm with ISO 639 TSV File because
            # Wiktionary name does not always correspond with ISO language name
            # Wiktionary: Ancient Greek; ISO: Greek, Ancient (to 1453)
            code = lang_table[i].text
            code = code.split('\n')[1]
            break
        i += 1
    return name, code


def main():
    new_languages = {}
    failed_languages = {}
    prev_languages_file = open("languages.json", "r")
    prev_languages = json.load(prev_languages_file)
    language_codes_file = open("iso-639-3_20190408.tsv", "r")
    iso_list = csv.reader(language_codes_file, delimiter="\t")
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s",
        level="INFO"
    )

    for lang_page_title, total_pages in cat_members():
        logging.info('Working on: "%s"', lang_page_title)
        lang = {}
        iso639_name = None
        iso639_code = None

        # lang_page_title may come out with a space as in:
        # "Category:Ancient Greek"
        # space replaced with _
        wiktionary_name, wiktionary_code = scrape_wiktionary_info(
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
            lang[iso639_code] = {
                "iso639_name": iso639_name,
                "wiktionary_name": wiktionary_name,
                "wiktionary_code": wiktionary_code,
                "casefold": (
                    prev_languages[iso639_code]["casefold"]
                    if iso639_code in prev_languages
                    else None
                ),
                "total_pages": total_pages
            }
            new_languages.update(lang)
        else:
            lang[wiktionary_code] = {
                "wiktionary_name": wiktionary_name,
                "total_pages": total_pages
            }
            failed_languages.update(lang)
        # Reset to beginning of tsv file
        # Else we will continue for loop from index of last match
        language_codes_file.seek(0)

    prev_languages_file.close()
    language_codes_file.close()

    with open("languages.json", "w") as json_file:
        json_dict = json.dumps(new_languages, indent=4)
        json_file.write(json_dict)
    # All languages that failed to be paired with data in ISO 639 tsv file
    with open("failed_languages.json", "w") as failed:
        failed_dict = json.dumps(failed_languages, indent=4)
        failed.write(failed_dict)


if __name__ == "__main__":
    main()
