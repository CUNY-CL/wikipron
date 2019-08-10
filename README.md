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
As a basic example, the following command scrapes G2P data for French
(with the ISO language code `fr`):

```bash
wikipron fr
```

By default, the results appear on the terminal,
where each line has the orthography of a word, followed by a tab and then
the word's pronunciation in IPA.

For example commands using advanced options,
the [`languages/scrape`](languages/scrape) script shows
how a multilingual G2P dataset can be created.

For a full list of command-line options, please run `wikipron -h`.

The underlying module can also be used from Python. A standard workflow looks lie:

```python
import wikipron

config = wikipron.Config("fr")  # French, with default options.
for word, pron in wikipron.scrape(config):
    ...
```

## Development and Contribution

For questions, bug reports, and feature requests,
please [file an issue](https://github.com/kylebgorman/wikipron/issues).

If you would like to contribute to the `wikipron` codebase,
please see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Apache 2.0. Please see [`LICENSE.txt`](LICENSE.txt) for details.
