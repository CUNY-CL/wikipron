Whitelists
==========

A whitelist is a list of phonemes (or phones, for `_phonetic.tsv` files); any
pronunciation which is not totally composed of whitelist phonemes (resp. phones)
will be filtered as a postprocessing step.

What they filter
----------------

There are several types of segments which should be filtered by a whitelist:

-   Typos
-   Invalid IPA transcriptions (e.g., extra length indicated with /ːː/)
-   non-native segments (e.g., a transcription of *Bach* as ending in the
    voiceless velar fricative /x/)

Finally, for phonemic lists, there may be segments that are properly considered
pure allophones but appear in phonemic transcriptions. However, such segments
may be quite frequent in the data and removing all pronunciations that contain
them would greatly reduce the amount of available data. Therefore, we prefer to
simply add a comment of the form `# Allophone of ...`; such annotations will
ultimately be used improve Wiktionary itself.

Wiktionary has [transcription
guidelines](https://en.wiktionary.org/wiki/Appendix:English_pronunciation) for
many languages, which you can reference when building a whitelist; you can also
refer to the [Phoible](https://phoible.org/) inventories, but these often line
up poorly with the language-specific Wiktionary transcription guidelines.

How to submit a whitelist
-------------------------

We welcome user submissions for whitelists from linguists. Note that we use the
[fork and pull](../../../CONTRIBUTING.md) model for contributions.

1.  Make a list of all phones or phonemes, in descending-frequency order, using
    the appropriate file in [`../tsv`](../tsv).
2.  Remove typos, invalid IPA transcriptions, and non-native segments.
3.  For phonemic whitelists, add comments about allophony.
4.  In [`../src/`](../src) run `./postprocess && ./generate_summary.py`.
5.  Add the whitelist, the filtered `.tsv` file(s), and the summary files using
    `git add`.
6.  Commit using `git commit`, push to your branch using `git push`, and then
    file a pull request.

The whitelist format is a UTF-8 encoded file with one segment per line, with
optional comments formatted as two spaces, `#`, one space, and then a sentence
or sentence fragment with appropriate punctuation (e.g.,
`tʰ  # Allophone of /t/.`). Please do not leave any trailing whitespace. The
whitelist file should have the same name as the corresponding TSV file, but with
a `.whitelist` extension instead of `.tsv`.
