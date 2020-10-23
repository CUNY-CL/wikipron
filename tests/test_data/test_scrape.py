import os

from typing import Any, Dict, List

import pytest

from data.src.scrape import _build_scraping_config

from . import handle_dummy_files


# "mul" should be a future-proof iso639 code to test with.
# "mul" is resolved to "Multiple Languages" by iso639 package,
# which is a non-existent category on Wikitionary.
# An alternative solution to using "mul" would be to add
# a code to languagecodes.py explicitly for the purposes of testing.
@pytest.mark.parametrize(
    "config_settings, dialect_suffix, phones, expected_file_name",
    [
        # Dialect and phones
        (
            {"key": "mul"},
            "test_",
            True,
            [
                "mul_test_phonetic.tsv",
                "mul_test_phonemic.tsv",
                "mul_test_phonetic_filtered.tsv",
                "mul_test_phonemic_filtered.tsv",
            ],
        ),
        # Dialect
        (
            {"key": "mul"},
            "test_",
            False,
            ["mul_test_phonetic.tsv", "mul_test_phonemic.tsv"],
        ),
        # Standard
        (
            {"key": "mul"},
            "",
            False,
            ["mul_phonetic.tsv", "mul_phonemic.tsv"],
        ),
    ],
)
def test_file_creation(
    config_settings: Dict[str, Any],
    dialect_suffix: str,
    phones: bool,
    expected_file_name: List[str],
):
    """Check whether _build_scraping_config() outputs TSVs with expected
    file names based on presence or absence of dialect specification
    or .phones files for a given language.
    """
    dummy_tsv_path: str
    with handle_dummy_files(
        phones, config_settings["key"], dialect_suffix
    ) as dummy_tsv_path:
        _build_scraping_config(
            config_settings=config_settings, dialect_suffix=dialect_suffix
        )
        tsv_contents = os.listdir(dummy_tsv_path)

    for produced_file in tsv_contents:
        assert produced_file in expected_file_name
