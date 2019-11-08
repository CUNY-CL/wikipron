import pytest
import requests

from wikipron.extract import EXTRACTION_FUNCTIONS
from wikipron.extract.default import extract_word_pron_default


@pytest.mark.parametrize(
    "func",
    tuple(EXTRACTION_FUNCTIONS.values()) + (extract_word_pron_default,),
)
def test_extraction_functions_have_the_same_signature(func):
    expected_annotations = {
        "word": "Word",
        "request": requests.Response,
        "config": "Config",
        "return": "Iterator[WordPronPair]",
    }
    actual_annotations = func.__annotations__
    assert expected_annotations == actual_annotations, (
        f"{func.__qualname__} does not have the expected function signature.",
    )
