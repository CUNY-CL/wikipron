import pytest
import requests_html

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.core import _handle_parens, _skip_pron
from wikipron.extract.default import extract_word_pron_default


@pytest.mark.parametrize(
    "func", tuple(EXTRACTION_FUNCTIONS.values()) + (extract_word_pron_default,)
)
def test_extraction_functions_have_the_same_signature(func):
    expected_annotations = {
        "word": "Word",
        "request": requests_html,
        "config": "Config",
        "return": "Iterator[WordPronPair]",
    }
    actual_annotations = func.__annotations__
    assert expected_annotations == actual_annotations, (
        f"{func.__qualname__} does not have the expected function signature.",
    )


@pytest.mark.parametrize(
    "pron, iso639_key, skip_spaces, expected",
    [
        ("əbzɝvɚ", "eng", True, False),
        # GH-105: Dashed prons are skipped.
        ("ɑb-", "eng", True, True),
        # Spaces in Chinese prons are not skipped.
        ("ɕjɛ tu", "cmn", False, False),
        # Non-breaking spaces are not skipped.
        ("zinda ɡi", "per", False, False),
    ],
)
def test__skip_pron(pron, iso639_key, skip_spaces, expected):
    assert _skip_pron(pron, skip_spaces) == expected


@pytest.mark.parametrize(
    "input_pron, skip_parens, expected_pron",
    [
        ("mɪskæɹəktəɹ(a)ɪzeɪʃən", True, "mɪskæɹəktəɹaɪzeɪʃən"),
        ("mɪskæɹəktəɹ(a)ɪzeɪʃən", False, "mɪskæɹəktəɹ(a)ɪzeɪʃən"),
    ],
)
def test__handle_parens(input_pron, skip_parens, expected_pron):
    assert _handle_parens(input_pron, skip_parens) == expected_pron
