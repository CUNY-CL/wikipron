"Big scrape" scripts
====================

[scrape.py](./src/scrape.py) calls WikiPron's scraping functions on all
Wiktionary languages with over 100 entries. [generate_summary.py](./src/generate_summary.py)
generates a [README](./tsv/README.md) and a [TSV](languages_summary.tsv) with selected
information regarding the contents of the TSVs [scrape.py](./src/scrape.py)
generated and the configuration settings
that were passed to scrape. [languages.json](./src/languages.json) provides
[scrape.py](./src/scrape.py) with a dictionary containing the information it
needs to call scrape on all Wiktionary languages with over 100 entries as well
as to generate the previously mentioned [README](./tsv/README.md).
[codes.py](./src/codes.py) is used to generate
[languages.json](./src/languages.json). It queries Wiktionary for all languages
with over 100 entries. It also outputs
[unmatched\_langauges.json](./src/unmatched_languages.json), a list of languages on
Wiktionary that have over 100 entries but that could not be matched with an ISO
639 language code.

Steps used to update the dataset
--------------------------------

1.  Run [codes.py](./src/codes.py) to update
    [languages.json](./src/languages.json).
    -   If there are new Wiktionary languages with over 100 entries, they will
        be added to [languages.json](./src/languages.json).
    -   As mentioned in the comment at the top of [codes.py](./src/codes.py),
        any new languages added to [languages.json](./src/languages.json) will
        not have their case-folding settings specified. Their `"casefold"` value
        will therefore be set to `None`.
    -   Whether or not to apply case-folding for these new languages needs to be
        manually set by changing the "casefold" value within
        [languages.json](./src/languages.json).
    -   To find new languages you can run`git diff languages.json` 
        or search for `null` values within 
        [languages.json](./src/languages.json).
2.  Run [scrape.py](./src/scrape.py).
3.  Run [generate_summary.py](./src/generate_summary.py).