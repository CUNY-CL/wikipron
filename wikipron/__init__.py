"""Scraping grapheme-to-phoneme data from Wiktionary."""

from ._version import __version__

from wikipron.config import Config
from wikipron.scrape import scrape


__all__ = ["__version__", "Config", "scrape"]
