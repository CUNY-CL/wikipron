import pytest

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.core import (
    _expand_parens,
    _skip_parens,
    _skip_pron,
)
from wikipron.extract.default import extract_word_pron_default
from wikipron.html_utils import HTMLResponse


@pytest.mark.parametrize(
    "func",
    tuple(EXTRACTION_FUNCTIONS.values()) + (extract_word_pron_default,),
)
def test_extraction_functions_have_the_same_signature(func):
    expected_annotations = {
        "word": str,
        "request": HTMLResponse,
        "config": "Config",
        "return": "Iterator[WordPronPair]",
    }
    actual_annotations = func.__annotations__
    msg = f"{func.__qualname__}: unexpected function signature."
    assert expected_annotations == actual_annotations, msg


@pytest.mark.parametrize(
    "pron, iso639_key, skip_spaces, expected",
    [
        ("əbzɝvɚ", "eng", True, False),
        # GH-105: Dashed prons are skipped.
        ("ɑb-", "eng", True, True),
        # Spaces in Chinese prons are not skipped.
        ("ɕjɛ tu", "cmn", False, False),
        # Non-breaking spaces are not skipped.
        ("zinda ɡi", "per", False, False),
    ],
)
def test__skip_pron(pron, iso639_key, skip_spaces, expected):
    assert _skip_pron(pron, skip_spaces) == expected


@pytest.mark.parametrize(
    "pron, expected",
    [
        ("abc", "abc"),
        ("mɪskæɹəktəɹ(a)ɪzeɪʃən", "mɪskæɹəktəɹaɪzeɪʃən"),
        ("ən(d)iː", "əndiː"),
        ("a(b)c(d)e", "abcde"),
        ("(a)bc", "abc"),
        ("ab(c)", "abc"),
    ],
)
def test__skip_parens(pron, expected):
    assert _skip_parens(pron) == expected


@pytest.mark.parametrize(
    "pron, expected",
    [
        ("abc", ["abc"]),
        ("ən(d)iː", ["əndiː", "əniː"]),
        (
            "mɪskæɹəktəɹ(a)ɪzeɪʃən",
            [
                "mɪskæɹəktəɹaɪzeɪʃən",
                "mɪskæɹəktəɹɪzeɪʃən",
            ],
        ),
        (
            "a(b)c(d)e",
            ["abcde", "abce", "acde", "ace"],
        ),
        ("(a)bc", ["abc", "bc"]),
        ("ab(c)", ["abc", "ab"]),
        ("(a)(b)c", ["abc", "ac", "bc", "c"]),
    ],
)
def test__expand_parens(pron, expected):
    assert _expand_parens(pron) == expected
