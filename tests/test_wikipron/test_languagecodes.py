import warnings

import iso639
import pytest

import wikipron
from data.scrape.lib.codes import _get_language_categories, _get_language_sizes
from wikipron.languagecodes import LANGUAGE_CODES

from . import can_connect_to_wiktionary

# We handle languages with at least this number of pronunciation entries.
_MIN_LANGUAGE_SIZE = 100


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
def test_language_coverage():
    """Check if WikiPron covers languages with a sufficient amount of data.

    If any warnings are raised, they should be suppressed by expanding
    the LANGUAGE_CODES dict to handle the relevant languages.
    """
    categories = _get_language_categories()
    sizes = _get_language_sizes(categories)
    unhandled = []
    mismatched = []
    for language, size in sizes.items():
        if size < _MIN_LANGUAGE_SIZE:
            continue
        if language in ("Hokkien", "Mon", "Translingual"):
            # "mon" is the ISO 639 code for Mongolian, but there is also
            # the Mon language (ISO 639 code: "mnw").
            # "Hokkien" is a variety of Min Nan; LANGUAGE_CODES maps it
            # to the existing Min Nan handler rather than as its own
            # language (see the "hokkien" dialect under nan in
            # languages.json).
            continue
        try:
            language_code = iso639.Language.match(language).part3
        except iso639.LanguageNotFoundError:
            # Check if WikiPron can handle `language` directly.
            language_code = language
        try:
            language_inferred = wikipron.Config(key=language_code).language
        except ValueError:
            unhandled.append(language)
            continue
        if language_inferred != language:
            mismatched.append((language_code, language_inferred, language))
    if unhandled:
        joined = ", ".join(f'"{lang}"' for lang in unhandled)
        warnings.warn(f"WikiPron cannot handle {joined}.")
    if mismatched:
        details = "; ".join(
            f'"{code}" -> "{inferred}" (not "{language}")'
            for code, inferred, language in mismatched
        )
        warnings.warn(
            f"WikiPron resolves keys to languages not on Wiktionary: "
            f"{details}."
        )


def test_language_codes_dict_keys():
    """LANGUAGE_CODES keys must be in lowercase for Config._get_language."""
    for k in LANGUAGE_CODES.keys():
        assert k == k.lower()
