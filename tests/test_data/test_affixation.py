import os
import shutil

import pytest

from data.src.scrape import _build_scraping_config


PARENT_DIR = os.path.dirname(os.getcwd())

# "mul" is code given to Translingual by Wiktionary.
# Resolved to "Multiple Languages" by iso639 package.
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
            [
                "mul_test_phonetic.tsv",
                "mul_test_phonemic.tsv",
            ],
        ),
        # Standard
        (
            {"key": "mul"},
            "",
            False,
            [
                "mul_phonetic.tsv",
                "mul_phonemic.tsv",
            ],
        ),
    ],
)
def test_something(config_settings, dialect_suffix, phones, expected_file_name):
    tsv_path = f"{PARENT_DIR}/tsv"
    phones_path = f"{PARENT_DIR}/phones"
    os.mkdir(tsv_path)
    os.mkdir(phones_path)

    if phones:
        with open(
            f"{phones_path}/{config_settings['key']}_{dialect_suffix}phonetic.phones",
            "w",
        ) as f1:
            f1.write("a")
        with open(
            f"{phones_path}/{config_settings['key']}_{dialect_suffix}phonemic.phones",
            "w",
        ) as f2:
            f2.write("a")
    _build_scraping_config(
        config_settings=config_settings, dialect_suffix=dialect_suffix
    )
    contents = os.listdir(tsv_path)
    shutil.rmtree(tsv_path)
    shutil.rmtree(phones_path)

    for produced_file in contents:
        assert produced_file in expected_file_name
