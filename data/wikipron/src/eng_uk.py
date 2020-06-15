#!/usr/bin/env python
"""
* rewrite "ɛ ə" as "ɛː"
* rewrite "a ɹ" as "æ ɹ"
* rewrite "ɪ i" as "iː" (FLEECE)
* rewrite "ɪ ə" as "ɪː" (NEAR)
* rewrite "ɑ i" as "a ɪ" (PRICE)
* rewrite "ɔ" as "ɒ" (CLOTH/THOUGHT)
* rewrite "ɔ ə" and "oː" as "ɔː" (NORTH/FORCE)
"""

from typing import List


SOURCE = "../tsv/eng_uk_phonemic.tsv"
PAIRS = [
    ("ɛ ə", "ɛː"),
    ("a ɹ", "æ ɹ"),
    ("ɪ i", "iː"),
    ("ɪ ə", "ɪː"),
    ("ɑ i", "a ɪ"),
    ("ɔ", "ɒ"),
    ("ɔ ə", "ɔː"),
    ("oː", "ɔː"),
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
