import re
import warnings

from typing import Dict, List

import iso639
import pytest
import requests

import wikipron
from wikipron.languagecodes import LANGUAGE_CODES

from . import can_connect_to_wiktionary


_URL = "https://en.wiktionary.org/w/api.php"
# We handle languages with at least this number of pronunciation entries.
_MIN_LANGUAGE_SIZE = 100


def _get_language_categories() -> List[str]:
    """Get the list of language categories from Wiktionary.

    A category looks like "Category:Bengali terms with IPA pronunciation".

    Reference:
    https://en.wiktionary.org/w/index.php?title=Category:Terms_with_IPA_pronunciation_by_language
    """
    requests_params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:Terms with IPA pronunciation by language",
        "cmlimit": "500",
    }
    language_categories = []
    while True:
        data = requests.get(_URL, params=requests_params).json()
        for member in data["query"]["categorymembers"]:
            category = member["title"]
            language_categories.append(category)
        if "continue" not in data:
            break
        continue_code = data["continue"]["cmcontinue"]
        requests_params.update({"cmcontinue": continue_code})
    return language_categories


def _get_language_sizes(categories: List[str]) -> Dict[str, int]:
    """Get the map from a language to its number of pronunciation entries."""
    language_sizes = {}
    # MediaWiki API can retrieve sizes for multiple categories at a time,
    # but would complain about too many language categories for each API call.
    chunk_size = 50
    for start in range(0, len(categories), chunk_size):
        end = start + chunk_size
        requests_params = {
            "action": "query",
            "format": "json",
            "prop": "categoryinfo",
            "titles": "|".join(categories[start:end]),
        }
        data = requests.get(_URL, params=requests_params).json()
        for page in data["query"]["pages"].values():
            size = page["categoryinfo"]["size"]
            language = re.search(
                r"Category:(.+?) terms with IPA pronunciation", page["title"]
            ).group(1)
            language_sizes[language] = size
    return language_sizes


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
