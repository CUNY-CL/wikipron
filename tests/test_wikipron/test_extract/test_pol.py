"""Tests for the Polish extractor.

Modeled on the live Wiktionary page for Polish "trzeba" (2026-11-24).
A modern line, then a "(Middle Polish)" line with two qualified prons.
On the live page the 17th-18th c. pron is /ˈtʂɛ.ba/, the same as the modern
one. Here it is /ˈtʂɛ.bɒ/ so that skipping it is observable. Then two synthetic
nesting cases: a modern line with a nested Middle Polish sub-line, and a
Middle Polish header line with a nested sub-line.
"""

from wikipron.extract.default import extract_word_pron_default
from wikipron.extract.pol import extract_word_pron_polish

from .. import _offline_response, config_factory

_POLISH_IPA_KEY = (
    '<a href="/wiki/Wiktionary:International_Phonetic_Alphabet" '
    'title="Wiktionary:International Phonetic Alphabet">IPA</a>'
    '<sup>(<a href="/wiki/Appendix:Polish_pronunciation" '
    'title="Appendix:Polish pronunciation">key</a>)</sup>: '
)
_MIDDLE_POLISH_ACCENT_LABEL = (
    '<span class="usage-label-accent">'
    '<span class="ib-brac label-brac">(</span>'
    '<span class="ib-content label-content">'
    '<a href="https://en.wikipedia.org/wiki/Middle_Polish" class="extiw" '
    'title="w:Middle Polish">Middle Polish</a></span>'
    '<span class="ib-brac label-brac">)</span></span> '
)
_POLISH_MIDDLE_POLISH_HTML = f"""
<ul>
  <li>{_POLISH_IPA_KEY}<span class="IPA nowrap">/ˈtʂɛ.ba/</span></li>
  <li>{_MIDDLE_POLISH_ACCENT_LABEL}{_POLISH_IPA_KEY}
    <span class="ib-brac qualifier-brac">(</span><span
      class="ib-content qualifier-content"><span
      class="usage-label-accent">16<sup>th</sup> c.</span></span><span
      class="ib-brac qualifier-brac">)</span>
    <span class="IPA nowrap">/ˈtr̝ɛ.ba/</span>,
    <span class="ib-brac qualifier-brac">(</span><span
      class="ib-content qualifier-content"><span
      class="usage-label-accent">17<sup>th</sup>–18<sup>th</sup> c.</span>
      </span><span class="ib-brac qualifier-brac">)</span>
    <span class="IPA nowrap">/ˈtʂɛ.bɒ/</span>
  </li>
  <li>{_POLISH_IPA_KEY}<span class="IPA nowrap">/ˈtʂɛ.bɘ/</span>
    <ul>
      <li>{_MIDDLE_POLISH_ACCENT_LABEL}{_POLISH_IPA_KEY}<span
        class="IPA nowrap">/ˈtʂɛ.bɨ/</span></li>
    </ul>
  </li>
  <li>{_MIDDLE_POLISH_ACCENT_LABEL}{_POLISH_IPA_KEY}<span
    class="IPA nowrap">/ˈtʂe.ba/</span>
    <ul>
      <li>{_POLISH_IPA_KEY}<span class="IPA nowrap">/ˈtʂe.bɒ/</span></li>
    </ul>
  </li>
</ul>
"""


def test_polish_skips_middle_polish():
    config = config_factory(key="pol", stress=False, syllable_boundaries=False)
    response = _offline_response(_POLISH_MIDDLE_POLISH_HTML)
    prons = [
        pron
        for _, pron in extract_word_pron_polish("trzeba", response, config)
    ]
    # Kept: the modern line, and a modern line whose nested sub-line is
    # Middle Polish. Skipped: Middle Polish lines (both qualified prons) and
    # a sub-line under a Middle Polish line.
    assert prons == ["t ʂ ɛ b a", "t ʂ ɛ b ɘ"]
    # The default extractor keeps everything, which is the bug being fixed.
    default_prons = [
        pron
        for _, pron in extract_word_pron_default("trzeba", response, config)
    ]
    assert default_prons == [
        "t ʂ ɛ b a",
        "t r̝ ɛ b a",
        "t ʂ ɛ b ɒ",
        "t ʂ ɛ b ɘ",
        "t ʂ ɛ b ɨ",
        "t ʂ e b a",
        "t ʂ e b ɒ",
    ]
