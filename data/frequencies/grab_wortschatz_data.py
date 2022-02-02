#!/usr/bin/env python
"""Downloads and decompresses Wortschatz frequency data."""

import argparse
import json
import logging
import os
import re
import tarfile
import time

from typing import Any, Dict

import requests


WORTSCHATZ_DICT_PATH = "wortschatz_languages.json"


def download(data_to_grab: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    to_retry = {}
    os.makedirs("tgz", exist_ok=True)
    codes = frozenset(key[:3] for key in data_to_grab)
    if args.restriction:
        restriction_set = frozenset(
            re.split(r"[;,\s]+\s*", args.restriction.strip(";, "))
        )
        if len(restriction_set) == 1 and not list(restriction_set)[0]:
            raise ValueError("Restriction flag raised but no language provided")
        if not restriction_set.issubset(codes):
            for key in restriction_set - codes:
                raise ValueError(f"{key} is not a valid ISO code", key)
    else:
        restriction_set = codes
    for language in data_to_grab:
        if language[:3] not in restriction_set:
            continue
        url = data_to_grab[language]["data_url"]
        with requests.get(url, stream=True) as response:
            target_path = url.split("/")[-1]
            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:
                with open(f"tgz/{target_path}", "wb") as sink:
                    sink.write(response.raw.read())
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
    os.makedirs("tsv", exist_ok=True)
    for tarball in os.listdir("tgz"):
        logging.info("Unpacking: %s", tarball)
        with tarfile.open(name=f"tgz/{tarball}", mode="r:gz") as tar_data:
            for file_entry in tar_data:
                if file_entry.name.endswith("words.txt"):
                    # Removes inconsistent path in tarballs
                    # so tsv has uniform contents.
                    file_entry.name = os.path.basename(file_entry.name)
                    tar_data.extract(file_entry, "tsv")


def main(args: argparse.Namespace) -> None:
    with open(WORTSCHATZ_DICT_PATH, "r", encoding="utf-8") as langs:
        languages = json.load(langs)
    # Hack for repeatedly attempting to download Wortschatz data
    # as a way of getting around 404 response from their server.
    langs_to_retry = download(languages, args)
    while langs_to_retry:
        langs_to_retry = download(langs_to_retry, args)
    unpack()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--restriction",
        help="restricts download to specified language(s)",
    )
    main(parser.parse_args())
