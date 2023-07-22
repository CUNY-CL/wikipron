# WikiPron

[![PyPI
version](https://badge.fury.io/py/wikipron.svg)](https://pypi.org/project/wikipron)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/wikipron.svg)](https://pypi.org/project/wikipron)
[![CircleCI](https://circleci.com/gh/CUNY-CL/wikipron/tree/master.svg?style=shield)](https://circleci.com/gh/CUNY-CL/wikipron/tree/master)
[![Paper](http://img.shields.io/badge/paper-ACL:2020.lrec--1.521-B31B1B.svg)](https://www.aclweb.org/anthology/2020.lrec-1.521/)
[![Conference](http://img.shields.io/badge/LREC-2020-4b44ce.svg)](https://lrec2020.lrec-conf.org/en/)

WikiPron is a command-line tool and Python API for mining multilingual
pronunciation data from Wiktionary, as well as a database of pronunciation
dictionaries mined using this tool.

-   [Command-line tool](#command-line-tool)
-   [Python API](#python-api)
-   [Data](#data)
-   [Models](#models)
-   [Development](#development)

If you use WikiPron in your research, please cite the following:

Jackson L. Lee, Lucas F.E. Ashby, M. Elizabeth Garza, Yeonju Lee-Sikka, Sean
Miller, Alan Wong, Arya D. McCarthy, and Kyle Gorman (2020). [Massively
multilingual pronunciation mining with
WikiPron](https://www.aclweb.org/anthology/2020.lrec-1.521/). In *Proceedings of
the 12th Language Resources and Evaluation Conference*, pages 4223-4228.
\[[bibtex](https://www.aclweb.org/anthology/2020.lrec-1.521.bib)\]

## Command-line tool

### Installation

```bash
pip install wikipron
```

### Usage

#### Quick start

After installation, the terminal command `wikipron` will be available. As a
basic example, the following command scrapes G2P data for French:

```bash
wikipron fra
```

#### Specifying the language

The language is indicated by a three-letter [ISO
639-3](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes) language code,
e.g., `fra` for French. For which languages can be scraped,
[here](https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language)
is the complete list of languages on Wiktionary that have pronunciation entries.

#### Specifying the dialect

One can optionally specify dialects to target using the `--dialect` flag. The
dialect name can be found together with the transcription on Wiktionary. For
example, "(UK, US) IPA: /təˈmɑːtəʊ/". To restrict to the union of dialects use
the pipe character '\|': e.g., `--dialect='General American | US'`.
Transcriptions which lack a dialect specification are selected regardless of the
value of this flag.

#### Specifying the transcription level

By default, WikiPron selects broad pronunciations in angled brackets /like
this/. One can instead select narrow transcriptions written \[like this\] using
the `--narrow` flag. Note that some languages only have broad or narrow
transcriptions (e.g., Russian only has the latter.

#### Segmentation

By default, the [`segments`](https://github.com/cldf/segments) library is used
to segment the transcription into whitespace. The segmentation tends to place
IPA diacritics and modifiers on the "parent" symbol. For instance, \[kʰæt\] is
rendered `kʰ æ t`. This can be disabled using the `--no-segment` flag.

#### Parentheses

Some of transcriptions contain parentheses to indicate alternative
pronunciations. The parentheses (but not the content) are discarded in the
scrape unless the `--no-skip-parens` flag is used.

#### Output

The scraped data is organized with each \<word, pronunciation\> pair on its own
line, where the word and pronunciation are separated by a tab. Note that the
pronunciation is in [International Phonetic Alphabet
(IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet), segmented
by spaces that correctly handle the combining and modifier diacritics for
modeling purposes, e.g., we have `kʰ æ t` with the aspirated k instead of
`k ʰ æ t`.

For illustration, here is a snippet of French data scraped by WikiPron:

```tsv
accrémentitielle    a k ʁ e m ɑ̃ t i t j ɛ l
accrescent  a k ʁ ɛ s ɑ̃
accrétion   a k ʁ e s j ɔ̃
accrétions  a k ʁ e s j ɔ̃
```

By default, the scraped data appears in the terminal. To save the data in a TSV
file, please redirect the standard output to a filename of your choice:

```bash
wikipron fra > fra.tsv
```

#### Advanced options

The `wikipron` terminal command has an array of options to configure your
scraping run. For a full list of the options, please run `wikipron -h`.

## Python API

The underlying module can also be used from Python. A standard workflow looks
like:

```python
import wikipron

config = wikipron.Config(key="fra")  # French, with default options.
for word, pron in wikipron.scrape(config):
    ...
```

## Data

We also make available [a database of over 3 million word/pronunciation
pairs](https://github.com/CUNY-CL/wikipron/tree/master/data) mined using
WikiPron.

## Models

We host grapheme-to-phoneme models and modeling software [in a separate
repository](https://github.com/kylebgorman/wikipron-modeling).

## Development

### Repository

The source code of WikiPron is hosted on GitHub at
[`https://github.com/CUNY-CL/wikipron`](https://github.com/CUNY-CL/wikipron),
where development also happens.

For the latest changes not yet released through `pip` or working on the codebase
yourself, you may obtain the latest source code through GitHub and `git`:

1.  Create a fork of the `wikipron` repo on your GitHub account.

2.  Locally, make sure you are in some sort of a virtual environment (venv,
    virtualenv, conda, etc).

3.  Download and install the library in the "editable" mode together with the
    core and dev dependencies within the virtual environment:

    ```bash
    git clone https://github.com/<your-github-username>/wikipron.git
    cd wikipron
    pip install -U pip setuptools
    pip install -r requirements.txt
    pip install --no-deps -e .
    ```

We keep track of notable changes in
[`CHANGELOG.md`](https://github.com/CUNY-CL/wikipron/blob/master/CHANGELOG.md).

### Contributing

For questions, bug reports, and feature requests, please [file an
issue](https://github.com/CUNY-CL/wikipron/issues).

If you would like to contribute to the `wikipron` codebase, please see
[CONTRIBUTING.md](https://github.com/CUNY-CL/wikipron/blob/master/CONTRIBUTING.md).

### License

WikiPron is released under an Apache 2.0 license. Please see
[LICENSE.txt](https://github.com/CUNY-CL/wikipron/blob/master/LICENSE.txt) for
details.

Please note that Wiktionary data in the
[`data/`](https://github.com/CUNY-CL/wikipron/tree/master/data) directory has
[its own licensing terms](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).
