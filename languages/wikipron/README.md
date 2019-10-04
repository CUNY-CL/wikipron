## Introduction to Python scripts within /src

[scrape_and_write.py](./src/scrape_and_write.py) was built to call Wikipron’s scrape method on all Wiktionary languages with over 100 entries. It writes the results of those scrape calls to tsvs and generates a [README](./tsv/README.md) with selected information regarding the contents of those tsvs and the configuration settings that were passed to scrape.
[languages.json](./src/languages.json) provides [scrape_and_write.py](./src/scrape_and_write.py) with a dictionary containing the information it needs to call scrape on all Wiktionary languages with over 100 entries as well as to generate the previously mentioned [README](./tsv/README.md). [codes.py](./src/codes.py) is used to generate [languages.json](./src/languages.json). It queries Wiktionary for all languages with over 100 entries. It also outputs [failed_langauges.json](./src/failed_languages.json), a list of languages on Wiktionary that have over 100 entries but that could not be matched with an ISO 639 language code.

## Steps used to update the dataset
1. Run [codes.py](./src/codes.py) to update [languages.json](./src/languages.json)
    - If there are new Wiktionary languages with over 100 entries, they will be added to [languages.json](./src/languages.json). 
    - As mentioned in the comment at the top of [codes.py](./src/codes.py), any new languages added to [languages.json](./src/languages.json) will not have their case-folding settings specified. Their `"casefold"` value will therefore be set to `None` and after exporting to json will look like: 
        ```
        "hun": {
          "iso639_name": "Hungarian",
          "wiktionary_name": "Hungarian",
          "wiktionary_code": "hu",
          "casefold": null,
          "total_pages": 45292
        }
        ```
    - Whether or not to apply case-folding for these new languages needs to be manually set by changing the “casefold” value within [languages.json](./src/languages.json).
    - To find new languages running `git diff languages.json` is not recommended, as it is likely that the `“total_pages”` value will have updated for every language already in [languages.json](./src/languages.json). Instead just search for `null` values within [languages.json](./src/languages.json).
2. Run [scrape_and_write.py](./src/scrape_and_write.py)