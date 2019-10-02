# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- TSV files for all Wiktionary languages with over 1000 entries (except Russian) (#61)
- Resolved Wiktionary language names for languages with at least 100
  pronunciation entries. (#52, #55)

### Changed
### Deprecated
### Removed
### Fixed
- Skipped empty pronunciations in scraping. (#59)
- Updated the `<li>` XPath selector for an optional layer of `<span>`
  to cover previously unhandled languages (e.g., Korean). (#50) 
- Updated the `<li>` XPath selector for `title="wikipedia:<language> phonology"`
  to cover previously unhandled languages (e.g., Estonian and Slovak). (#49)

### Security

## [0.1.1] - 2019-08-14

### Fixed
- Fixed import bug. (#45)

## [0.1.0] - 2019-08-14

First Release
