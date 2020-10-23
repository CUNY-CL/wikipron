from typing import Any, Dict

import requests

from wikipron.config import Config
from wikipron.scrape import HTTP_HEADERS


def config_factory(**kwargs) -> Config:
    """Create a Config object for testing."""
    config_dict: Dict[str, Any] = {"key": "eng"}  # Default; may be overridden.
    config_dict.update(**kwargs)
    return Config(**config_dict)


def can_connect_to_wiktionary() -> bool:
    """Check whether WAN connection to Wiktionary is available."""
    try:
        requests.get(
            "https://en.wiktionary.org/wiki/linguistics", headers=HTTP_HEADERS
        )
    except requests.ConnectionError:
        return False
    else:
        return True
