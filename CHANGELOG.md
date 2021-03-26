Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic
Versioning](http://semver.org/spec/v2.0.0.html).

Unreleased
----------

### Under `data/`

#### Added

-   Added `data/src/normalize.py`. (\#356)
-   Updated `README.md`. (\#360)
-   Added `data/cg/tsv/geo.tsv`. (\#367)
-   Added `data/morphology`. (\#369)
-   Added SIGMORPHON 2021 morphology data. (\#375)
-   Added `data/cg/tsv/jpn_hira.tsv`. (\#384)
-   Enforced final newlines. (\#387)
-   Adds all UniMorph languages to morphology. (\#393)

#### Changed

-   Added new columns in summary tables. (\#365)
-   Fixed broken paths in `data/src/generate_phones_summary.py` and in 
    `data/phones/HOWTO.md`. (\#352)
-   Added Atong (India) (`aot`). (\#353)
-   Added Egyptian Arabic (`arz`). (\#354)
-   Added Lolopo (`ycl`). (\#355)
-   Fixed Unicode normalization in `data/phones/slv_phonemic.phones` and
    re-scraped Slovenian data. (\#356)
-   Updated `data/phones/HOWTO.md` to include instructions on applying the
    NFC Unicode normalization (\#357)
-   Updated `data/src/normalize.py` to be more efficient. (\#358)
-   Fixed inaccuracies in `data/phones/geo_phonemic.phones`. (\#367)
-   Fixed typo in `data/cg/tsv/geo.tsv` and added missing character. (\#370)
-   Morphology URLs are now provided as a list. (\#376)
-   Configured and scraped Yamphu (`ybi`). (\#380)
-   Configured and scraped Khumi Chin (`cnk`). (\#381)
-   Made summary generation in `common_characters.py` optional. (\#382)
-   Fixed phone counting in `data/src/generate_phones_summary.py` (\#390, \#392)
-   Reorganizes scraping scripts under `data/scrape` (\#394)
-   Reorganizes `.phones` files and related scripts under `data/phones` (\#395)

### Under `wikipron/` and elsewhere

#### Added

-  Added test of phones list generation in `test_data/test_summary.py` (\#363)

[1.2.0] - 2021-01-30
--------------------

### Under `data/`

#### Added

-   Added generate_phones_summary.py, generating `./phones/README.md` and `./phones/phones_summary.tsv`. (\#344) 
-   Added Afrikaans whitelists, filtered TSV file, rescraped phonemic and phonetic TSV files. (\#311)
-   Added German whitelists and filtered TSV file. (\#285)
-   Added whitelisting capabilities to `postprocess`. (\#152)
-   Added whitelists for Dutch, English, Greek, Latin, Korean, and Spanish.
    (\#158, etc.)
-   Logged dialect configuration if specified. (\#133)
-   Added typing to big scrape code. (\#140)
-   Added argparse to allow limiting 'big scrape' to individual languages
    with `--restriction` flag. (\#154)
-   Added Manchu (`mnc`). (\#185)
-   Added Polabian (`pox`). (\#186)
-   Added `aar`, `bdq`, `jje`, and `lsi`. (\#202)
-   Added `tyv` to `languagecodes.py` (\#203, \#205)
-   Added `bcl`, `egl`, `izh`, `ltg`, `azg`, `kir` and `mga` to `languagecodes.py`. (\#205)
-   Added `nep` to `languagecodes.py`. (\#206)
-   Added Ingrian (`izh`). (\#215)
-   Added French phoneme list and filtered TSV file. (\#213, \#217)
-   Added Corsican (`cos`). (\#222)
-   Added Middle Korean (`okm`). (\#223)
-   Added Middle Irish (`mga`). (\#224)
-   Added Old Portuguese (`opt`). (\#225)
-   Added Serbo-Croatian phoneme list and filtered TSV files. (\#227)
-   Added Tuvan (`tyv`). (\#228)
-   Added Shan (`shn`) with custom extraction. (\#229)
-   Added Northern Kurdish (`kmr`). (\#243)
-   Added a script to facilitate the creation of a `.phones` file. (\#246)
-   Added IPA validity checks for phonemes. (\#248)
-   Split multiple pronunciations joined by tilde in `eng_us_phonetic`.
-   Added Italian phoneme list and filtered TSV file. (\#260, \#261)
-   Added Adyghe phone list and filtered TSV file. (\#262, \#263)
-   Added Bulgarian phoneme list and filtered TSV file. (\#264, \#267)
-   Added Icelandic phoneme list and filtered TSV file. (\#269, \#270)
-   Added Slovenian phoneme list and filtered TSV file. (\#271, \#273)
-   Added normalization to `list_phones.py`. Corrected errors relating to
    `ipapy` (\#275)
-   Added Welsh .phones lists and filtered TSV files. (\#274, \#276)
-   Added draft of covering grammar script. (\#297)
-   Updated `data/phones/README.md` with instructions to re-scrape. (\#279, \#281)
-   Added Vietnamese `.phones` files and re-scraped and filtered `.tsv` files.
    (\#278, \#283)
-   Added Hindi `.phones` files and the re-scraped and filtered `.tsv` files.
    (\#282, \#284)
-   Added Old Frisian (`ofs`). (\#294)
-   Added Dungan (`dng`). (\#293)
-   Added Latgalian (`ltg`). (\#296)
-   Added draft of covering grammar script. (\#297)
-   Added Portuguese `.phones` files and re-scraped data. (\#290, \#304)
-   Added Japanese `.phones` files and re-scraped data. (\#230, \#307)
-   Added Moksha (`mdf`). (\#295)
-   Added Azerbaijani `.phones` files and re-scraped data. (\#306, \#312)
-   Added Turkish `.phones` file and re-scraped data. (\#313, \#314)
-   Added Maltese `.phones` file and re-scraped data. (\#317, \#318)
-   Added Latvian `.phones` file and re-scraped data. (\#321, \#322)
-   Added Khmer `.phones` file and re-scraped data. (\#324, \#327)
-   Added Østnorsk (Bokmål) `.phones` file and re-scraped data. (\#324, \#327)
-   Added SIGMORPHON 2021 frequencies JSON. (\#332)
-   Several languages added to `languagecodes.py`. (\#334)
-   Configured scripts for Kazakh (`kaz`). (\#345)
-   Added Easten Lawa (`lwl`). (\#346)
-   Configuration for Western Lawa (`lcp`). (\#347)
-   Added Nyahkur (`cbn`). (\#348)
-   Split Tagalog (`tgl`) scripts into Latin and Baybayin, rescraped. (\#351)

#### Changed

-   Changed the name of the existing `./phones/README.md` to `./phones/HOWTO.md`. (\#344)
-   Edited the name of `generate_summary.py` to `generate_tsv_summary.py`.(\#344)
-   Edited the output file name of `generate_tsv_summary.py` to `tsv_summary.tsv`.(\#344)
-   Edited the arm_e_phonetic.phones and arm_w_phonetic.phones files. (\#298)
-   Improved printing in the README table. (\#145)
-   Renamed data directory `data`. (\#147)
-   Split `may` into Latin and Arabic files. (\#164)
-   Split `pan` into Gurmukhi and Shahmukhī. (\#169)
-   Split `uig` into Perso-Arabic and Cyrillic. (\#173)
-   Only allowed Latin spellings in Maltese lexicon. (\#166).
-   Split `mon` into Cyrillic and Mongol Bichig (\#179).
-   Merged whitelist.py into 'big scrape' script. src scrape.py now checks for
    existence of whitelist file during scrape to create second filtered TSV.
    New TSV placed under `tsv/\*\_filtered.tsv`. (\#154).
-   Updated `generate_summary.py` to reflect presence of 'filtered' tsv. (\#154)
-   Imperial Aramaic (`arc`) split into three scripts properly. (\#187)
-   Flattened data directory structure. (\#194)
-   Updated Georgian (`geo`) to take advantage of upstream bot-based
    consistency fixes. (\#138)
-   Split `arm` into Eastern and Western dialects. (\#197)
-   Rescraped files with new whitelists. (\#199)
-   Updated logging statements for consistency. (\#196)
-   Renamed `.whitelist` file extension name as `.phones`. (\#207)
-   Split `ban` into Latin and Balinese scripts. (\#214)
-   Split `kir` into Cyrillic and Arabic. (\#216)
-   Split Latin (`lat`) into its dialects. (\#233)
-   Added MyPy coverage for `wikipron`, `tests` and `data` directories. (\#247)
-   Modified paths in `codes.py`, `scrape.py`, and `split.py`. (\#251, \#256)
-   Modified config flags in `languages.json` and `scrape.py`. (\#258)
-   Edited Serbo-Croatian `.phones` file to list all vowel/pitch accent
    combinations. Re-scraped Serbo-Croatian data. (\#288)
-   Moved `list_phones.py` to parent directory. (\#265, \#266)
-   Moved `list_phones.py` to `src` directory. (\#297)
-   Frequencies code no longer overwrites TSV files. (\#320)
-   Updated `data/phones/README.md` to specify that `.phones` files should be
    in NFC normalization form. (\#333)
-   Kurdish (`kur`) and Opata (`opt`) removed from `languages.json`. (\#334)
-   Re-scraped Armenian data. Fixed an error in West Armenian phone list.
    (\#338)

#### Fixed

-   Fixed path issue with phonetic whitelisted files. (\#195)

### Under `wikipron/` and Elsewhere

#### Added

-   Added positive flags for stress, syllable boundaries, tones, segment to `cli.py`. (\#141)
-   Added positive flags for space skipping to `cli.py`. (\#257)
-   Added two Vietnamese dialects to `languages.json`. (\#139)
-   Handled additional language codes. (\#132, \#148)
-   Added `--no-skip-spaces-word` and `--no-skip-spaces-pron` flag. (\#135)
-   Allowed ASCII apostrophes (0x27) in spellings. (\#172).
-   Added Vietnamese extraction function. (\#181).
-   Modified pron selector in Latin extraction function. (\#183).
-   Added `--no-tone` flag. (\#188)
-   Customized extractor and new scraped prons for `khb`. (\#219)
-   Added `tests/test_data` directory containing two tests. (\#226, \#251)
-   Added HTTP User-Agent header to API calls to Wiktionary. (\#234)
-   Added support for python 3.9 (\#240)
-   Added black style formatting to `.circleci/config.yml`. (\#242)
-   Added logging for scraping a language with `--dialect` specified
    that requires its custom extraction logic. (\#245)
-   Improved CircleCI workflow with orbs. (\#249)
-   Added `test_split.py` to `tests/test_data`. (\#256)
-   Handled Cantonese for scraping. (\#277)
-   Added exclusion for reconstructions. (\#302)
-   Added Vietnamese contour tone grouping test in `tests/test_config.py` (\#308)
-   Added restart functionality. (\#340)
-   Added very basic API for script detection. (\#341)
-   Added `--skip-parens` and `--no-skip-parens` flags. (\#343)

#### Changed

-   Renamed arguments to positive statements in `wikipron/config.py` and edited `_get_process_pron` function accordingly. (\#141, \#257)
-   Changed testing values used in `tests/test_config.py` in order to accomodate the addition of positive flags. (\#141)
-   Specified UTF-8 encoding in handling text files. (\#221)
-   Moved previous contents of `tests` into `tests/test_wikipron` (\#226)
-   Updated the packages version numbers in requirements.txt to their latest according to PyPI (\#239)
-   Updated the default pron selector to also look for IPA strings under paragraphs in addition to list items. (\#295)
-   Updated segments package version to 2.2.0 (\#308)

#### Removed

-   Moved Wiktionary querying functions from `test_languagecodes.py` to `codes.py` (\#205)

[1.1.0] - 2020-03-03
--------------------

#### Added

-   Added the extraction function for Mandarin Chinese and its scraped data. (\#124)
-   Integrated Wortschatz frequencies. (\#122)

#### Changed

-   Updated the Japanese extraction function and Japanese data. (\#129)
-   Updated all scraped Wiktionary data and frequency data. (\#127, \#128)
-   Generalized the splitting script in the big scrape. (\#123)
-   Moved small file removal to `generate_summary.py`. (\#119)
-   Updated Russian data. (\#115)

#### Fixed

-   Avoided and logged error in case of pron processing failure. (\#130)

[1.0.0] - 2019-11-29
----------------------

#### Added

-   Handled Japanese. (\#109, \#114)
-   Handled Latin, for which the actual graphemes cannot be the Wiktionary
    page titles and have to come from within the page. (\#92, \#93)
-   Handled Thai, whose pronunciations are embedded in HTML tables. (\#90)
-   Handled Khmer, whose pronunciations are embedded in HTML tables. (\#88)
-   IPA segmentation using spaces by default, with the `--no-segment` flag to
    optionally turn it off. (\#69, \#79, \#83, \#89, \#100)
-   Added TSV files for all Wiktionary languages with over 100 entries.
    (\#61, \#76, \#95, \#97, \#103, \#104)
-   Resolved Wiktionary language names for languages with at least 100
    pronunciation entries. (\#52, \#55)

#### Changed

-   Removed duplicate <word, pronunciation> pairs in the persisted data. (\#85, \#111, \#116)
-   Split Welsh into Northern Wales and Southern dialects in the persisted data. (\#110)
-   Factored out casefolding. (\#102)
-   Split Serbo-Croatian into Cyrillic and Latin TSVs. (\#96)
-   Generalized word and pronunciation extraction. (\#88)

#### Removed

-   Removed the timeout in smoke tests. (\#107)
-   Removed the `output` option. (\#82)
-   Removed the `require_dialect_label` option. (\#77)

#### Fixed

-   Skipped pronunciations with a dash. (\#106)
-   Skipped empty pronunciations in scraping. (\#59)
-   Updated the `<li>` XPath selector for an optional layer of `<span>` to cover
    previously unhandled languages (e.g., Korean). (\#50)
-   Updated the `<li>` XPath selector for
    `title="wikipedia:<language> phonology"` to cover previously unhandled
    languages (e.g., Estonian and Slovak). (\#49)

#### Security

-   Avoided using `exec` to retrieve the version string. Used `pkg_resources`
    instead. (\#63)

[0.1.1] - 2019-08-14
----------------------

#### Fixed

-   Fixed import bug. (\#45)

[0.1.0] - 2019-08-14
----------------------

First release.
