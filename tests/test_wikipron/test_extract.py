import pytest
import requests

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.core import (
    _expand_parens,
    _skip_parens,
    _skip_pron,
)
from wikipron.extract.default import extract_word_pron_default
from wikipron.extract.eng import extract_word_pron_eng
from wikipron.html_utils import HTMLResponse

from . import config_factory


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


# A general pronunciation on an outer <li> with an accent variant nested in a
# sub-<li> (bus/cookie-type). The extractor must read only the line's own IPA
# (direct child), so the general /bʌs/ line does not also pull the nested
# /bʊs/. Under a US filter the nested non-US line is dropped entirely.
_GENERAL_OUTER_NESTED_ACCENT_HTML = """
<ul>
<li>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/bʌs/</span>
<ul>
<li>
<span class="ib-content"><span class="usage-label-accent">
<a title="w:English language">Northern England</a>
</span></span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/bʊs/</span>
</li>
</ul>
</li>
</ul>
"""


def _offline_response(html: str) -> HTMLResponse:
    response = requests.Response()
    # Declare the charset so libxml2 decodes the bytes as UTF-8 (real
    # Wiktionary pages carry a <meta charset> in their <head>).
    response._content = ('<meta charset="utf-8">' + html).encode("utf-8")
    return HTMLResponse(response)


@pytest.mark.parametrize(
    "extract_func", [extract_word_pron_default, extract_word_pron_eng]
)
def test_general_outer_extracts_own_ipa_only(extract_func):
    config = config_factory(key="en", dialect="US | General American")
    response = _offline_response(_GENERAL_OUTER_NESTED_ACCENT_HTML)
    prons = [pron for _, pron in extract_func("bus", response, config)]
    # Only the outer line's own IPA is read; the nested /bʊs/ (a non-US accent
    # variant) is neither pulled onto the general line nor selected on its own.
    assert prons == ["b ʌ s"]
