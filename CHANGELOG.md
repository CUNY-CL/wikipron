Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic
Versioning](http://semver.org/spec/v2.0.0.html).

Unreleased
----------

### Added

-   Logs dialect configuration if specified (\#133).

### Deprecated
### Removed
### Fixed
### Security

[1.1.0] - 2020-03-03
--------------------

### Added

-   Added the extraction function for Mandarin Chinese and its scraped data. (\#124)
-   Integrated Wortschatz frequencies. (\#122)

### Changed

-   Updated the Japanese extraction function and Japanese data. (\#129)
-   Updated all scraped Wiktionary data and frequency data. (\#127, \#128)
-   Generalized the splitting script in the big scrape. (\#123)
-   Moved small file removal to `generate_summary.py`. (\#119)
-   Updated Russian data. (\#115)

### Fixed

-   Avoided and logged error in case of pron processing failure. (\#130)

[1.0.0] - 2019-11-29
----------------------

### Added

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

### Changed

-   Removed duplicate <word, pronunciation> pairs in the persisted data. (\#85, \#111, \#116)
-   Split Welsh into Northern Wales and Southern dialects in the persisted data. (\#110)
-   Factored out casefolding. (\#102)
-   Split Serbo-Croatian into Cyrillic and Latin TSVs. (\#96)
-   Generalized word and pronunciation extraction. (\#88)

### Removed

-   Removed the timeout in smoke tests. (\#107)
-   Removed the `output` option. (\#82)
-   Removed the `require_dialect_label` option. (\#77)

### Fixed

-   Skipped pronunciations with a dash. (\#106)
-   Skipped empty pronunciations in scraping. (\#59)
-   Updated the `<li>` XPath selector for an optional layer of `<span>` to cover
    previously unhandled languages (e.g., Korean). (\#50)
-   Updated the `<li>` XPath selector for
    `title="wikipedia:<language> phonology"` to cover previously unhandled
    languages (e.g., Estonian and Slovak). (\#49)

### Security

-   Avoided using `exec` to retrieve the version string. Used `pkg_resources`
    instead. (\#63)

[0.1.1] - 2019-08-14
----------------------

### Fixed

-   Fixed import bug. (\#45)

[0.1.0] - 2019-08-14
----------------------

First release.
