"""Core functionality for word and pron extraction."""

import re


def yield_pron(request_html, ipa_xpath_selector, config):
    for x in request_html.xpath(ipa_xpath_selector):
        m = re.search(config.ipa_regex, x.text)
        if not m:
            continue
        pron = m.group(1)
        # Removes parens around various segments.
        pron = pron.replace("(", "").replace(")", "")
        # Skips examples with a space in the pron.
        if " " in pron:
            continue
        try:
            pron = config.process_pron(pron)
        except IndexError:
            print(pron)
            raise
        if pron:
            yield pron
