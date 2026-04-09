"""Thin wrapper over requests + lxml for HTML fetching and XPath queries.

This replaces the unmaintained requests_html library. Only the features
actually used by wikipron are implemented: HTMLSession.get() for HTTP
requests and .html.xpath() for XPath-based HTML parsing.
"""

from lxml import html as lxml_html


class HTMLTree:
    """An HTML tree supporting XPath queries."""

    def __init__(self, element):
        self._element = element

    def xpath(self, selector, *, first=False):
        results = self._element.xpath(selector)
        wrapped = [Element(r) if hasattr(r, "tag") else r for r in results]
        if first:
            return wrapped[0] if wrapped else None
        return wrapped


class Element(HTMLTree):
    """An HTML element with text and attribute access."""

    @property
    def text(self):
        # text_content() concatenates all descendant text,
        # matching the behavior of requests_html's Element.text.
        return self._element.text_content()

    @property
    def attrs(self):
        return dict(self._element.attrib)


class HTMLResponse:
    """Wraps a requests.Response to provide .html.xpath() access."""

    def __init__(self, response):
        self._response = response
        self._html = None

    @property
    def html(self):
        if self._html is None:
            self._html = HTMLTree(lxml_html.fromstring(self._response.content))
        return self._html
