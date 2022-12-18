import re
import time
import unicodedata
from importlib.metadata import version

from typing import Any, Dict

import requests
import requests_html

from wikipron.config import Config
from wikipron.typing import Iterator, WordPronPair

# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
_CATEGORY_TEMPLATE = "Category:{language} terms with IPA pronunciation"
# Selects the content on the page.
_PAGE_TEMPLATE = "https://en.wiktionary.org/wiki/{word}"
# Http headers for api call
HTTP_HEADERS = {
    "User-Agent": (
        f"WikiPron/{version('wikipron')} "
        "(https://github.com/CUNY-CL/wikipron) "
        f"requests/{requests.__version__}"
    ),
}


def _skip_word(word: str, skip_spaces: bool) -> bool:
    # Skips reconstructions.
    if word.startswith("*"):
        return True
    # Skips multiword examples.
    if skip_spaces and (" " in word or "\u00A0" in word):
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
        title = member["title"]
        timestamp = member["timestamp"]
        config.restart_key = member["sortkey"]
        if _skip_word(title, config.skip_spaces_word) or _skip_date(
            timestamp, config.cut_off_date
        ):
            continue
        request = session.get(
            _PAGE_TEMPLATE.format(word=title), timeout=10, headers=HTTP_HEADERS
        )

        for word, pron in config.extract_word_pron(title, request, config):
            # Pronunciation processing is done in NFD-space;
            # we convert back to NFC afterwards.
            normalized_pron = unicodedata.normalize("NFC", pron)
            yield word, normalized_pron


def _language_name_for_scraping(language):
    """Handle cases where X is under a "macrolanguage" on Wiktionary.

    So far, only the Chinese languages necessitate this helper function.
    We'll keep this function as simple as possible, until it becomes too
    complicated and requires refactoring.
    """
    return (
        "Chinese"
        if language == "Cantonese" or language == "Min Nan"
        else language
    )


def scrape(config: Config) -> Iterator[WordPronPair]:
    """Scrapes with a given configuration."""
    category = _CATEGORY_TEMPLATE.format(
        language=_language_name_for_scraping(config.language)
    )
    requests_params: Dict[str, Any] = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": "500",
        "cmprop": "ids|title|timestamp|sortkey",
    }
    while True:
        data = requests.get(
            "https://en.wiktionary.org/w/api.php?",
            params=requests_params,
            headers=HTTP_HEADERS,
        ).json()
        try:
            yield from _scrape_once(data, config)
            if "continue" not in data:
                break
            continue_code = data["continue"]["cmcontinue"]
            # "cmstarthexsortkey" reset so as to avoid competition
            # with "continue_code".
            requests_params.update(
                {"cmcontinue": continue_code, "cmstarthexsortkey": None}
            )
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            requests_params.update({"cmstarthexsortkey": config.restart_key})
            # 5 minute timeout. Immediately restarting after the
            # connection has dropped appears to have led to
            # 'Connection reset by peer' errors.
            time.sleep(300)
