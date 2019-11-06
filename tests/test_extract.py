import inspect

import pytest

from wikipron.extract import EXTRACTION_FUNCTIONS


@pytest.mark.parametrize("func", EXTRACTION_FUNCTIONS.values())
def test_extraction_functions_have_the_same_signature(func):
    expected_args = ["word", "request", "config"]
    actual_args = list(inspect.signature(func).parameters.keys())
    assert expected_args == actual_args, (
        f"{func.__qualname__} does not have the expected function signature.",
    )
