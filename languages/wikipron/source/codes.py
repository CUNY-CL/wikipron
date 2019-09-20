import requests
import requests_html
import re
import csv
import json


def cat_info(cat_title):
    cat_info_params = {
        "action": "query",
        "format": "json",
        "titles": cat_title,
        "prop": "categoryinfo"
    }
    data = requests.get("https://en.wiktionary.org/w/api.php?", params=cat_info_params).json()
    pages = data["query"]["pages"]

    for k, v in pages.items():
        num_of_pages = v["categoryinfo"]["pages"]
        if num_of_pages >= 100:
            isolate_language_category = re.search("(\s+)terms(\s+)", v["title"])
            yield (v["title"][0:isolate_language_category.start()], num_of_pages)
        else:
            continue

def cat_members():
    cat_member_params = {
        "action": "query",
        "cmtitle": "Category:Terms with IPA pronunciation by language",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }
    while True:
        data = requests.get("https://en.wiktionary.org/w/api.php?", params=cat_member_params).json()
        for member in data["query"]["categorymembers"]:
            yield from cat_info(member["title"])
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        cat_member_params["cmcontinue"] = continue_code


def scrape_wiktionary_info(page_template, lang_title):
    lang_title = lang_title.replace(" ", "_")
    # print(lang_title)
    name = None
    code = None

    session = requests_html.HTMLSession()
    language_page = session.get(page_template.format(language=lang_title), timeout=10)
    lang_table = language_page.html.find('.language-category-info > tbody > tr')

    i = 0
    while i < len(lang_table):
        if "Canonical name" in lang_table[i].text:
            name = lang_table[i].text
            name = name.split('\n')[1]
        elif "Language code" in lang_table[i].text:
            # Canonical name (should) always be filled already.
            # We grab Wiktionary language code as our entry point for comparison/confirmation with ISO 639 TSV File
            # Wiktionary name does not always correspond with ISO language name. 
            # Wiktionary: Ancient Greek; ISO: Greek, Ancient (to 1453)
            code = lang_table[i].text
            code = code.split('\n')[1]
            break
        i += 1
    return name, code


def main():
    languages_dictionary = {}
    failed_languages = {}
    # Why is the even up here?
    lang_page_template = "https://en.wiktionary.org/wiki/{language}_language"

    language_codes_file = open('language-codes-full.tsv', 'r')
    tsv_file = csv.reader(language_codes_file, delimiter="\t")

    for lang_page_title, total_pages in cat_members():    
        # Reset to beginning of tsv file, else we will continue to iterate from last match
        language_codes_file.seek(0)
        iso639_name = None
        iso639_code = None

        wiktionary_name, wiktionary_code = scrape_wiktionary_info(lang_page_template, lang_page_title)

        for row in tsv_file:
            # Convert ISO 639-1 and ISO 639-2 T to ISO-639-2 B and grab ISO language name.
            if wiktionary_code == row[2] or wiktionary_code == row[1] or wiktionary_code == row[0]:
                iso639_name = row[3]
                iso639_code = row[0]
                break

        if iso639_code:
            languages_dictionary[iso639_code] = {
                "iso639_name": iso639_name, 
                "wiktionary_name": wiktionary_name, 
                "wiktionary_code": wiktionary_code,
                "casefold": None, 
                "total_pages": total_pages
            }
        else:
            failed_languages[wiktionary_code] = {
                "wiktionary_name": wiktionary_name,
                "total_pages": total_pages
            }


    language_codes_file.close()
    with open("languages_dictionary.json", "w") as json_file:
        json_dict = json.dumps(languages_dictionary)
        json_file.write(json_dict)
    with open("failed_langauges.json", "w") as failed:
        failed_dict = json.dumps(failed_languages)
        failed.write(failed_dict)

if __name__ == "__main__":
  main()