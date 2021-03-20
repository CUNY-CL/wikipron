#!/usr/bin/env python
"""Downloads and decompresses Wortschatz frequency data."""

import json
import logging
import os
import tarfile
import time

from typing import Any, Dict

import requests


WORTSCHATZ_DICT_PATH = "wortschatz_languages.json"


def download(data_to_grab: Dict[str, Any]) -> Dict[str, Any]:
    to_retry = {}
    os.mkdir("tgz")
    for language in data_to_grab:
        url = data_to_grab[language]["data_url"]
        with requests.get(url, stream=True) as response:
            target_path = url.split("/")[-1]
            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:
                with open(f"tgz/{target_path}", "wb") as f:
                    f.write(response.raw.read())
            else:
                logging.info(
                    "Status code %d while downloading %s",
                    response.status_code,
                    target_path,
                )
                to_retry[language] = data_to_grab[language]
        # 30 seconds appears to not be enough, 60-70 seconds works well
        # but takes a long time.
        time.sleep(45)
    return to_retry


def unpack() -> None:
    os.mkdir("tsv")
    for tarball in os.listdir("tgz"):
        logging.info("Unpacking: %s", tarball)
        with tarfile.open(name=f"tgz/{tarball}", mode="r:gz") as tar_data:
            for file_entry in tar_data:
                if file_entry.name.endswith("words.txt"):
                    # Removes inconsistent path in tarballs
                    # so tsv has uniform contents.
                    file_entry.name = os.path.basename(file_entry.name)
                    tar_data.extract(file_entry, "tsv")


def main() -> None:
    with open(WORTSCHATZ_DICT_PATH, "r", encoding="utf-8") as langs:
        languages = json.load(langs)
    # Hack for repeatedly attempting to download Wortschatz data
    # as a way of getting around 404 response from their server.
    langs_to_retry = download(languages)
    while langs_to_retry:
        langs_to_retry = download(langs_to_retry)
    unpack()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
