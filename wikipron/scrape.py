import re

import requests
import requests_html

from wikipron.config import Config
from wikipron.typing import Iterator, WordPronPair


# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
_CATEGORY_TEMPLATE = "Category:{language} terms with IPA pronunciation"
# Selects the content on the page.
_PAGE_TEMPLATE = "https://en.wiktionary.org/wiki/{word}"


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


def _scrape_once(data, config: Config) -> Iterator[WordPronPair]:
    session = requests_html.HTMLSession()
    for member in data["query"]["categorymembers"]:
        word = member["title"]
        date = member["timestamp"]
        if _skip_word(word) or _skip_date(date, config.cut_off_date):
            continue
        request = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10)
        for word, pron in config.extract_word_pron(word, request, config):
            yield word, pron


def scrape(config: Config) -> Iterator[WordPronPair]:
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
