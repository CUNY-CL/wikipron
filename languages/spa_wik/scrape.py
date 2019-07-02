#!/usr/bin/env python

import argparse
import re
import requests
import requests_html
import string

# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
CATEGORY = "Category:Spanish_terms_with_IPA_pronunciation"
LIMIT = 500
INITIAL_QUERY = f"https://en.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle={CATEGORY}&cmlimit={LIMIT}"
CONTINUE_TEMPLATE = string.Template(INITIAL_QUERY + "&cmcontinue=$cmcontinue")

# Selects the content on the page.
PAGE_TEMPLATE = string.Template("https://en.wiktionary.org/wiki/$word")

"""LI_SELECTOR...v_1 assumes that all Latin American phonemes will be the last bulleted entry in the "//ul" section."""

LI_SELECTOR_for_Latin_American_phonemes_v_1 = """\
//li[last()][sup[a[@title = "Appendix:Spanish pronunciation"]]\
and span[@class = "IPA"]]\
"""

""" 
LI_SELECTOR..._v_2 assumes that Latin American phonemes are the only entries that won't have a hyperlinked description  
before providing the phoneme.    
"""

LI_SELECTOR_for_Latin_American_phonemes_v_2 = """\
//li[sup[a[@title = "Appendix:Spanish pronunciation"]] and span[@class = "IPA"]\
and count(span[a]) =0]\
"""

"""
LI_SELECTOR..._v_3 assumes that entries are Latin American if the non-hyperlinked textual description,  
"Latin America", is provided before the phoneme,or if no description is provided at all.   
"""

LI_SELECTOR_for_Latin_American_phonemes_v_3 = """\
//li[sup[a[@title = "Appendix:Spanish pronunciation"]] and span[@class = "IPA"]\
and\
(span[@class = "ib-content qualifier-content"][text()="Latin America"]\
or\
count(span[@class = "ib-content qualifier-content"]) = 0)]\
"""

SPAN_SELECTOR = '//span[@class = "IPA"]'
PHONEMES = r"/(.+?)/"


def _yield_phn(request):
    for li in request.html.xpath(LI_SELECTOR_for_Latin_American_phonemes_v_3):
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
        # Skips examples starting or ending with a dash.
        if word.startswith("-") or word.endswith("-"):
            continue
        # Skips examples containing digits.
        if re.search(r"\d", word):
            continue
        request = session.get(PAGE_TEMPLATE.substitute(word=word))
        # Template lookup is case-sensitive, but we case-fold afterwards.
        word = word.casefold()
        for m in _yield_phn(request):
            pron = m.group(1)
            # Skips examples with a space in the pron.
            if " " in pron:
                continue
            if args.no_stress:
                pron = pron.replace('ˈ', '').replace('ˌ', '')
            print(f"{word.casefold()}\t{pron}")
            
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
    parser.add_argument("--no-stress", action="store_true")
    main(parser.parse_args())
