#!/usr/bin/env python
import json
import requests
from typing import Any, Dict
import logging
import os
import time

def download():
    os.makedirs("unimorph_for_split", exist_ok=True)
    with open("shared_task_lgs.json") as jfile:
        data_to_grab = json.load(jfile)
    #print(data_to_grab)
    urls = list(data_to_grab.values())
    #print(urls)
    #sprint(urls)
    lg_codes = list(data_to_grab.keys())
    print(data_to_grab["glg"])

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
download()


'''
    #with requests.get(x) as response:
    #    if response.status_code == 200:
    #        print(response.raw.read())
    #with requests.get(url,stream=True) as response:
        #if response.status_code == 200:
            #with open("ady.tsv","w") as f:
            #print(response.raw.read())


        # 30 seconds appears to not be enough, 60-70 seconds works well
        # but takes a long time.




def download(data_to_grab: Dict[str, Any]) -> Dict[str, Any]:
    to_retry = {}

    os.mkdir("morphology/unimorph_tsv")
    with open("shared_task_lgs.json") as jfile:
        data_to_grab = json.load(jfile)
    for language in data_to_grab:
        url = data_to_grab[language]
        with requests.get(url, stream=True) as response:
            target_path = url.split("/")[-1]
            logging.info("Downloading: %s", target_path)
            if response.status_code == 200:
                with open(f"tgz/{target_path}", "wb") as f:
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
    return(to_retry)
'''
