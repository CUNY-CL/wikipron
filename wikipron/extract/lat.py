import re

from wikipron.extract.default import IPA_XPATH


_WORD_XPATH = """
//ul[
  li[
    (.|span)[sup[a[@title = "Appendix:Latin pronunciation"]]]
    and
    span[@class = "IPA"]
  ]
]
/following::
p[strong[@class = "Latn headword" and @lang = "la"]]
"""


def _extract_words(request):
    words = []
    for p in request.html.xpath(_WORD_XPATH):
        for strong in p.xpath(
            '//strong[@class = "Latn headword" and @lang = "la"]'
        ):
            words.append(strong.text)
    return words


def _extract_prons(request, config):
    prons = []
    for li in request.html.xpath(config.li_selector):
        for span in li.xpath(IPA_XPATH):
            m = re.search(config.ipa_regex, span.text)
            if m:
                try:
                    prons.append(m.group(1))
                except IndexError:
                    pass
    return prons


def extract_word_pron_lat(word, request, config):
    # The headword from Wiktionary isn't used.
    word = None  # noqa: F841

    words = _extract_words(request)
    prons = _extract_prons(request, config)

    print()
    print(words, prons)

    # In case words and prons don't match up for numbers, give up.
    if len(words) != len(prons):
        return

    yield from zip(words, prons)
