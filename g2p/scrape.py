"""Scraping Wiktionary data."""

import datetime
import io
import os
import re
from typing import Callable, Optional

import requests
import requests_html


# Queries for the MediaWiki backend.
# Documentation here: https://www.mediawiki.org/wiki/API:Categorymembers
_CATEGORY_TEMPLATE = "Category:{language}_terms_with_IPA_pronunciation"

_INITIAL_QUERY_TEMPLATE = (
    "https://en.wiktionary.org/w/api.php?"
    "action=query"
    "&format=json"
    "&list=categorymembers"
    "&cmtitle={category}"
    "&cmlimit=500"
    "&cmprop=ids|title|timestamp"
)
_CONTINUE_TEMPLATE = _INITIAL_QUERY_TEMPLATE + "&cmcontinue={cmcontinue}"

# Selects the content on the page.
_PAGE_TEMPLATE = "https://en.wiktionary.org/wiki/{word}"
_LI_SELECTOR_TEMPLATE = """
//li[
  sup[a[@title = "Appendix:{language} pronunciation"]]
  and
  span[@class = "IPA"]
  and
  ({dialect_selector})
]
"""
_SPAN_SELECTOR = '//span[@class = "IPA"]'
_PHONEMES = r"/(.+?)/"
_PHONES = r"\[(.+?)\]"  # FIXME: it doesn't grab anything now


class _Config:
    """Configuration for a scraping run.

    A configuration digests the settings for a scraping run and exposes
    various utilities. An important purpose is to create processing functions
    (e.g., cleaning pronunciations) that would otherwise require the
    inefficient checking of conditionals (e.g., whether to remove stress marks
    and syllable boundaries) at the inner for loops.
    """

    def __init__(
        self,
        language,
        phonetic,
        no_stress,
        no_syllable_boundaries,
        dialect,
        require_dialect_label,
        casefold,
        cut_off_date,
        output,
    ):
        _cut_off_date: str = self._get_cut_off_date(cut_off_date)
        self.output: Optional[io.TextIOWrapper] = self._get_output(output)
        self.casefold: Callable[[str], str] = self._get_casefold(casefold)
        self.process_pron: Callable[[str], str] = self._get_process_pron(
            no_stress, no_syllable_boundaries
        )
        self.process_word: Callable[[str, str], str] = self._get_process_word(
            _cut_off_date
        )
        self.ipa_regex: str = _PHONES if phonetic else _PHONEMES
        self.li_selector: str = self._get_li_selector(
            language, dialect, require_dialect_label
        )

    def _get_output(self, output):
        if output:
            if os.path.exists(output):
                os.remove(output)
            return open(output, "a")
        else:
            return None

    def _get_cut_off_date(self, cut_off_date):
        today = datetime.date.today()

        if not cut_off_date:
            return today.isoformat()

        try:
            d = datetime.date.fromisoformat(cut_off_date)
        except ValueError as e:
            msg = (
                "Cut-off date must be in ISO format (e.g., 2019-10-23): "
                f"{cut_off_date}"
            )
            raise ValueError(msg) from e

        if d > today:
            msg = (
                "Cut-off date cannot be later than today's date: "
                f"{cut_off_date}"
            )
            raise ValueError(msg)

        return cut_off_date

    def _get_casefold(self, casefold):
        if casefold:
            fn = lambda word: word.casefold()  # noqa: E731
        else:
            fn = lambda word: word  # noqa: E731

        def wrapper(word):
            return fn(word)

        return wrapper

    def _get_process_pron(self, no_stress, no_syllable_boundaries):
        processors = []
        if no_stress:
            processors.append(
                lambda pron: pron.replace("ˈ", "").replace("ˌ", "")
            )
        if no_syllable_boundaries:
            processors.append(lambda pron: pron.replace(".", ""))

        def wrapper(pron):
            for processor in processors:
                pron = processor(pron)
            return pron

        return wrapper

    def _get_li_selector(self, language, dialect, require_dialect_label):
        if not dialect:
            dialect_selector = "true"
        else:
            dialect_selector = f'span[a[@title = "w:{dialect}"]]'

        if not require_dialect_label:
            # include entries with no dialect specification
            dialect_selector += (
                ' or count(span[@class = "ib-content qualifier-content"]) = 0'
            )

        return _LI_SELECTOR_TEMPLATE.format(
            language=language, dialect_selector=dialect_selector
        )

    def _get_process_word(self, cut_off_date):
        def wrapper(word, date):
            # Skips multiword examples.
            if " " in word:
                return None
            # Skips examples containing a dash.
            if "-" in word:
                return None
            # Skips examples containing digits.
            if re.search(r"\d", word):
                return None
            # Skips examples available later than the cut-off date.
            if date > cut_off_date:
                return None
            return word

        return wrapper


def _yield_phn(request, config):
    for li in request.html.xpath(config.li_selector):
        for span in li.xpath(_SPAN_SELECTOR):
            m = re.search(config.ipa_regex, span.text)
            if m:
                yield m


def _scrape(data, config):
    session = requests_html.HTMLSession()
    entries = []
    for member in data["query"]["categorymembers"]:
        word = member["title"]
        date = member["timestamp"]
        word = config.process_word(word, date)
        if not word:
            continue
        request = session.get(_PAGE_TEMPLATE.format(word=word))
        # Template lookup is case-sensitive, but we case-fold afterwards.
        word = config.casefold(word)
        for m in _yield_phn(request, config):
            try:
                pron = m.group(1)  # FIXME: really need this try-except block?
            except IndexError:
                continue
            # Removes parens around various segments.
            pron = pron.replace("(", "").replace(")", "")
            # Skips examples with a space in the pron.
            if " " in pron:
                continue
            pron = config.process_pron(pron)
            entries.append((word, pron))

    output_entries = "\n".join(f"{word}\t{pron}" for word, pron in entries)
    if config.output:
        config.output.write(output_entries)
    else:
        print(output_entries)


def run(
    language,
    phonetic,
    no_stress,
    no_syllable_boundaries,
    dialect,
    require_dialect_label,
    casefold,
    cut_off_date,
    output,
):
    config = _Config(
        language,
        phonetic,
        no_stress,
        no_syllable_boundaries,
        dialect,
        require_dialect_label,
        casefold,
        cut_off_date,
        output,
    )
    category = _CATEGORY_TEMPLATE.format(language=language)
    next_query = _INITIAL_QUERY_TEMPLATE.format(category=category)
    while True:
        data = requests.get(next_query).json()
        _scrape(data, config)
        if "continue" not in data:
            break
        code = data["continue"]["cmcontinue"]
        next_query = _CONTINUE_TEMPLATE.format(
            category=category, cmcontinue=code
        )
