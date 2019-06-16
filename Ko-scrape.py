#!/usr/bin/env python 
# coding: utf-8


import re
import requests
import requests_html
import string


CATEGORY = 'Category:Korean_terms_with_IPA_pronunciation'

LIMIT = 500    
INITIAL_QUERY = f'https://en.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle={CATEGORY}&cmlimit={LIMIT}'
CONTINUE_TEMPLATE = string.Template(INITIAL_QUERY + "&cmcontinue=$cmcontinue")

PAGE_TEMPLATE = string.Template("https://en.wiktionary.org/wiki/$word")     
LI_SELECTOR1 = '//li[sup[a[@title = "Appendix:Korean pronunciation"]] and span[@class = "IPA"]]' # a few Korean words have this format too.
LI_SELECTOR2 ='//li[span[sup[a[@title = "Appendix:Korean pronunciation"]]] and span[@class = "IPA"]]' # majority of Korean words has this format.
SPAN_SELECTOR = '//li[span[@class = "IPA"]]'    
PHONEMES = r"\[(.+?)\]"   


def _yield_phn(request):
    try:
        for li in request.html.xpath(LI_SELECTOR2):
            for span in li.xpath(SPAN_SELECTOR):
                m = re.search(PHONEMES, span.text)     
                if m:
                    yield m
    except:
        for li in request.html.xpath(LI_SELECTOR1):
            for span in li.xpath(SPAN_SELECTOR):
                print(span.text, '\n\n')
                if m:
                    yield m




def _print_data(data):
    session = requests_html.HTMLSession()
    """ <example of data>
query":{"categorymembers":[{"pageid":81811,"ns":0,"title":"Homo sapiens"},
{"pageid":3072481,"ns":0,"title":"\u0901"}...."""
    #f = open('kor.tsv', 'a')
    for member in data["query"]["categorymembers"]:
        word = member["title"]  
        # Skips multiword examples.
        if " " in word:
            continue
        query = PAGE_TEMPLATE.substitute(word=word)
        request = session.get(query)  
        
        for m in _yield_phn(request):
            pron = m.group(1)   
            print(f"{word}\t{pron}")
          



def main():
    data = requests.get(INITIAL_QUERY).json() 
    _print_data(data)
    code = data["continue"]["cmcontinue"]   
    """ <example>
    continue":{"cmcontinue":"page|414245494c4c45204d4552450a414245494c4c45204dc3885245|6478110","continue":"-||"}
    """
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

