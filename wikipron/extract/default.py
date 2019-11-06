"""Default word and pron extraction."""

import itertools

from wikipron.extract.core import yield_pron


IPA_XPATH = '//span[@class = "IPA"]'


def _yield_phn(request, config):
    for li in request.html.xpath(config.li_selector):
        yield from yield_pron(li, IPA_XPATH, config)


def extract_word_pron_default(word, request, config):
    words = itertools.repeat(config.casefold(word))
    prons = _yield_phn(request, config)
    yield from zip(words, prons)
