"""Thin wrapper over requests + lxml for HTML fetching and XPath queries.

This replaces the unmaintained requests_html library. Only the features
actually used by wikipron are implemented: HTMLSession.get() for HTTP
requests and .html.xpath() for XPath-based HTML parsing.
"""

from typing import Literal, overload

import requests
from lxml import html as lxml_html
from lxml.html import HtmlElement


class HTMLTree:
    """An HTML tree supporting XPath queries."""

    def __init__(self, element: HtmlElement) -> None:
        self._element: HtmlElement = element

    @overload
    def xpath(
        self,
        selector: str,
        *,
        first: Literal[True],
    ) -> "Element | str | None": ...

    @overload
    def xpath(
        self,
        selector: str,
        *,
        first: Literal[False] = ...,
    ) -> list["Element"]: ...

    def xpath(
        self,
        selector: str,
        *,
        first: bool = False,
    ) -> list["Element"] | "Element" | str | None:
        results = self._element.xpath(selector)
        wrapped: list[Element] = [
            Element(r) for r in results if hasattr(r, "tag")
        ]
        if first:
            return wrapped[0] if wrapped else None
        return wrapped


class Element(HTMLTree):
    """An HTML element with text and attribute access."""

    @property
    def text(self) -> str:
        # text_content() concatenates all descendant text,
        # matching the behavior of requests_html's Element.text.
        return self._element.text_content()

    @property
    def attrs(self) -> dict[str, str]:
        return dict(self._element.attrib)


class HTMLResponse:
    """Wraps a requests.Response to provide .html.xpath() access."""

    def __init__(self, response: requests.Response) -> None:
        self._response: requests.Response = response
        self._html: HTMLTree | None = None

    @property
    def html(self) -> HTMLTree:
        if self._html is None:
            self._html = HTMLTree(lxml_html.fromstring(self._response.content))
        return self._html
