Frequencies scripts
===================

The scripts in this directory are responsible for downloading
word frequency counts from the
[Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download/)
and merging those counts into [our corresponding TSVs](../tsv/).
[grab\_wortschatz\_data.py](grab_wortschatz_data.py) downloads
and unpacks the TARs provided by the aforementioned Corpora Collection.
[merge.py](merge.py) merges in the word frequency counts with
our TSVs such that, for the languages covered by the Corpora Collection,
we end up with three column TSVs:

```
bashkë	b a ʃ k ə	1005
bashkëfajtor	b a ʃ k f a j t ɔ ɹ	2
bashkëfajtor	b a ʃ k ə f a j t ɔ ɹ	2
bashkëjetesë	b a ʃ k ə j ɛ t ɛ s ə	9
```

We generally choose to download the largest available News corpus
for each language, though in some cases other sources are used.
[wortschatz\_languages.json](wortschatz_languages.json) contains
a dictionary of all the languages for which we download frequencies.
The `"data_url"` key for each language links to the particular
corpus we download.