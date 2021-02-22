import collections
import json
import operator
import os
import sys

import unicodedataplus

from typing import Dict, Tuple, Union
def _detect_best_script_name(
    word: str, strict: bool = True
) -> Union[Tuple[str, float], None]:
    """Returns the most likely script name (rather than ISO 15924 code) the
    word belongs to along with the corresponding confidence expressed as a
    maximum likelihood estimate computed over the `word` sample. If `strict`
    is enabled, then all the characters must belong to the same script and
    `(None, None)` is returned on failure.

    Example: "ژۇرنال" -> ("Arabic", 1.0).
    """
    script_counts: Dict[str, float] = collections.defaultdict(float)
    for char in word:
        script_counts[unicodedataplus.script(char)] += 1.0
    script_probs = [(s, script_counts[s] / len(word)) for s in script_counts]
    script_probs.sort(key=operator.itemgetter(1), reverse=True)
    if strict and len(script_probs) != 1:
        return None
    else:
        # The script names in Unicode data tables have underscores instead of
        # whitespace to enable parsing. See:
        #   https://www.unicode.org/Public/13.0.0/ucd/Scripts.txt
        return script_probs[0][0].replace("_", " "), script_probs[0][1]


def _update_languages_json(tsv_path: str, output_path: str) -> None:

        orth_dict = dict()

        for file in os.listdir(tsv_path):
            if file.endswith('.tsv'):
                with open(f'{tsv_path}/{file}', "r", encoding="utf-8") as f:
                    title = str(file)
                    with open(f'{output_path}/test_languages.json', "w", encoding="utf-8") as output_tsv:
                        orth_dict[title] = {
                            "scripts": {}
                        }
                        for line in f:
                            try:
                                word = line.split("\t", 1)[0]
                                script, prob = _detect_best_script_name(word)
                                if not script in orth_dict[file]["scripts"]:
                                    orth_dict[file]["scripts"][script] = prob
                            except TypeError as error:
                                pass
                        json_object = json.dumps(orth_dict, indent = 4)

                        output_tsv.write(json_object)

        return json_object


def main():
    '''
    basically want to test out how each of the functions in split.py work
    and where the best place to insert _detect_best_script_name would be.
    '''
    tsv_path = sys.argv[1]
    output_path = sys.argv[2]

    _update_languages_json(tsv_path, output_path)

if __name__ == "__main__":
    main()