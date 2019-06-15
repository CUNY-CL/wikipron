#!/usr/bin/env python

import requests
import requests_html
import string

# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
CATEGORY = "Category:Japanese_katakana"
LIMIT = 500
INITIAL_QUERY = f"https://en.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle={CATEGORY}&cmlimit={LIMIT}"
CONTINUE_TEMPLATE = string.Template(INITIAL_QUERY + "&cmcontinue=$cmcontinue")

# Selects the content on the page.
PAGE_TEMPLATE = string.Template("https://en.wiktionary.org/wiki/$word")
SELECTOR = 'b[class="Latn form-of lang-ja romanized-form-of"]'


def _print_data(data):
    session = requests_html.HTMLSession()
    for member in data["query"]["categorymembers"]:
        katakana = member["title"]
        query = PAGE_TEMPLATE.substitute(word=katakana)
        got = session.get(query).html.find(SELECTOR, first=True)
        if not got:
            continue
        romaji = got.text
        # Skips multiword examples.
        if " " in romaji:
            continue
        if romaji.endswith(")") or romaji.endswith(","):
            romaji = romaji[:-1]
        romaji = romaji.casefold()
        print(f"{katakana}\t{romaji}")


def main():
    data = requests.get(INITIAL_QUERY).json()
    _print_data(data)
    code = data["continue"]["cmcontinue"]
    next_query = CONTINUE_TEMPLATE.substitute(cmcontinue=code)
    while True:
        data = requests.get(next_query).json()
        _print_data(data)
        # Then this is the last one.
        if not "continue" in data:
            break
        code = data["continue"]["cmcontinue"]
        next_query = CONTINUE_TEMPLATE.substitute(cmcontinue=code)


if __name__ == "__main__":
    main()
