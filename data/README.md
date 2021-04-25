Data directories
================

- The [scrape](./scrape) directory contains our "Big Scrape" scripts, the
  [TSVs](./scrape/tsv) created by those scripts, and two tables (a
  [README](./scrape/README.md) and a [TSV](./scrape/tsv_summary.tsv)) describing
  those TSVs.
  - More information on the "Big Scrape" scripts, including instructions on how
    to run your own scrape, can be found [here](./scrape/lib/README.md).
- The [phones](./phones) directory contains the [`.phones`](./phones/phones)
  files used to filter the TSVs produced by the "Big Scrape", scripts that
  facilitate the creation of `.phones` files, and two tables (a
  [README](./phones/README.md) and a [TSV](./phones/phones_summary.tsv))
  describing those `.phones` files.
  - More information on the files within the [phones](./phones) directory,
    including instructions on how to create your own `.phones` file, can be
    found [here](./phones/HOWTO.md).
- The [frequencies](./frequencies) directory contains scripts used to merge word
  frequencies into the TSVs produced by the "Big Scrape".
  - Details on the specific function of each script and how we acquire the
    frequencies can be found [here](./frequencies/README.md).
- The [morphology](./morphology) directory contains scripts that download
  UniMorph data for all languages covered by both UniMorph and the "Big Scrape".
  - Details can be found [here](./morphology/README.md)