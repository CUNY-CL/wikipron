# "Big scrape" scripts

[`scrape`](../scrape) calls WikiPron's scraping functions on all Wiktionary
languages with over 100 entries. If a `.phones` file is present for a given
language, the process will generate an additional filtered file only containing
the permitted phones/phonemes.
[`generate_tsv_summary.py`](generate_tsv_summary.py) generates a
[README](../README.md) and a [TSV](../tsv_summary.tsv) with selected information
regarding the contents of the TSVs [`scrape.py`](scrape.py) generated and the
configuration settings that were passed to scrape.
[`postprocess`](../postprocess) sorts and removes entries in each TSV if they
have the same graphemic form and narrow/broad form as a previous entry. In
addition it splits TSVs containing multiple scripts (Arabic, Cyrillic, etc.)
into constituent TSVs containing a single script.
[`languages.json`](languages.json) provides [`scrape.py`](../scrape.py) with a
dictionary containing the information it needs to call scrape on all Wiktionary
languages with over 100 entries and is also used to generate the previously
mentioned [README](../README.md). [`codes.py`](codes.py) is used to generate
[`languages.json`](languages.json). It queries Wiktionary for all languages with
over 100 entries. It also outputs
[`unmatched_languages.json`](unmatched_languages.json), a list of languages on
Wiktionary that have over 100 entries but that could not be matched with an ISO
639 language code.

## Steps used to update the dataset

1.  Run [`codes.py`](codes.py) to update [`languages.json`](languages.json).
    -   If there are new Wiktionary languages with over 100 entries, they will
        be added to [`languages.json`](languages.json).
    -   To find new languages you can run `git diff languages.json` or search
        for `null` values within [`languages.json`](languages.json).
2.  Run [`scrape`](../scrape).
    -   For the annual big scrape, apply the `--fresh` flag when you run
        `scrape.py` the first time for the year. If the run dies out in the
        middle (or if you abort the execution, intentionally or otherwise),
        `unscraped.json` records which languages have not been scraped, and you
        can run `scrape.py` again *without* the `--fresh` flag to scrape only
        the remaining languages.
    -   By default `cut_off_date` in `main()` is set using
        `datetime.date.today().isoformat()` but can be set manually using an ISO
        formatted string (ex. "2019-10-31").
3.  Run [`postprocess`](../postprocess).

## Running a subset of languages using the big scrape

The following steps can be used to run the big scrape procedure for a subset:

1.  Run [`scrape`](../scrape) with `--restriction` flag, followed by command
    line arguments for desired languages. Note: languages must be in their ISO
    designation and argument string must delineate with comma, semicolon, or
    space. E.g. To target only Lithuanian and Spanish:
    `./scrape.py --restriction='lit; spa'`. To target all but one or more
    specific languages, apply the `--exclude` flag, e.g., to exclude Lithuanian
    and Spanish: `./scrape --exclude='lit; spa'`. Only one, but not both, of
    `--restriction` and `--exclude` can be applied.
2.  If `cut_off_date` was set in [`scrape`](../scrape) using
    `datetime.date.today().isoformat()` and it is important that all the data
    you scrape is from before the same date, then manually set `cut_off_date` in
    `main()` (using an ISO formatted string) to the date of the original big
    scrape run - which can be found in the messages logged to the console or in
    `scraping.log`.
3.  Run [`postprocess`](../postprocess).
