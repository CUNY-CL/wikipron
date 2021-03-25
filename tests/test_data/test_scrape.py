import os
import tempfile

from typing import List

import pytest

from data.scrape.scrape import _build_scraping_config


def write_dummy_phones_files(phones_dir, key: str, dialect: str) -> None:
    """Creates dummy .phones files in dummy phones directory."""
    open(
        f"{phones_dir}/{key}_{dialect}phonetic.phones", "w", encoding="utf-8"
    ).close()
    open(
        f"{phones_dir}/{key}_{dialect}phonemic.phones", "w", encoding="utf-8"
    ).close()


# "mul" should be a future-proof iso639 code to test with.
# "mul" is resolved to "Multiple Languages" by iso639 package,
# which is a non-existent category on Wikitionary.
# An alternative solution to using "mul" would be to add
# a code to languagecodes.py explicitly for the purposes of testing.
@pytest.mark.parametrize(
    "iso_key, dialect_affix, phones, expected_file_name",
    [
        # Dialect and phones
        (
            "mul",
            "test_",
            True,
            [
                "mul_test_phonetic.tsv",
                "mul_test_phonemic.tsv",
                "mul_test_phonetic_filtered.tsv",
                "mul_test_phonemic_filtered.tsv",
            ],
        ),
        # Phones
        (
            "mul",
            "",
            True,
            [
                "mul_phonetic.tsv",
                "mul_phonemic.tsv",
                "mul_phonetic_filtered.tsv",
                "mul_phonemic_filtered.tsv",
            ],
        ),
        # Dialect
        (
            "mul",
            "test_",
            False,
            ["mul_test_phonetic.tsv", "mul_test_phonemic.tsv"],
        ),
        # Standard
        (
            "mul",
            "",
            False,
            ["mul_phonetic.tsv", "mul_phonemic.tsv"],
        ),
    ],
)
def test_file_creation(
    iso_key: str,
    dialect_affix: str,
    phones: bool,
    expected_file_name: List[str],
):
    """Check whether _build_scraping_config() outputs TSVs with expected
    file names based on presence or absence of dialect specification
    or .phones files for a given language.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(f"{temp_dir}/tsv")
        os.mkdir(f"{temp_dir}/phones")
        if phones:
            write_dummy_phones_files(
                f"{temp_dir}/phones", iso_key, dialect_affix
            )
        _build_scraping_config(
            config_settings={"key": iso_key},
            path_affix=f"{temp_dir}/tsv/{iso_key}_{dialect_affix}",
            phones_path_affix=f"{temp_dir}/phones/{iso_key}_{dialect_affix}",
        )
        tsv_contents = os.listdir(f"{temp_dir}/tsv")

    for produced_file in tsv_contents:
        assert produced_file in expected_file_name
