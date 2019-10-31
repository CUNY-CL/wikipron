import re

from typing import Iterator, Tuple

import requests
import requests_html

from wikipron.config import Config


Pair = Tuple[str, str]

# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
_CATEGORY_TEMPLATE = "Category:{language} terms with IPA pronunciation"
# Selects the content on the page.
_PAGE_TEMPLATE = "https://en.wiktionary.org/wiki/{word}"
_SPAN_SELECTOR = '//span[@class = "IPA"]'


def _yield_phn(request, config: Config):
    for li in request.html.xpath(config.li_selector):
        for span in li.xpath(_SPAN_SELECTOR):
            m = re.search(config.ipa_regex, span.text)
            if m:
                yield m


def _skip_word(word: str) -> bool:
    # Skips multiword examples.
    if " " in word:
        return True
    # Skips examples containing a dash.
    if "-" in word:
        return True
    # Skips examples containing digits.
    if re.search(r"\d", word):
        return True
    return False


def _skip_date(date_from_word: str, cut_off_date: str) -> bool:
    return date_from_word > cut_off_date


def _scrape_once(data, config: Config) -> Iterator[Pair]:
    session = requests_html.HTMLSession()
    for member in data["query"]["categorymembers"]:
        word = member["title"]
        date = member["timestamp"]
        if _skip_word(word) or _skip_date(date, config.cut_off_date):
            continue
        request = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10)
        word = config.extract_word(word, request)

        # TODO need this if check?
        if not word:
            continue

        for m in _yield_phn(request, config):
            try:
                pron = m.group(1)
            except IndexError:
                continue
            # Removes parens around various segments.
            pron = pron.replace("(", "").replace(")", "")
            # Skips examples with a space in the pron.
            if " " in pron:
                continue
            pron = config.process_pron(pron)
            if pron:
                yield (word, pron)


def scrape(config: Config) -> Iterator[Pair]:
    """Scrapes with a given configuration."""
    category = _CATEGORY_TEMPLATE.format(language=config.language)
    requests_params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": "500",
        "cmprop": "ids|title|timestamp",
    }
    while True:
        data = requests.get(
            "https://en.wiktionary.org/w/api.php?", params=requests_params
        ).json()
        yield from _scrape_once(data, config)
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        requests_params.update({"cmcontinue": continue_code})
