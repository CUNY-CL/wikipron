"""Scraping grapheme-to-phoneme data from Wiktionary."""

import argparse
import datetime
import functools
import logging
import re
import sys

from typing import Callable, Iterator, List, Optional, TextIO, Tuple

try:
    import iso639
    import requests
    import requests_html
except ModuleNotFoundError:
    logging.warning(
        "Thirty-party packages are not imported. "
        "This situation should arise only in the installation phase, "
        "where setup.py runs and imports this present module."
    )


__version__ = "0.1.1"

Pair = Tuple[str, str]


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
_DIALECT_SELECTOR_TEMPLATE = (
    'span[@class = "ib-content qualifier-content" and a[{dialects_text}]]'
)
_SPAN_SELECTOR = '//span[@class = "IPA"]'
_PHONEMES_REGEX = r"/(.+?)/"
_PHONES_REGEX = r"\[(.+?)\]"


# Map from a ISO 639 code to its non-ISO 639 Wiktionary language name.
# ISO 639-3: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab  # noqa: E501
# Wiktionary: https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language  # noqa: E501
# TODO: Expand this as needed to cover additional languages.
_LANGUAGE_CODES = {
    # Greek. Would have been "Modern Greek (1453-)" in ISO 639.
    "el": "Greek",
    "ell": "Greek",
    "gre": "Greek",
    "greek": "Greek",
    # Slovene. Would have been "Slovenian" in ISO 639.
    "sl": "Slovene",
    "slv": "Slovene",
    "slovene": "Slovene",
    "slovenian": "Slovene",
}


class Config:
    """Configuration for a scraping run.

    A configuration digests the settings for a scraping run and exposes
    various utilities. An important purpose is to create processing functions
    (e.g., cleaning pronunciations) that would otherwise require the
    inefficient checking of conditionals (e.g., whether to remove stress marks
    and syllable boundaries) at the inner for loops.
    """

    def __init__(
        self,
        *,
        key: str,
        output: Optional[str] = None,
        casefold: bool = False,
        no_stress: bool = False,
        no_syllable_boundaries: bool = False,
        cut_off_date: Optional[str] = None,
        phonetic: bool = False,
        dialect: Optional[str] = None,
        require_dialect_label: bool = False,
    ):
        self.language: str = self._get_language(key)
        self.output: Optional[str] = self._get_output(output)
        self.casefold: Callable[[str], str] = self._get_casefold(casefold)
        self.process_pron: Callable[[str], str] = self._get_process_pron(
            no_stress, no_syllable_boundaries
        )
        _cut_off_date: str = self._get_cut_off_date(cut_off_date)
        self.process_word: Callable[[str, str], str] = self._get_process_word(
            _cut_off_date
        )
        self.ipa_regex: str = _PHONES_REGEX if phonetic else _PHONEMES_REGEX
        self.li_selector: str = self._get_li_selector(
            self.language, dialect, require_dialect_label
        )

    def _get_language(self, key) -> str:
        key = key.lower().strip()
        try:
            language = _LANGUAGE_CODES[key]
        except KeyError:
            # In some cases it returns "Language; Dialect";
            # we just save the "first half".
            language = iso639.to_name(key).split(";")[0]
        logging.info('Language: "%s"', language)
        return language

    def _get_output(self, output: Optional[str]) -> Optional[TextIO]:
        return open(output, "w") if output else sys.stdout

    def _get_cut_off_date(self, cut_off_date: Optional[str]) -> str:
        today = datetime.date.today()

        if not cut_off_date:
            logging.info("No cut-off date specified")
            return today.isoformat()

        try:
            # TODO: when we require Python 3.7+ later, we can do this:
            #  d = datetime.date.fromisoformat(cut_off_date)
            d = datetime.datetime.strptime(cut_off_date, "%Y-%m-%d").date()
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

        logging.info('Cut-off date: "%s"', cut_off_date)
        return cut_off_date

    def _get_casefold(self, casefold: bool) -> Callable[[str], str]:
        return str.casefold if casefold else lambda word: word  # noqa: E731

    def _get_process_pron(
        self, no_stress: bool, no_syllable_boundaries: bool
    ) -> Callable[[str], str]:
        processors = []
        if no_stress:
            processors.append(functools.partial(re.sub, r"[ˈˌ]", ""))
        if no_syllable_boundaries:
            processors.append(functools.partial(re.sub, r"\.", ""))

        def wrapper(pron):
            for processor in processors:
                pron = processor(pron)
            return pron

        return wrapper

    def _get_li_selector(
        self,
        language: str,
        dialect: Optional[str],
        require_dialect_label: bool,
    ) -> str:
        if require_dialect_label and not dialect:
            raise ValueError(
                "When --require-dialect-label is used, "
                "--dialect must also be used."
            )

        if not dialect:
            dialect_selector = "true()"
        else:
            dialect_selector = _DIALECT_SELECTOR_TEMPLATE.format(
                dialects_text=" or ".join(
                    f'text() = "{d.strip()}"' for d in dialect.split("|")
                )
            )

        if not require_dialect_label:
            # include entries with no dialect specification
            dialect_selector += (
                "\n   "
                'or count(span[@class = "ib-content qualifier-content"]) = 0'
            )

        return _LI_SELECTOR_TEMPLATE.format(
            language=language, dialect_selector=dialect_selector
        )

    def _get_process_word(
        self, cut_off_date: Optional[str]
    ) -> Callable[[str, str], str]:
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


def _yield_phn(request, config: Config):
    for li in request.html.xpath(config.li_selector):
        for span in li.xpath(_SPAN_SELECTOR):
            m = re.search(config.ipa_regex, span.text)
            if m:
                yield m


def _scrape_once(data, config: Config) -> Iterator[Pair]:
    session = requests_html.HTMLSession()
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
                pron = m.group(1)
            except IndexError:
                continue
            # Removes parens around various segments.
            pron = pron.replace("(", "").replace(")", "")
            # Skips examples with a space in the pron.
            if " " in pron:
                continue
            pron = config.process_pron(pron)
            yield (word, pron)


def scrape(config: Config) -> Iterator[Pair]:
    """Scrapes with a given configuration."""
    category = _CATEGORY_TEMPLATE.format(language=config.language)
    next_query = _INITIAL_QUERY_TEMPLATE.format(category=category)
    while True:
        data = requests.get(next_query).json()
        yield from _scrape_once(data, config)
        if "continue" not in data:
            break
        code = data["continue"]["cmcontinue"]
        next_query = _CONTINUE_TEMPLATE.format(
            category=category, cmcontinue=code
        )


def _scrape_and_write(config: Config) -> None:
    for i, (word, pron) in enumerate(scrape(config), 1):
        print(f"{word}\t{pron}", file=config.output)
        if i % 100 == 0:
            logging.info("%d pronunciations scraped", i)


def _get_cli_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "key", help="Key (i.e., name or ISO-639 code) for the language"
    )
    parser.add_argument(
        "--phonetic",
        action="store_true",
        help=(
            "Retrieve the [phonetic] transcriptions "
            "rather than the /phonemic/ ones."
        ),
    )
    parser.add_argument(
        "--no-stress",
        action="store_true",
        help="Remove stress marks in pronunciations.",
    )
    parser.add_argument(
        "--no-syllable-boundaries",
        action="store_true",
        help="Remove syllable boundary marks in pronunciations.",
    )
    parser.add_argument(
        "--dialect",
        help=(
            "Retrieve entries that have this dialect specification. "
            "If not given, then all dialects are included in the output. "
            "The dialect name is found together with the IPA transcription, "
            'e.g., "UK" or "US" in "(UK, US) IPA: /təˈmɑːtəʊ/". '
            'To include more than one dialect, use a pipe "|" to separate '
            'the dialect names, e.g., --dialect="General American | US".'
        ),
    )
    parser.add_argument(
        "--require-dialect-label",
        action="store_true",
        help=(
            "Include only entries that have a dialect specification. "
            "If applied, then --dialect must also be used."
        ),
    )
    parser.add_argument(
        "--casefold",
        action="store_true",
        help="Apply case-folding to the orthography.",
    )
    parser.add_argument(
        "--cut-off-date",
        help=(
            "Retrieve only entries that were added to Wiktionary "
            "on or before this date (in ISO format, e.g., 2018-10-23). "
            "If not given, today's date is used."
        ),
    )
    parser.add_argument(
        "--output",
        help=(
            "Output filename. If the output file already exists, it will be "
            "overridden. If not given, results appear in stdout."
        ),
    )
    return parser.parse_args(args)


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level="INFO")
    args = _get_cli_args(sys.argv[1:])
    config = Config(**args.__dict__)
    _scrape_and_write(config)
