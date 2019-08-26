# WikiPron

[![PyPI version](https://badge.fury.io/py/wikipron.svg)](https://pypi.org/project/wikipron)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/wikipron.svg)](https://pypi.org/project/wikipron)
[![CircleCI](https://circleci.com/gh/kylebgorman/wikipron/tree/master.svg?style=svg)](https://circleci.com/gh/kylebgorman/wikipron/tree/master)


WikiPron is a command line toolkit for scraping grapheme-to-phoneme (G2P) data
from Wiktionary.

## Installation

WikiPron requires Python 3.6+. It is available through pip:

```bash
pip install wikipron
```

## Usage

After installation, the terminal command `wikipron` will be available.
As a basic example, the following command scrapes G2P data for French:

```bash
wikipron fra
```

The language is indicated by a three-letter
[ISO 639-2](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes) or
[ISO 639-3](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes)
language code, e.g., `fra` for French.
For which languages can be scraped,
[here](https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language)
is the complete list of languages on Wiktionary that have pronunciation entries.

By default, the results appear on the terminal,
where each line has the orthography of a word, followed by a tab and then
the word's pronunciation in the
[International Phonetic Alphabet (IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet).

For example commands using advanced options, the
[languages/wikipron/scrape](https://github.com/kylebgorman/wikipron/blob/master/languages/wikipron/scrape)
script shows how a multilingual G2P dataset can be created.

For a full list of command-line options, please run `wikipron -h`.

The underlying module can also be used from Python.
A standard workflow looks like:

```python
import wikipron

config = wikipron.Config(key="fra")  # French, with default options.
for word, pron in wikipron.scrape(config):
    ...
```

## Development and Contribution

For questions, bug reports, and feature requests,
please [file an issue](https://github.com/kylebgorman/wikipron/issues).

If you would like to contribute to the `wikipron` codebase,
please see
[CONTRIBUTING.md](https://github.com/kylebgorman/wikipron/blob/master/CONTRIBUTING.md).

We keep track of notable changes in
[CHANGELOG.md](https://github.com/kylebgorman/wikipron/blob/master/CHANGELOG.md).

## License

Apache 2.0. Please see
[LICENSE.txt](https://github.com/kylebgorman/wikipron/blob/master/LICENSE.txt)
for details.

Please note that Wiktionary data has
[its own licensing terms](https://en.wiktionary.org/wiki/Wiktionary:Copyrights)
, as does the other data in the
[languages/](https://github.com/kylebgorman/wikipron/tree/master/languages)
subdirectory.
