from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from wikipron.config import Config  # noqa: F401


WordPronPair = tuple[str, str]
ExtractFunc = Callable[
    [str, requests.Response, "Config"], Iterator[WordPronPair]
]
