"""Regular Spanish spelling-to-pronunciation rules.

A Python port of the letter rules in kokoro.cpp's ``SpanishG2P.cpp``, used to
tell apart words whose Wiktionary pronunciation is predictable from their
spelling from those that are pronounced exceptionally (mostly loanwords such
as "pizza" /ˈpitsa/ or "show" /ˈʃou/, or irregular spellings such as
"México" /ˈmexiko/).

Rules are compared on WikiPron's broad transcription after normalizing away
differences that are not exceptional: allophones (β ð ɣ), nasal place
assimilation, glide vs. vowel (j/i, w/u), yeísmo (ʎ/ʝ), and the hi-/hu-
onsets transcribed as ʝ and w̝. A few espeak-specific quirks of
``SpanishG2P.cpp`` (hiatus after trill r and ʎ, ü always in hiatus, open ɛ)
are not ported, as Wiktionary does not follow them.
"""

import unicodedata

from collections.abc import Iterable

DIALECTS = ("ca", "la")

_VOWEL_LETTERS = frozenset("aeiouáéíóúü")
_FRONT = frozenset("eiéí")
_ACCENTED = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
_VOWELS = frozenset("aeiou")
_UNSTRESSED = frozenset(
    "a al con de del e el en la las le les lo los me mi mis ni nos o os por "
    "que se si sin su sus te tu tus u y".split()
)
_LETTER_NAMES = {
    "a": "a",
    "b": "be",
    "c": "ce",
    "d": "de",
    "e": "e",
    "f": "efe",
    "g": "ge",
    "h": "hache",
    "i": "i",
    "j": "jota",
    "k": "ka",
    "l": "ele",
    "m": "eme",
    "n": "ene",
    "ñ": "eñe",
    "o": "o",
    "p": "pe",
    "q": "cu",
    "r": "erre",
    "s": "ese",
    "t": "te",
    "u": "u",
    "v": "uve",
    "w": "uvedoble",
    "x": "equis",
    "y": "igriega",
    "z": "zeta",
}

# Broad phones that are not exceptional when swapped for one another.
_NORMALIZE = {
    "β": "b",
    "ð": "d",
    "ɣ": "ɡ",
    "g": "ɡ",
    "ɛ": "e",
    "ɪ": "i",
    "ʊ": "u",
    "j": "i",
    "i̯": "i",
    "u̯": "u",
    "w": "u",
    "w̝": "u",
    "ʎ": "ʝ",
    "ɟ͡ʝ": "ʝ",
    "ɲ": "ɲ",
    "ŋ": "n",
    "ɱ": "n",
    "ʧ": "t͡ʃ",
    "tʃ": "t͡ʃ",
    "ç": "x",
    "h": "x",
}

# Word-initial clusters whose first consonant is usually silent: "psicología",
# "gnomo", "ctónico", "mnemotecnia", "pterodáctilo".
_SILENT_INITIAL = frozenset(("ps", "gn", "ct", "mn", "pn", "pt"))
_CODA_STOPS = {"p": "b", "t": "d", "k": "ɡ"}

# A predicted pronunciation: phones and the index of the stressed vowel
# (None when unknown or not applicable).
Prediction = tuple[tuple[str, ...], int | None]


class _Unit:
    __slots__ = ("ipa", "vowel", "accented", "weak")

    def __init__(
        self,
        ipa: str,
        vowel: bool = False,
        accented: bool = False,
        weak: bool = False,
    ) -> None:
        self.ipa = ipa
        self.vowel = vowel
        self.accented = accented
        self.weak = weak


def _vowel(c: str) -> _Unit:
    if c in _ACCENTED:
        return _Unit(_ACCENTED[c], vowel=True, accented=True)
    if c == "ü":
        return _Unit("u", vowel=True, weak=True)
    return _Unit(c, vowel=True, weak=c in "iu")


def _units(word: str, dialect: str, keep_cluster: bool) -> list[_Unit]:
    """Maps the letters of a lowercased word to phonetic units."""
    sibilant = "θ" if dialect == "ca" else "s"
    units: list[_Unit] = []
    i = 0
    if not keep_cluster and word[:2] in _SILENT_INITIAL:
        i = 1
    while i < len(word):
        c = word[i]
        nxt = word[i + 1] if i + 1 < len(word) else ""
        after = word[i + 2] if i + 2 < len(word) else ""
        at = i
        i += 1
        if c in _VOWEL_LETTERS:
            units.append(_vowel(c))
        elif c == "h":
            # Wiktionary transcribes hie-/hia- as ʝ and hue- as w̝.
            if nxt == "i" and after in _VOWEL_LETTERS:
                units.append(_Unit("ʝ"))
                i += 1
            continue
        elif c + nxt in ("ch", "ll", "rr"):
            i += 1
            units.append(_Unit({"ch": "t͡ʃ", "ll": "ʝ", "rr": "r"}[c + nxt]))
        elif c in "qg" and nxt == "u" and after in _FRONT:
            i += 1
            units.append(_Unit("k" if c == "q" else "ɡ"))
        elif c == "r":
            trill = at == 0 or word[at - 1] in "lns"
            units.append(_Unit("r" if trill else "ɾ"))
        elif c == "q":
            units.append(_Unit("k"))
        elif c == "g":
            units.append(_Unit("x" if nxt in _FRONT else "ɡ"))
        elif c == "c":
            units.append(_Unit(sibilant if nxt in _FRONT else "k"))
        elif c == "z":
            units.append(_Unit(sibilant))
        elif c == "j":
            units.append(_Unit("x"))
        elif c == "ñ":
            units.append(_Unit("ɲ"))
        elif c == "x":
            if at == 0:
                units.append(_Unit("s"))
            else:
                units.append(_Unit("k"))
                units.append(_Unit("s"))
        elif c == "v":
            units.append(_Unit("b"))
        elif c == "y":
            if nxt in _VOWEL_LETTERS:
                units.append(_Unit("ʝ"))
            else:
                units.append(_Unit("i", vowel=True, weak=True))
        else:
            units.append(_Unit(c))
    return units


def _strong(u: _Unit) -> bool:
    return not u.weak or u.accented


def _nuclei(units: list[_Unit]) -> list[tuple[int, bool]]:
    """Returns (main vowel index, accented) for each syllable nucleus."""
    nuclei = []
    begin = 0
    while begin < len(units):
        if not units[begin].vowel:
            begin += 1
            continue
        end = begin + 1
        while (
            end < len(units)
            and units[end].vowel
            and not (_strong(units[end]) and _strong(units[end - 1]))
        ):
            end += 1
        main = next(
            (i for i in range(begin, end) if _strong(units[i])), end - 1
        )
        nuclei.append((main, units[main].accented))
        begin = end
    return nuclei


def _stressed(nuclei: list[tuple[int, bool]], word: str) -> int | None:
    """Unit index of the stressed vowel, or None if not determined."""
    for main, accented in nuclei:
        if accented:
            return main
    # Monosyllables: stress is not informative and Wiktionary rarely marks it.
    if len(nuclei) < 2:
        return None
    penult = word[-1] in _VOWEL_LETTERS or word[-1] in "ns"
    return nuclei[-2][0] if penult else nuclei[-1][0]


def _render(units: list[_Unit], stressed: int | None) -> Prediction:
    phones: list[str] = []
    index = None
    for i, u in enumerate(units):
        if i == stressed:
            index = len(phones)
        phones.append(u.ipa)
    return tuple(phones), index


def _clean(word: str) -> str:
    word = unicodedata.normalize("NFC", word).lower()
    # Apostrophes, hyphens, and periods are not pronounced.
    return "".join(c for c in word if c not in "'’-.·")


def _acronym(word: str, dialect: str) -> Prediction | None:
    letters = _clean(word)
    if (
        not letters
        or (len(letters) > 1 and word != word.upper())
        or any(c not in _LETTER_NAMES for c in letters)
    ):
        return None
    spelled = "".join(_LETTER_NAMES[c] for c in letters)
    phones, _ = _render(_units(spelled, dialect, keep_cluster=True), None)
    return phones, None


def predict(word: str, dialect: str) -> set[Prediction]:
    """Returns the regular broad pronunciations of a word.

    Each prediction is a tuple of raw (unnormalized) broad phones and the
    index of the stressed vowel in it, or None when stress is not predicted.
    """
    if dialect not in DIALECTS:
        raise ValueError(f"Unknown Spanish dialect: {dialect!r}")
    cleaned = _clean(word)
    predictions: set[Prediction] = set()
    if not cleaned:
        return predictions
    for keep_cluster in (False, True):
        units = _units(cleaned, dialect, keep_cluster)
        stressed = (
            None
            if cleaned in _UNSTRESSED
            else _stressed(_nuclei(units), cleaned)
        )
        predictions.add(_render(units, stressed))
    acronym = _acronym(word, dialect)
    if acronym:
        predictions.add(acronym)
    return predictions


def _normalize(phones: Iterable[str]) -> tuple[str, ...]:
    out = [_NORMALIZE.get(p, p) for p in phones]
    for i in range(len(out) - 1):
        nxt = out[i + 1]
        if nxt in _VOWELS:
            continue
        # Nasal place assimilation: "envío" /emˈbio/, "inmenso" /imˈmenso/.
        if out[i] in ("m", "n"):
            out[i] = "m" if nxt == "m" else "n"
        # Stops neutralize voicing in the coda: "acto" /ˈaɡto/.
        elif out[i] in _CODA_STOPS:
            out[i] = _CODA_STOPS[out[i]]
        # Trill vs. tap after a prefix: "subrayar", "abrogar".
        elif out[i] in ("b", "d") and nxt == "ɾ":
            out[i + 1] = "r"
    # Seseo makes <sc> before e, i a single s: "piscina" /piˈsina/.
    return tuple(
        p
        for i, p in enumerate(out)
        if not (p == "s" and out[i - 1 : i] == ["s"])
    )


def parse_pron(pron: str) -> tuple[tuple[str, ...], frozenset[int]]:
    """Splits a segmented WikiPron pronunciation into phones and stress.

    Returns the phones without stress or syllable marks, and the indices of
    the vowels carrying primary stress. Wiktionary places ˈ at the start of a
    syllable, so the stressed vowel is the first full vowel after the mark.
    """
    phones: list[str] = []
    marks: list[int] = []
    for seg in pron.split():
        while seg and seg[0] in "ˈˌ.":
            if seg[0] == "ˈ":
                marks.append(len(phones))
            seg = seg[1:]
        if seg:
            phones.append(seg)
    stressed = set()
    for mark in marks:
        for i in range(mark, len(phones)):
            if _NORMALIZE.get(phones[i], phones[i])[:1] in _VOWELS and (
                phones[i] not in ("j", "w", "w̝", "i̯", "u̯")
            ):
                stressed.add(i)
                break
    return tuple(phones), frozenset(stressed)


def is_regular(word: str, pron: str, dialect: str) -> bool:
    """True when the pronunciation follows regular Spanish spelling rules.

    The pronunciation is a space-segmented WikiPron string; stress marks are
    optional and only compared when present on both sides.
    """
    phones, stressed = parse_pron(pron)
    normalized = _normalize(phones)
    # Stress is compared by vowel count, as normalization may drop phones.
    marked = {_vowel_ordinal(phones, i) for i in stressed}
    for predicted, index in predict(word, dialect):
        if _normalize(predicted) != normalized:
            continue
        if (
            index is None
            or not marked
            or _vowel_ordinal(predicted, index) in marked
        ):
            return True
    return False


def _vowel_ordinal(phones: tuple[str, ...], index: int) -> int:
    """Number of vowels and glides before phones[index]."""
    return sum(_NORMALIZE.get(p, p) in _VOWELS for p in phones[:index])


def irregular_words(rows: Iterable[tuple[str, str]], dialect: str) -> set[str]:
    """Words with at least one pronunciation not following the rules."""
    return {word for word, pron in rows if not is_regular(word, pron, dialect)}
