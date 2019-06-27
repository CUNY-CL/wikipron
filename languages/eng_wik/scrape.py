#!/usr/bin/env python

import argparse
import re
import requests
import requests_html
import string

# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
CATEGORY = "Category:English_terms_with_IPA_pronunciation"
LIMIT = 500
INITIAL_QUERY = (
    "https://en.wiktionary.org/w/api.php?"
    "action=query"
    "&format=json"
    "&list=categorymembers"
    f"&cmtitle={CATEGORY}"
    f"&cmlimit={LIMIT}"
    "&cmprop=ids|title|timestamp"
)
CONTINUE_TEMPLATE = string.Template(INITIAL_QUERY + "&cmcontinue=$cmcontinue")
CUT_OFF_DATE = '2019-06-07'  # date of the very first project team meeting!

# Selects the content on the page.
PAGE_TEMPLATE = string.Template("https://en.wiktionary.org/wiki/$word")
LI_SELECTOR = """
//li[
  sup[a[@title = "Appendix:English pronunciation"]]
  and
  span[@class = "IPA"]
  and
  (
    span[a[@title = "w:American English" or @title = "w:General American"]]
    or
    count(span[@class = "ib-content qualifier-content"]) = 0
  )
]
"""
SPAN_SELECTOR = '//span[@class = "IPA"]'
PHONEMES = r"/(.+?)/"


def _yield_phn(request):
    for li in request.html.xpath(LI_SELECTOR):
        for span in li.xpath(SPAN_SELECTOR):
            m = re.search(PHONEMES, span.text)
            if m:
                yield m


def _print_data(data, args):
    session = requests_html.HTMLSession()
    for member in data["query"]["categorymembers"]:

        word = member["title"]
        # Skips multiword examples.
        if " " in word:
            continue
        # Skips examples containing a dash.
        if "-" in word:
            continue
        # Skips examples containing digits.
        if re.search(r"\d", word):
            continue

        date = re.search(r"\d{4}-\d{2}-\d{2}", member["timestamp"]).group(0)
        # Skips examples not available on or before the cut-off date.
        if date > CUT_OFF_DATE:
            continue

        request = session.get(PAGE_TEMPLATE.substitute(word=word))
        # Template lookup is case-sensitive, but we case-fold afterwards.
        word = word.casefold()
        for m in _yield_phn(request):
            pron = m.group(1)
            # Removes parens around various segments.
            pron = pron.replace("(", "").replace(")", "")
            # Skips examples with a space in the pron.
            if " " in pron:
                break
            if args.no_stress:
                pron = pron.replace('ˈ', '').replace('ˌ', '')
            if args.no_syllable_boundaries:
                pron = pron.replace('.', '')
            print(f"{word}\t{pron}")


def main(args):
    data = requests.get(INITIAL_QUERY).json()
    _print_data(data, args)
    code = data["continue"]["cmcontinue"]
    next_query = CONTINUE_TEMPLATE.substitute(cmcontinue=code)
    while True:
        data = requests.get(next_query).json()
        _print_data(data, args)
        # Then this is the last one.
        if not "continue" in data:
            break
        code = data["continue"]["cmcontinue"]
        next_query = CONTINUE_TEMPLATE.substitute(cmcontinue=code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-stress', action='store_true')
    parser.add_argument('--no-syllable-boundaries', action='store_true')
    main(parser.parse_args())
