import pytest
import requests_html

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.core import _skip_pron
from wikipron.extract.default import extract_word_pron_default
from . import config_factory


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
    "pron, iso639_key, no_skip_spaces, expected",
    [
        ("əbzɝvɚ", "eng", False, False),
        # GH-105: Dashed prons are skipped.
        ("ɑb-", "eng", False, True),
        # Spaces in Chinese prons are not skipped.
        ("ɕjɛ tu", "cmn", True, False),
        # Non-breaking spaces are not skipped.
        ("zinda ɡi", "per", True, False),
    ],
)
def test__skip_pron(pron, iso639_key, no_skip_spaces, expected):
    config = config_factory(key=iso639_key, no_skip_spaces_pron=no_skip_spaces)
    assert _skip_pron(pron, config) == expected
