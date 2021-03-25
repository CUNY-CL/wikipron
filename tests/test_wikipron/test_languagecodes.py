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
    for language, size in sizes.items():
        if size < _MIN_LANGUAGE_SIZE:
            continue
        if language in ("Mon", "Translingual"):
            # "mon" is the ISO 639 code for Mongolian, but there is also
            # the Mon language (ISO 639 code: "mnw").
            continue
        try:
            language_code = iso639.to_iso639_2(language)
        except iso639.NonExistentLanguageError:
            # Check if WikiPron can handle `language` directly.
            language_code = language
        try:
            language_inferred = wikipron.Config(key=language_code).language
        except iso639.NonExistentLanguageError:
            warnings.warn(f'WikiPron cannot handle "{language}".')
            continue
        if language_inferred != language:
            warnings.warn(
                f'WikiPron resolves the key "{language_code}" to '
                f'"{language_inferred}", '
                f'which is not "{language}" on Wiktionary.'
            )


def test_language_codes_dict_keys():
    """LANGUAGE_CODES keys must be in lowercase for Config._get_language."""
    for k in LANGUAGE_CODES.keys():
        assert k == k.lower()
