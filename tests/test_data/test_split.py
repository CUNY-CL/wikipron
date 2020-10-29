import collections
import json
import pytest
import os

from typing import Set

from data.src.split import _generalized_check

_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
_LANGUAGES = os.path.join(_REPO_DIR, "data/src/languages.json")

SmokeTestScript = collections.namedtuple(
    "SmokeTestScript", ("script", "samples")
)
SmokeTestScript.__doc__ = """
Represents a language to run a smoke test on.

Parameters
----------
script : str
    Unicode script name.
samples : list
    List of tuples containing samples of various scripts
    and a boolean reflecting whether those samples are
    within that Unicode script range.
"""

_SMOKE_TEST_LANGUAGES = [
    SmokeTestScript(
        "Han",
        [
            ("瀨尿蝦", True),
            ("Mandarin", False),
            ("กงสุล", False),
            ("烈日x空", False),
            ("た日當空", False),
        ],
    ),
    SmokeTestScript(
        "Hiragana",
        [
            ("あいきどう", True),
            ("Lucas", False),
            ("シミーズ", False),
            ("あいかイらず", False),
        ],
    ),
    SmokeTestScript(
        "Hebrew",
        [
            ("עליתא", True),
            ("мећава", False),
            ("עלbתא", False),
            ("πיתא", False),
        ],
    ),
    SmokeTestScript(
        "Syriac", [("ܐܒܝܕܘܬܐ", True), ("ܐܒܝܕאܬܐ", False), ("cܘܘl", False)]
    ),
    SmokeTestScript("Balinese", [("ᬰᬶᬮᬵ", True), ("ᬰнᬮᬰสุᬮᬵ", False)]),
    SmokeTestScript("Cyrillic", [("наиме", True), ("наиmе", False)]),
    SmokeTestScript("Gurmukhi", [("ਲੂੰਬੜੀ", True), ("ੁ", True), ("ਲਬลੜੀ", False)]),
    SmokeTestScript("Katakana", [("シニヨン", True), ("あいき", False), ("瀨", False)]),
    SmokeTestScript("Imperial Aramaic", [("𐡀𐡅𐡓𐡔𐡋𐡌", True), ("𐡀ܒ𐡓𐡔𐡋𐡌", False)]),
    SmokeTestScript("Latin", [("wikipron", True), ("ае", False), ("lịch", True)]),
    SmokeTestScript("Arabic", [("ژۇرنال", True), ("ژלرنال", False)]),
]


def _collect_scripts() -> Set[str]:
    scripts = set()
    with open(_LANGUAGES, "r") as source:
        languages = json.load(source)
    for language in languages:
        if "script" in languages[language]:
            for _, unicode_script in languages[language]["script"].items():
                scripts.add(unicode_script)
    return scripts


@pytest.mark.parametrize(
    "observed_scripts, known_scripts",
    [(_collect_scripts(), [lang.script for lang in _SMOKE_TEST_LANGUAGES])],
)
def test_script_coverage(observed_scripts, known_scripts):
    """All scripts added to languages.json must be
    included in the smoke test.
    """
    for script in observed_scripts:
        assert (
            script in known_scripts
        ), f"{script} must be included in _SCRIPTS."


@pytest.mark.parametrize("smoke_test_script,", _SMOKE_TEST_LANGUAGES)
def test_smoke_test_script(smoke_test_script):
    for sample, val in smoke_test_script.samples:
        assert _generalized_check(smoke_test_script.script, sample) == val
