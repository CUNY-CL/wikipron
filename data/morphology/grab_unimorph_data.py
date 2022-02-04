#!/usr/bin/env python
"""Downloads UniMorph morphological paradigms data."""

import argparse
import json
import logging
import os
import time

from typing import Dict, List

import requests


_THIS_DIR = os.path.dirname(__file__)
UNIMORPH_DICT_PATH = os.path.join(_THIS_DIR, "unimorph_languages.json")


def download(data_to_grab: Dict[str, List[str]]) -> Dict[str, List[str]]:
    to_retry = {}
    os.makedirs("tsv", exist_ok=True)
    for language, urls in data_to_grab.items():
        with open(f"tsv/{language}.tsv", "wb") as sink:
            for url in urls:
                with requests.get(url, stream=True) as response:
                    logging.info("Downloading: %s", language)
                    if response.status_code == 200:
                        sink.write(response.content)
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


def main(args: argparse.Namespace) -> None:
    with open(args.unimorph_json_path, "r", encoding="utf-8") as langs:
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--unimorph-json-path",
        default=UNIMORPH_DICT_PATH,
        help="Path to the JSON file for the UniMorph download URLs",
    )
    main(parser.parse_args())
