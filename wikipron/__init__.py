"""Scrapes grapheme-to-phoneme data from Wiktionary."""

from importlib.metadata import version

from wikipron.config import Config
from wikipron.scrape import scrape


__version__ = version("wikipron")
__all__ = ["__version__", "Config", "scrape"]
