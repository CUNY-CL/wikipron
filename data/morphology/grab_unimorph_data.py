#!/usr/bin/env python
"""Downloads UniMorph morphological paradigms data."""

import json
import logging
import os
import time

from typing import Dict

import requests


UNIMORPH_DICT_PATH = "unimorph_languages.json"


def download(data_to_grab: Dict[str, str]) -> Dict[str, str]:
    to_retry = {}
    os.mkdir("tsv")
    for language, url in data_to_grab.items():
        with requests.get(url, stream=True) as response:
            logging.info("Downloading: %s", language)
            if response.status_code == 200:
                with open(f"tsv/{language}.tsv", "wb") as f:
                    f.write(response.content)
            else:
                logging.info(
                    "Status code %d while downloading %s",
                    response.status_code,
                    language,
                )
                to_retry[language] = data_to_grab[language]
        # 30 seconds appears to not be enough, 60-70 seconds works well
        # but takes a long time.
        time.sleep(45)
    return to_retry


def main() -> None:
    with open(UNIMORPH_DICT_PATH, "r", encoding="utf-8") as langs:
        languages = json.load(langs)
    # Hack for repeatedly attempting to download Wortschatz data
    # as a way of getting around 404 response from their server.
    langs_to_retry = download(languages)
    while langs_to_retry:
        langs_to_retry = download(langs_to_retry)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()
