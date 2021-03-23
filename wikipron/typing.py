import requests

from typing import TYPE_CHECKING, Callable, Iterator, NewType, Tuple


if TYPE_CHECKING:
    from wikipron.config import Config  # noqa: F401


Word = NewType("Word", str)
Pron = NewType("Pron", str)
WordPronPair = Tuple[Word, Pron]
ExtractFunc = Callable[
    [Word, requests.Response, "Config"], Iterator[WordPronPair]
]
