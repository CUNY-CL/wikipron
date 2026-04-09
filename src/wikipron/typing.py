from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wikipron.config import Config  # noqa: F401
    from wikipron.html_utils import HTMLResponse  # noqa: F401


WordPronPair = tuple[str, str]
ExtractFunc = Callable[[str, "HTMLResponse", "Config"], Iterator[WordPronPair]]
