"Big scrape" scripts
====================

[scrape.py](scrape.py) calls WikiPron's scraping functions on all
Wiktionary languages with over 100 entries.
[generate\_summary.py](generate_summary.py) generates a [README](../README.md)
and a [TSV](../languages_summary.tsv) with selected
information regarding the contents of the TSVs [scrape.py](scrape.py)
generated and the configuration settings
that were passed to scrape. [remove\_duplicates.sh](remove_duplicates.sh)
sorts and removes entries in each TSV if they have 
the same graphemic form and phonemic form as a previous entry.
 [languages.json](languages.json) provides
[scrape.py](scrape.py) with a dictionary containing the information it
needs to call scrape on all Wiktionary languages with over 100 entries 
and is also used to generate the previously mentioned [README](../README.md).
[codes.py](codes.py) is used to generate
[languages.json](languages.json). It queries Wiktionary for all languages
with over 100 entries. It also outputs
[unmatched\_languages.json](unmatched_languages.json), a list of languages on
Wiktionary that have over 100 entries but that could not be matched with an ISO
639 language code.

Steps used to update the dataset
--------------------------------

1.  Run [codes.py](codes.py) to update
    [languages.json](languages.json).
    -   If there are new Wiktionary languages with over 100 entries, they will
        be added to [languages.json](languages.json).
    -   As mentioned in the comment at the top of [codes.py](codes.py),
        any new languages added to [languages.json](languages.json) will
        not have their case-folding settings specified. 
        Their `"casefold"` value will therefore be set to `None`.
    -   Whether or not to apply case-folding for these new languages needs
        to be manually set by changing the "casefold" value within
        [languages.json](languages.json).
    -   To find new languages you can run`git diff languages.json` 
        or search for `null` values within 
        [languages.json](languages.json).
2.  Run [scrape.py](scrape.py).
    -   By default `cut_off_date` in `main()` is set using
        `datetime.date.today().isoformat()` but can be set manually 
        using an ISO formatted string (ex. "2019-10-31").
3.  Run [serbo\_croat\_split.py](serbo_croat_split.py).
4.  Run [remove\_duplicates.sh](remove_duplicates.sh).
5.  Run [generate\_summary.py](generate_summary.py).

Running a subset of languages using the big scrape
--------------------------------------------------

By default, if [scrape.py](scrape.py) cannot successfully complete a scrape
of an entire language in 10 retries, it will log the language,
remove the incomplete data scraped from that language, 
and move on to the next language in [languages.json](languages.json). 
There may therefore be a few languages that you need to run again when 
the big scrape finishes. These are the steps to follow should you need
 to run the big scrape scripts for a smaller set of languages:

1.  Modify [languages.json](languages.json) so it only contains
    the languages you want to scrape.
2.  If `cut_off_date` in [scrape.py](scrape.py) was set using 
    `datetime.date.today().isoformat()` and it is important that all
    the data you scrape is from before the same date,
    then manually set `cut_off_date` in `main()` (using an ISO formatted
    string) to the date of the original big scrape run - which can be
    found in the messages logged to the console or in `scraping.log`.
3.  Run [scrape.py](scrape.py).
4.  If you have not already done so,
    run [serbo\_croat\_split.py](serbo_croat_split.py)
5.  Run [remove\_duplicates.sh](remove_duplicates.sh).
6.  Reset [languages.json](languages.json) to its unmodified state.
    (Using `git checkout` or `git reset`)
7.  Run [generate\_summary.py](generate_summary.py).

Steps 1-3 can be repeated until you have successfully scraped all languages.
