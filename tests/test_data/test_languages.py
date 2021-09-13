import json
import os

_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
_LANGUAGES = os.path.join(_REPO_DIR, "data/scrape/lib/languages.json")


def test_casefold_value():
    """Check if each language in data/scrape/lib/languages.json
    has a value for 'casefold' key.
    """
    missing_languages = set()
    with open(_LANGUAGES, "r") as source:
        languages = json.load(source)
    for language in languages:
        if languages[language]["casefold"] is None:
            missing_languages.add(languages[language]["wiktionary_name"])

    assert not missing_languages, (
        "The following languages do not have a 'casefold' value "
        "in data/scrape/lib/languages.json:"
        f"{missing_languages}"
    )
