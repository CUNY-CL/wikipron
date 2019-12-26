import json
import regex
import sys

# ../tsv/yid_phonetic.tsv
tsv_path = sys.argv[1]

with open("languages.json", "r") as lang_source:
    languages = json.load(lang_source)


def generalized_check(script, word):
    script = "{" + script + "}"
    regex_string = r"^\p{script}+$".format(script=script)
    # print(regex_string)
    return bool(regex.match(regex_string, word))


def iterate_through_file(tsv_path, unicode_script, path):
    with open(tsv_path, "r") as source:
        with open(path, "w") as destination:
            for line in source:
                word = line.split("\t", 1)[0]
                if generalized_check(unicode_script, word):
                    print(line.rstrip(), file=destination)


def check_file():
    iso639_code = tsv_path[tsv_path.rindex("/") + 1: tsv_path.index("_")]
    transcription_level = tsv_path[
        tsv_path.rindex("_") + 1:
    ]

    if "script" in languages[iso639_code]:
        if len(languages[iso639_code]["script"]) > 1:
            lang = languages[iso639_code]

            # Hacky way of filtering out the already split scripts.
            for script_prefix in lang["script"]:
                if script_prefix in tsv_path:
                    # Then this is a previously split file.
                    return

            # print("REMAINING", lang)
            for script_prefix, unicode_script in lang["script"].items():
                output_path = f"../tsv/{iso639_code}_{script_prefix}_{transcription_level}.tsv"
                iterate_through_file(tsv_path, unicode_script, output_path)


check_file()
