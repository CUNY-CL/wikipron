#!/usr/bin/env python
"""Downloads UniMorph morphological paradigms data."""
import json
import logging
import os
from typing import Dict
import time


#import requests in separate import block
import requests


UNIMORPH_DICT_PATH = "unimorph_languages.json"


def download():
    to_retry = {}
    os.makedirs("tsv")
    with open(UNIMORPH_DICT_PATH) as jfile:
        data_to_grab = json.load(jfile)
    for k, v in data_to_grab.items():
        with requests.get(data_to_grab[k], stream=True) as response:
            target_path = data_to_grab[k].split("/")[-1]
            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:
                with open(f"tsv/{target_path}.tsv", "w+") as sink:
                    print(response.text,file=sink)
            else:
                logging.info(
                "Status code %s while downloading %s",
                response.status_code,
                target_path
                )
            time.sleep(45)

       
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
