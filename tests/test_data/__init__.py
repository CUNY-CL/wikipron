import os
import shutil

from contextlib import contextmanager

_TESTS_DIR = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))
)
_TSV_PATH = f"{_TESTS_DIR}/tsv"
_PHONES_PATH = f"{_TESTS_DIR}/phones"

def write_files_dummy_phones_files(key: str, dialect: str):
    with open(
        f"{_PHONES_PATH}/{key}_{dialect}phonetic.phones",
        "w",
    ) as f1:
        f1.write("a")
    with open(
        f"{_PHONES_PATH}/{key}_{dialect}phonemic.phones",
        "w",
    ) as f2:
        f2.write("a")


@contextmanager
def handle_dummy_files(phones: bool, key: str, dialect: str):
    os.mkdir(_TSV_PATH)
    os.mkdir(_PHONES_PATH)
    print("IN CONTENXT MAANGER")
    if phones:
        write_files_dummy_phones_files(key, dialect)
    yield _TSV_PATH
    shutil.rmtree(_TSV_PATH)
    shutil.rmtree(_PHONES_PATH)
