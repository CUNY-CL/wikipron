import os
import shutil

from contextlib import contextmanager

_TESTS_DIR = os.path.dirname(os.getcwd())
_TSV_PATH = f"{_TESTS_DIR}/tsv"
_PHONES_PATH = f"{_TESTS_DIR}/phones"


def write_dummy_phones_files(key: str, dialect: str) -> None:
    """Creates dummy .phones files in dummy phones directory."""
    with open(f"{_PHONES_PATH}/{key}_{dialect}phonetic.phones", "w",) as f1:
        f1.write("a")
    with open(f"{_PHONES_PATH}/{key}_{dialect}phonemic.phones", "w",) as f2:
        f2.write("a")


@contextmanager
def handle_dummy_files(phones: bool, key: str, dialect: str) -> str:
    """Creates and removes dummy directories for housing
    TSV and phones files."""
    os.mkdir(_TSV_PATH)
    os.mkdir(_PHONES_PATH)
    if phones:
        write_dummy_phones_files(key, dialect)
    yield _TSV_PATH
    shutil.rmtree(_TSV_PATH)
    shutil.rmtree(_PHONES_PATH)
