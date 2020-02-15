"""Scrapes grapheme-to-phoneme data from Wiktionary."""

import pkg_resources

from wikipron.config import Config
from wikipron.scrape import scrape


__version__ = pkg_resources.get_distribution("wikipron").version
__all__ = ["__version__", "Config", "scrape"]
