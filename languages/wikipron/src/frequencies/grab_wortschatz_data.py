#!/usr/bin/env python

import json
import logging
import os
import requests
import tarfile
import time

with open("wortschatz_languages.json", "r") as langs:
    languages = json.load(langs)


# Downloads the Wortschatz tarballs, roughly 10 GB of data.
def download(data_to_grab):
    to_retry = {}
    os.makedirs("tars", exist_ok=True)
    for language in data_to_grab:
        url = data_to_grab[language]["data_url"]
        with requests.get(url, stream=True) as response:
            target_path = url.split("/")[-1]
            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:
                with open(f"tars/{target_path}", "wb") as f:
                    f.write(response.raw.read())
            else:
                logging.info(
                    "Status code %s while downloading %s",
                    response.status_code,
                    target_path,
                )
                to_retry[language] = data_to_grab[language]
        # 30 seconds appears to not be enough, 60-70 seconds works well
        # but takes a long time.
        time.sleep(45)
    return to_retry


# Unpacks word frequency TSVs of tarballs, roughly 1 GB of data.
def unpack():
    os.mkdir("freq_tsvs")
    for tarball in os.listdir("tars"):
        logging.info("Unpacking: %s", tarball)
        with tarfile.open(name=f"tars/{tarball}", mode="r:gz") as tar_data:
            for file_entry in tar_data:
                if file_entry.name.endswith("words.txt"):
                    # Removes inconsistent path in tarballs
                    # so freq_tsvs has uniform contents.
                    file_entry.name = os.path.basename(file_entry.name)
                    tar_data.extract(file_entry, "freq_tsvs")


def main():
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
