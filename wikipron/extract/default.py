import re


IPA_XPATH = '//span[@class = "IPA"]'


def _yield_phn(request, config):
    for li in request.html.xpath(config.li_selector):
        for span in li.xpath(IPA_XPATH):
            m = re.search(config.ipa_regex, span.text)
            if m:
                yield m


def extract_word_pron_default(word, request, config):
    word = config.casefold(word)
    for m in _yield_phn(request, config):
        try:
            pron = m.group(1)
        except IndexError:
            continue
        # Removes parens around various segments.
        pron = pron.replace("(", "").replace(")", "")
        # Skips examples with a space in the pron.
        if " " in pron:
            continue
        pron = config.process_pron(pron)
        if pron:
            yield (word, pron)
