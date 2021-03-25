import collections
import json
import pytest
import os

from typing import Set

from data.scrape.lib.languages_update import _detect_best_script_name
from data.scrape.lib.split import _generalized_check

_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
_LANGUAGES = os.path.join(_REPO_DIR, "data/scrape/lib/languages.json")

SmokeTestScript = collections.namedtuple(
    "SmokeTestScript", ("script", "samples")
)
SmokeTestScript.__doc__ = """
A script and a list of orthographic samples to run
a smoke test on.

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
    SmokeTestScript("Tagalog", [("ᜋᜇᜇᜌ", True), ("ᜋᜇᜇbᜌ", False)]),
    SmokeTestScript("Cyrillic", [("наиме", True), ("наиmе", False)]),
    SmokeTestScript(
        "Bengali",
        [
            ("ব্রাহ্মীকে", True),
            ("অসমীয়া", True),  # Assamese.
            ("दर्‍या", False),
        ],
    ),
    SmokeTestScript("Devanagari", [("ब्राह्मिक", True), ("ก ไก่", False)]),
    SmokeTestScript("Gujarati", [("બ્રાહ્મીક", True), ("ब्राह्मिक", False)]),
    SmokeTestScript(
        "Gurmukhi", [("ਲੂੰਬੜੀ", True), ("ੁ", True), ("ਲਬลੜੀ", False)]
    ),
    SmokeTestScript("Kannada", [("ಬ್ರಾಹ್ಮಿಕ್", True), ("Ⱆ", False)]),
    SmokeTestScript("Malayalam", [("ബ്രാഹ്മിക്", True), ("Ⱆ", False)]),
    SmokeTestScript("Oriya", [("ବ୍ରାହ୍ମୀସି", True), ("Ⱆ", False)]),
    SmokeTestScript("Sinhala", [("බ්රාහ්මික්", True), ("Ⱆ", False)]),
    SmokeTestScript("Tamil", [("பிராமிக்", True), ("Ⱆ", False)]),
    SmokeTestScript("Telugu", [("బ్రహ్మికి", True), ("Ⱆ", False)]),
    SmokeTestScript(
        "Katakana", [("シニヨン", True), ("あいき", False), ("瀨", False)]
    ),
    SmokeTestScript("Imperial Aramaic", [("𐡀𐡅𐡓𐡔𐡋𐡌", True), ("𐡀ܒ𐡓𐡔𐡋𐡌", False)]),
    SmokeTestScript(
        "Latin", [("wikipron", True), ("ае", False), ("lịch", True)]
    ),
    SmokeTestScript("Arabic", [("ژۇرنال", True), ("ژלرنال", False)]),
    SmokeTestScript(
        "Lao", [("ກັບຄືນ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Gothic", [("𐌰𐌲𐌲𐌹𐌻𐌿𐍃", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Inherited", [("ٔ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Tai Tham", [("ᨾᩮᩥ᩠ᨦ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Old Italic",
        [("𐌃𐌖𐌄𐌍𐌏𐌔", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Thai", [("กะเตาแด็ร", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Greek", [("β", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "New Tai Lue",
        [("ᦺᦘᧈᦵᦙᦲᧂ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Canadian Aboriginal",
        [("ᐊᔨᓈᓀᐤ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Myanmar",
        [("တင်ႇငူင်း", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Hangul", [("ᄀᆞᆨ다기", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Tibetan",
        [("ཀ་ཏ་མན་ཏུ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Syloti Nagri",
        [("ꠀꠁꠎꠇꠣꠁꠟ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Mongolian", [("ᠠᠨᡨᠠᡥᠠ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Khmer", [("កង់ហ្គូរូ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Javanese",
        [("ꦧꦲꦸꦱꦱ꧀ꦠꦿ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Common", [("ʻ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Coptic", [("ϣⲙⲏⲛ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Ahom", [("𑜀𑜦𑜡𑜀𑜨𑜈𑜫𑜍", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Armenian",
        [("ֆրիուլերեն", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Limbu",
        [("ᤀᤠᤀᤡᤴᤋᤠᤴᤍᤡᤰ", True), ("ژלرنال", False), ("wikipron", False)],
    ),
    SmokeTestScript(
        "Bopomofo", [("ㄅㄆㄇㄈ", True), ("ژלرنال", False), ("wikipron", False)]
    ),
    SmokeTestScript(
        "Georgian",
        [("ააბარგებს", True), ("ژלرنال", False), ("wikipron", False)],
    ),
]


def _collect_scripts() -> Set[str]:
    scripts = set()
    with open(_LANGUAGES, "r") as source:
        languages = json.load(source)
    for lang in languages:
        if "script" in languages[lang]:
            for unicode_script in languages[lang]["script"].values():
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
        ), f"{script} must be included in the smoke test."


@pytest.mark.parametrize("smoke_test_script,", _SMOKE_TEST_LANGUAGES)
def test_smoke_test_script(smoke_test_script):
    """Checks whether the scripts we'd like to split are appropriately handled
    by the Unicode script property."""
    for script_sample, predicted_truth_val in smoke_test_script.samples:
        assert (
            _generalized_check(smoke_test_script.script, script_sample, "")
            == predicted_truth_val
        )


@pytest.mark.parametrize("smoke_test_script,", _SMOKE_TEST_LANGUAGES)
def test_script_detection_strict(smoke_test_script):
    """Checks whether the scripts we'd like to split are correctly detected
    given the samples."""
    for script_sample, predicted_truth_val in smoke_test_script.samples:
        result = _detect_best_script_name(script_sample)
        predicted_script = result.replace("_", " ") if result else None
        status = predicted_script == smoke_test_script.script
        assert status == predicted_truth_val, (
            f"{script_sample}: {smoke_test_script.script} predicted"
            f" as {predicted_script}."
        )


def test_script_detection_basic():
    # Check mixing the scripts: Kharoṣṭhī and Brāhmī, with a longer segment
    # corresponding to Brāhmī.
    text = "𐨑𐨪𐨆𐨯𐨠𐨁𑀘𑀠𑀬𑁄𑀰𑀺𑀣𑁄"
    assert not _detect_best_script_name(text)  # Not allowed in strict mode.
    script = _detect_best_script_name(text, strict=False)
    assert script == "Brahmi"
