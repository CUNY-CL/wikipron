
import pytest

from data.src.scrape import _build_scraping_config

# "mul" is code given to Translingual
@pytest.mark.parametrize(
    "config_settings, dialect_suffix, expected_file_name",
    [
        ({"key": "mul"}, "test_", "mul_test_phonetic.tsv"),
    ],
)
def test_something(config_settings, dialect_suffix, expected_file_name):
    # Create a spoof tsv directory
    _build_scraping_config(
        config_settings=config_settings, dialect_suffix=dialect_suffix
    )
    # Inspect contents of spoof tsv directory
    # Delete spoof tsv directory
