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

### Quick Start

After installation, the terminal command `wikipron` will be available.
As a basic example, the following command scrapes G2P data for French:

```bash
wikipron fra
```

### Specifying the Language

The language is indicated by a three-letter
[ISO 639-2](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes) or
[ISO 639-3](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes)
language code, e.g., `fra` for French.
For which languages can be scraped,
[here](https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language)
is the complete list of languages on Wiktionary that have pronunciation entries.

### Output

The scraped data is organized with each <word, pronunciation> pair on its
own line, where the word and pronunciation are separated by a tab.
Note that the pronunciation is in
[International Phonetic Alphabet (IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet),
segmented by spaces that correctly handle the combining and modifier diacritics
for modeling purposes,
e.g., we have `kʰ æ t` with the aspirated k instead of `k ʰ æ t`.

For illustration, here is a snippet of French data scraped by WikiPron:

```tsv
accrémentitielle	a k ʁ e m ɑ̃ t i t j ɛ l
accrescent	a k ʁ ɛ s ɑ̃
accrétion	a k ʁ e s j ɔ̃
accrétions	a k ʁ e s j ɔ̃
```

By default, the scraped data appears in the terminal.
To save the data in a TSV file,
please redirect the standard output to a filename of your choice:

```bash
wikipron fra > fra.tsv
```

### Advanced Options

The `wikipron` terminal command has an array of options to configure
your scraping run.
For a full list of the options, please run `wikipron -h`.

### Python API

The underlying module can also be used from Python.
A standard workflow looks like:

```python
import wikipron

config = wikipron.Config(key="fra")  # French, with default options.
for word, pron in wikipron.scrape(config):
    ...
```

## Development

The source code of WikiPron is hosted on GitHub at
https://github.com/kylebgorman/wikipron,
where development also happens.

For the latest changes not yet released through `pip` or working on the codebase
yourself, you may obtain the latest source code through GitHub and `git`:

1. Create a fork of the `wikipron` repo on your GitHub account.
2. Locally, make sure you are in some sort of a virtual environment
   (venv, virtualenv, conda, etc).
3. Download and install the library in the "editable" mode
   together with the core and dev dependencies within the virtual environment:

    ```bash
    git clone https://github.com/<your-github-username>/wikipron.git
    cd wikipron
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
    pip install --no-deps -e .
    ```

We keep track of notable changes in
[CHANGELOG.md](https://github.com/kylebgorman/wikipron/blob/master/CHANGELOG.md).

## Contribution

For questions, bug reports, and feature requests,
please [file an issue](https://github.com/kylebgorman/wikipron/issues).

If you would like to contribute to the `wikipron` codebase,
please see
[CONTRIBUTING.md](https://github.com/kylebgorman/wikipron/blob/master/CONTRIBUTING.md).

## License

Apache 2.0. Please see
[LICENSE.txt](https://github.com/kylebgorman/wikipron/blob/master/LICENSE.txt)
for details.

Please note that Wiktionary data has
[its own licensing terms](https://en.wiktionary.org/wiki/Wiktionary:Copyrights)
, as does the other data in the
[languages/](https://github.com/kylebgorman/wikipron/tree/master/languages)
subdirectory.
