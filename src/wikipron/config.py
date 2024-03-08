import datetime
import functools
import logging
import re

from typing import Callable, Optional

import iso639
import segments

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.default import extract_word_pron_default
from wikipron.languagecodes import LANGUAGE_CODES
from wikipron.typing import ExtractFunc

# GH-49: Estonian and Slovak use @title = "wikipedia:{language} phonology".
# GH-50: Korean has an extra "span" layer (for fonts) in //li[span[sup[a.
# Some (but not all) Moksha pronunciations reside in //p[sup[a.
_PRON_XPATH_SELECTOR_TEMPLATE = """
(//li|//p)[
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
_DIALECT_XPATH_SELECTOR_TEMPLATE = (
    "and\n"
    '  (span[@class = "ib-content" and a[{dialects_text}]]\n'
    '   or count(span[@class = "ib-content"]) = 0)'
)
_PHONEMES_REGEX = r"/(.+?)/"
_PHONES_REGEX = r"\[(.+?)\]"

_TONES_REGEX = r"[˥˦˧˨˩⁰¹²³⁴⁵⁶⁷⁸⁹⁻◌̋ ◌̌ ◌̏ ◌̀ ◌́ ◌̂ ◌̄ ◌᷄◌᷅◌᷆◌᷇◌᷈◌᷉↑↓↗↘]"
_PARENS_REGEX = rf"⁽{_TONES_REGEX}+⁾"


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
        stress: bool = True,
        syllable_boundaries: bool = True,
        cut_off_date: Optional[str] = None,
        narrow: bool = False,
        dialect: Optional[str] = None,
        segment: bool = True,
        tone: bool = True,
        skip_spaces_word: bool = True,
        skip_spaces_pron: bool = True,
        skip_parens: bool = True,
    ):
        self.language: str = self._get_language(key)
        self.casefold: Callable[[str], str] = self._get_casefold(casefold)
        self.process_pron: Callable[[str], str] = self._get_process_pron(
            stress, syllable_boundaries, segment, tone
        )
        self.cut_off_date: str = self._get_cut_off_date(cut_off_date)
        self.ipa_regex: str = _PHONES_REGEX if narrow else _PHONEMES_REGEX
        self.pron_xpath_selector: str = self._get_pron_xpath_selector(
            self.language, dialect
        )
        self.dialect = dialect
        self.extract_word_pron: ExtractFunc = self._get_extract_word_pron(
            self.language
        )
        self.skip_spaces_word: bool = skip_spaces_word
        self.skip_spaces_pron: bool = skip_spaces_pron
        self.skip_parens: bool = skip_parens
        self.restart_key = None

    def _get_language(self, key: str) -> str:
        key = key.strip()
        if key.lower().startswith("proto-"):
            language = "-".join(x.title() for x in key.split("-"))
        else:
            try:
                language = LANGUAGE_CODES[key.lower()]
            except KeyError:
                func = iso639.Language.match
                try:
                    language = (
                        func(key) or func(key.lower()) or func(key.title())
                    ).name
                except iso639.LanguageNotFoundError:
                    raise ValueError(
                        f"Unrecognized language code or name: {key}"
                    )
        logging.info("Language: %r", language)
        return language

    def _get_cut_off_date(self, cut_off_date_str: Optional[str]) -> str:
        today = datetime.date.today()
        if not cut_off_date_str:
            logging.info("No cut-off date specified")
            return today.isoformat()
        try:
            cut_off_date = datetime.date.fromisoformat(cut_off_date_str)
        except ValueError as e:
            msg = (
                "Cut-off date must be in ISO format (e.g., 2019-10-23): "
                f"{cut_off_date_str}"
            )
            raise ValueError(msg) from e
        if cut_off_date > today:
            msg = (
                "Cut-off date cannot be later than today's date: "
                f"{cut_off_date_str}"
            )
            raise ValueError(msg)

        logging.info("Cut-off date: %r", cut_off_date_str)
        return cut_off_date_str

    def _get_casefold(self, casefold: bool) -> Callable[[str], str]:
        default_func: Callable[[str], str] = lambda word: word  # noqa: E731
        return self._casefold_word if casefold else default_func

    def _casefold_word(self, word: str) -> str:
        return str.casefold(word)

    def _get_process_pron(
        self,
        stress: bool,
        syllable_boundaries: bool,
        segment: bool,
        tone: bool,
    ) -> Callable[[str], str]:
        processors = []
        if not stress:
            processors.append(functools.partial(re.sub, r"[ˈˌ]", ""))
        if not syllable_boundaries:
            processors.append(functools.partial(re.sub, r"\.", ""))
        if not tone:
            processors.append(functools.partial(re.sub, _PARENS_REGEX, ""))
            processors.append(functools.partial(re.sub, _TONES_REGEX, ""))
        if segment:
            processors.append(
                functools.partial(segments.Tokenizer(), ipa=True)
            )
        prosodic_markers = frozenset(["ˈ", "ˌ", "."])

        def wrapper(pron: str):
            for processor in processors:
                pron = processor(pron)
            # GH-59: Skip prons that are empty, or have only stress marks or
            # syllable boundaries.
            if any(ch not in prosodic_markers for ch in pron):
                return pron

        return wrapper

    def _get_pron_xpath_selector(
        self, language: str, dialect: Optional[str]
    ) -> str:
        if not dialect:
            dialect_selector = ""
        else:
            dialect_selector = _DIALECT_XPATH_SELECTOR_TEMPLATE.format(
                dialects_text=" or ".join(
                    f'text() = "{d.strip()}"' for d in dialect.split("|")
                )
            )
            logging.info("Dialect(s): %r", dialect)

        return _PRON_XPATH_SELECTOR_TEMPLATE.format(
            language=language, dialect_selector=dialect_selector
        )

    def _get_extract_word_pron(self, language: str) -> ExtractFunc:
        try:
            extraction_function = EXTRACTION_FUNCTIONS[language]
            if self.dialect:
                logging.info(
                    "%r requires custom logic to handle its data from "
                    "Wiktionary. The dialect parameter, specified for "
                    "%r, may or may not work as desired. "
                    "If you notice any issues, please report them at "
                    "https://github.com/CUNY-CL/wikipron/issues.",
                    language,
                    self.dialect,
                )
        except KeyError:
            extraction_function = extract_word_pron_default

        def extract_word_pron_with_casefolding(*args, **kwargs):
            for word, pron in extraction_function(*args, **kwargs):
                yield self.casefold(word), pron

        return extract_word_pron_with_casefolding
