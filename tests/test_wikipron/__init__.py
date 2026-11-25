from typing import Any

import requests

from wikipron.config import Config
from wikipron.html_utils import HTMLResponse
from wikipron.scrape import HTTP_HEADERS


def config_factory(**kwargs) -> Config:
    """Create a Config object for testing."""
    config_dict: dict[str, Any] = {"key": "eng"}  # Default; may be overridden.
    config_dict.update(**kwargs)
    return Config(**config_dict)


def _offline_response(html: str) -> HTMLResponse:
    """Wrap an HTML string as an HTMLResponse, without a network fetch."""
    response = requests.Response()
    # Declare the charset so libxml2 decodes the bytes as UTF-8 (real
    # Wiktionary pages carry a <meta charset> in their <head>).
    response._content = ('<meta charset="utf-8">' + html).encode("utf-8")
    return HTMLResponse(response)


def can_connect_to_wiktionary() -> bool:
    """Check whether WAN connection to Wiktionary is available."""
    try:
        requests.get(
            "https://en.wiktionary.org/wiki/linguistics",
            headers=HTTP_HEADERS,
        )
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
    ):
        return False
    else:
        return True
