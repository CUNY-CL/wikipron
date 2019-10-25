import datetime
import functools
import logging
import re

from typing import Callable, Optional

import iso639
import unicodedata

from wikipron.languagecodes import LANGUAGE_CODES

# GH-49: Estonian and Slovak use @title = "wikipedia:{language} phonology".
# GH-50: Korean has an extra "span" layer (for fonts) in //li[span[sup[a.
_LI_SELECTOR_TEMPLATE = """
//li[
  (.|span)[sup[a[
    @title = "Appendix:{language} pronunciation"
    or
    @title = "wikipedia:{language} phonology"
  ]]]
  and
  span[@class = "IPA"]
  {dialect_selector}
]
"""
_DIALECT_SELECTOR_TEMPLATE = (
    "and\n"
    '  (span[@class = "ib-content qualifier-content" and a[{dialects_text}]]\n'
    '   or count(span[@class = "ib-content qualifier-content"]) = 0)'
)
_PHONEMES_REGEX = r"/(.+?)/"
_PHONES_REGEX = r"\[(.+?)\]"

# unicodedata does not have a way to check "modifier" codepoints
# so we compile a set here.
# see https://en.wikipedia.org/wiki/Phonetic_symbols_in_Unicode
UNICODE_MODIFIERS = frozenset(
    [
        "ˡ",
        "ˍ",
        "ʲ",
        "ˠ",
        "˺",
        "ː",
        "˞",
        "˽",
        "ˬ",
        "˖",
        "ʰ",
        "ˤ",
        "˳",
        "˟",
        "ⁿ",
        "ʷ",
        "˕",
        "ˌ",
        "˷",
        "˔",
    ]
)


def _parse_combining_modifiers(pron: str) -> str:
    """Keep combining/modifier diacritics with the previous character and
    unambiguously segment IPA prons with added whitespace.
    """
    chars = []
    for char in pron:
        # Unicode has separate codepoints for combining and modifying chars
        # so we have to check for both.
        if unicodedata.combining(char) or char in UNICODE_MODIFIERS:
            last_char = chars.pop()
            chars.append(f"{last_char}{char}")
        else:
            chars.append(char)
    return " ".join(chars)


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
        casefold: bool = False,
        no_stress: bool = False,
        no_syllable_boundaries: bool = False,
        cut_off_date: Optional[str] = None,
        phonetic: bool = False,
        dialect: Optional[str] = None,
        no_segment: bool = False,
    ):
        self.language: str = self._get_language(key)
        self.casefold: Callable[[str], str] = self._get_casefold(casefold)
        self.process_pron: Callable[[str], str] = self._get_process_pron(
            no_stress, no_syllable_boundaries, no_segment
        )
        _cut_off_date: str = self._get_cut_off_date(cut_off_date)
        self.process_word: Callable[[str, str], str] = self._get_process_word(
            _cut_off_date
        )
        self.ipa_regex: str = _PHONES_REGEX if phonetic else _PHONEMES_REGEX
        self.li_selector: str = self._get_li_selector(self.language, dialect)

    def _get_language(self, key) -> str:
        key = key.lower().strip()
        if key.startswith("proto-"):
            language = "-".join(x.title() for x in key.split("-"))
            return language
        try:
            language = LANGUAGE_CODES[key]
        except KeyError:
            # In some cases it returns "Language; Dialect";
            # we just save the "first half".
            language = iso639.to_name(key).split(";")[0]
        logging.info('Language: "%s"', language)
        return language

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
        self, no_stress: bool, no_syllable_boundaries: bool, no_segment: bool
    ) -> Callable[[str], str]:

        processors = []
        if no_stress:
            processors.append(functools.partial(re.sub, r"[ˈˌ]", ""))
        if no_syllable_boundaries:
            processors.append(functools.partial(re.sub, r"\.", ""))
        if not no_segment:
            processors.append(_parse_combining_modifiers)

        prosodic_markers = frozenset(["ˈ", "ˌ", "."])

        def wrapper(pron):
            for processor in processors:
                pron = processor(pron)
            # GH-59: Skip prons that are empty, or have only stress marks or
            # syllable boundaries. The `any()` call is much faster than
            # re.match(r"[^ˈˌ.]", pron).
            if any(c not in prosodic_markers for c in pron):
                return pron

        return wrapper

    def _get_li_selector(self, language: str, dialect: Optional[str]) -> str:
        if not dialect:
            dialect_selector = ""
        else:
            dialect_selector = _DIALECT_SELECTOR_TEMPLATE.format(
                dialects_text=" or ".join(
                    f'text() = "{d.strip()}"' for d in dialect.split("|")
                )
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
