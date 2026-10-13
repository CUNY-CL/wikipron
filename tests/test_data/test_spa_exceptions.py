import os
import tempfile

import pytest

from data.scrape.lib import spa_exceptions, spa_rules


@pytest.mark.parametrize(
    "word, pron, dialect",
    [
        ("gente", "ˈx e n t e", "ca"),
        ("banco", "ˈb a n k o", "ca"),
        ("cuidado", "k w i ˈd a d o", "ca"),
        ("prueba", "ˈp ɾ w e b a", "ca"),
        ("ruido", "ˈr w i d o", "ca"),
        ("hielo", "ˈʝ e l o", "ca"),
        ("huevo", "ˈw̝ e b o", "ca"),
        ("pingüino", "p i n ˈɡ w i n o", "ca"),
        ("cuál", "k w a l", "ca"),
        ("llave", "ˈʎ a b e", "ca"),
        ("llave", "ˈʝ a b e", "ca"),
        ("caza", "ˈk a θ a", "ca"),
        ("caza", "ˈk a s a", "la"),
        ("acto", "ˈa ɡ t o", "ca"),
        ("inmenso", "i m ˈm e n s o", "ca"),
        ("examen", "e ɡ ˈs a m e n", "ca"),
        ("psicología", "s i k o l o ˈx i a", "ca"),
        ("piscina", "p i ˈs i n a", "la"),
        ("ADN", "a d e ˈe n e", "ca"),
        ("cantar", "k a n t a ɾ", "ca"),
    ],
)
def test_regular(word, pron, dialect):
    assert spa_rules.is_regular(word, pron, dialect)


@pytest.mark.parametrize(
    "word, pron, dialect",
    [
        ("México", "ˈm e x i k o", "ca"),
        ("pizza", "ˈp i t s a", "ca"),
        ("show", "ˈʃ o u", "ca"),
        ("parking", "ˈp a ɾ k i n", "ca"),
        ("jazz", "ˈʝ a s", "la"),
        ("hardware", "ˈx a ɾ d w̝ e ɾ", "ca"),
        ("Kalahari", "k a l a ˈx a ɾ i", "la"),
        ("caza", "ˈk a s a", "ca"),
        # Stress against the spelling.
        ("cantar", "ˈk a n t a ɾ", "ca"),
    ],
)
def test_irregular(word, pron, dialect):
    assert not spa_rules.is_regular(word, pron, dialect)


@pytest.mark.parametrize(
    "pron, expected",
    [
        ("ˈp a ɾ k i n", "párkin"),
        ("ˈʃ o u", "ʃóu"),
        ("ˈp i t s a", "pítsa"),
        ("ˈm e x i k o", "méjiko"),
        ("ˈɡ w i s k i", "gwíski"),
        ("k ɾ w a ˈs a n", "kruasán"),
        ("ˈx a ɾ d w̝ e ɾ", "járduer"),
        ("ˈr o k", "rók"),
        ("ˈɾ o k", None),
        ("ˈf ə n", None),
    ],
)
def test_respell(pron, expected):
    respelling = spa_exceptions.respell(pron)
    assert respelling == expected
    if respelling:
        assert spa_rules.is_regular(respelling, pron, "ca")


def _write(path, rows):
    with open(path, "w", encoding="utf-8") as sink:
        for word, pron in rows:
            print(f"{word}\t{pron}", file=sink)


def _read(path):
    with open(path, encoding="utf-8") as source:
        return [line.rstrip("\n").split("\t") for line in source]


def test_apply():
    with tempfile.TemporaryDirectory() as tmp:
        tsv_dir = os.path.join(tmp, "tsv")
        raw_dir = os.path.join(tmp, "spa_raw")
        kokoro_path = os.path.join(tmp, "kokoro", "es_loanwords.tsv")
        os.makedirs(tsv_dir)
        os.makedirs(raw_dir)
        broad = [
            ("gato", "ɡ a t o"),
            ("pizza", "p i θ a"),
            ("pizza", "p i t s a"),
        ]
        stressed = [
            ("gato", "ˈɡ a t o"),
            ("pizza", "ˈp i θ a"),
            ("pizza", "ˈp i t s a"),
        ]
        for dialect in spa_rules.DIALECTS:
            _write(os.path.join(tsv_dir, f"spa_{dialect}_broad.tsv"), broad)
            _write(
                spa_exceptions.raw_path(raw_dir, dialect, "broad_stressed"),
                stressed,
            )
        spa_exceptions.apply(tsv_dir, raw_dir, kokoro_path)
        # Every pronunciation of an exceptional word is kept.
        assert _read(os.path.join(tsv_dir, "spa_ca_broad.tsv")) == [
            ["pizza", "p i θ a"],
            ["pizza", "p i t s a"],
        ]
        # The unfiltered scrape is moved aside.
        assert _read(spa_exceptions.raw_path(raw_dir, "ca", "broad")) == [
            list(row) for row in broad
        ]
        with open(kokoro_path, encoding="utf-8") as source:
            entries = [line for line in source if not line.startswith("#")]
        # The first pronunciation that has an exceptional respelling.
        assert entries == ["pizza\tpíza\n"]
        # Re-running from spa_raw/ gives the same result.
        spa_exceptions.apply(tsv_dir, raw_dir, kokoro_path)
        assert len(_read(os.path.join(tsv_dir, "spa_la_broad.tsv"))) == 2
