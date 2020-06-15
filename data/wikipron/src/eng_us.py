#!/usr/bin/env python
"""
* rewrite "o ɹ" as "ɔ ɹ"
* rewrite "ɛ ə" as "æ" (TRAP)
* rewrite "i ɹ" as "ɪ ɹ" (NEAR)
* rewrite "ə ʊ" as "o ʊ" (GOAT)
* rewrite "ɒ" as "ɔ" (CLOTH/THOUGHT)
"""

from typing import List


SOURCE = "../tsv/eng_us_phonemic.tsv"
PAIRS = [
    ("o ɹ", "ɔ ɹ"),
    ("ɛ ə", "æ"),
    ("i ɹ", "ɪ ɹ"),
    ("ə ʊ", "o ʊ"),
    ("ɒ", "ɔ"),
]


def _find(corpus: List[str], query: List[str]) -> int:
    qlen = len(query)
    if len(corpus) < qlen:
        return -1
    for i in range(len(corpus)):
        if corpus[i : i + qlen] == query:
            return i
    return -1


def _replace(corpus: List[str], query: List[str], rep: List[str]) -> List[str]:
    index = _find(corpus, query)
    if index == -1:
        return corpus
    return corpus[:index] + rep + corpus[index + len(query) :]


def main() -> None:
    with open(SOURCE, "r") as source:
        for line in source:
            (word, phonestr) = line.split("\t", 1)
            phones = phonestr.split()
            for (query, rep) in PAIRS:
                phones = _replace(phones, query.split(), rep.split())
            print(f"{word}\t{' '.join(phones)}")


if __name__ == "__main__":
    main()
