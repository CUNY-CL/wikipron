"""Word and pron extraction for Khmer."""

import itertools

from wikipron.extract.default import yield_pron


_IPA_XPATH = '//span[@class = "IPA" and @lang = "km"]'


def extract_word_pron_khm(word, request, config):
    # TODO: Document (and test?) what the function signature must look like.
    words = itertools.repeat(config.casefold(word))
    prons = yield_pron(request.html, _IPA_XPATH, config)
    yield from zip(words, prons)
