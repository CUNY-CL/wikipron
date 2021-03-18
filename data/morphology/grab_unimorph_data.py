#!/usr/bin/env python
"""Downloads UniMorph morphological paradigms data."""

import json
import logging
import os
import requests
import time
start_time = time.time()
from typing import Dict




UNIMORPH_DICT_PATH = "unimorph_languages.json"


def download():
    #start_time = time.time()

    os.makedirs("unimorph_for_split", exist_ok=True)
    with open("unimorph_languages.json") as jfile:
        data_to_grab = json.load(jfile)
    #print(data_to_grab)
    urls = list(data_to_grab.values())
    #print(urls)
    #sprint(urls)
    lg_codes = list(data_to_grab.keys())
    #print(data_to_grab["glg"])

    for i in range(len(urls)):
        with requests.get(urls[i], stream=True) as response:
            target_path = urls[i].split("/")[-1]
            #print(target_path)

            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:

                #unimorph/fao/master
                with open(f"unimorph_for_split/{target_path}.tsv", "w+") as sink:
                    #print(response.text)
                    print(response.text,file=sink)
            elif target_path == "glg":
                with requests.get(data_to_grab["glg"], stream=True) as response:
                    logging.info("Downloading: %s", target_path)
                    if response.status_code == 200:
                        with open(f"unimorph_for_split/glg.tsv", "w+") as sink:
                            print(response.text,file=sink)

                        #unimorph/fao/master
                        #with open(f"unimorph_for_split/gal.tsv", "w+") as sink:
                            #print(response.text)
                            #print(response.text,file=sink)
                    elif target_path == "geo":
                        with requests.get(data_to_grab["glg"], stream=True) as response:
                            logging.info("Downloading: %s", target_path)
                            if response.status_code == 200:
                                with open(f"unimorph_for_split/glg.tsv", "w+") as sink:
                                    print(response.text,file=sink)

            else:
                logging.info(
                "Status code %s while downloading %s",
                response.status_code,
                target_path
                )

            time.sleep(45)
#download()


def main() -> None:
    #with open(UNIMORPH_DICT_PATH, "r", encoding="utf-8") as langs:
    #    languages = json.load("unimorph_languages.json")
    # Hack for repeatedly attempting to download Wortschatz data
    # as a way of getting around 404 response from their server.
    #langs_to_retry = download(languages)
    #while langs_to_retry:
    #    langs_to_retry = download(langs_to_retry)
    download()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    print("--- %s seconds ---" % (time.time() - start_time))
    main()
