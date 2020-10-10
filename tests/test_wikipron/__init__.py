import requests

from wikipron.config import Config


def config_factory(**kwargs) -> Config:
    """Create a Config object for testing."""
    config_dict = {"key": "eng"}  # The one default; may be overridden.
    config_dict.update(**kwargs)
    return Config(**config_dict)


def can_connect_to_wiktionary() -> bool:
    """Check whether WAN connection to Wiktionary is available."""
    try:
        requests.get("https://en.wiktionary.org/wiki/linguistics")
    except (requests.ConnectionError, requests.ConnectTimeout):
        return False
    else:
        return True
