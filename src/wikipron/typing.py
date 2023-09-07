import requests

from typing import TYPE_CHECKING, Callable, Iterator, Tuple


if TYPE_CHECKING:
    from wikipron.config import Config  # noqa: F401


WordPronPair = Tuple[str, str]
ExtractFunc = Callable[
    [str, requests.Response, "Config"], Iterator[WordPronPair]
]
