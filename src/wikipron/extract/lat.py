"""Word and pron extraction for Latin.

As of writing (November 2019), Latin cannot use the default extraction
function, which uses the Wiktionary entry page title as the graphemes.
Latin uses the macrons orthographically (for vowel length),
but the Wiktionary entry page titles never have them.
The correct orthographic form is available from within the entry page.

In the underlying HTML, the Latin entry pages take several forms.

1. Because the orthographic distinction by macrons is collapsed,
   a Latin entry page organizes the "homographs" in terms of "Etymologies".
   Each etymology has one or more (word, pronunciation) pairs, in the form of
   a ``<strong class="Latn headword" lang="la">`` element and a
   ``<ul>`` element containing the pronunciation(s). Multiple pairs occur
   when an etymology groups several homographic lemmas that are spelled
   identically when the macrons are stripped (e.g. ``amāre`` and ``amārē``
   both appear under the ``/wiki/amare`` entry's Etymology 2). When there
   are multiple pairs, the headwords and pron lists are interleaved in
   document order (one pair per sub-section such as "Pronunciation 1" /
   "Pronunciation 2"), and we pair them positionally.

   <div class="mw-heading mw-heading3">
       <h3 id="Etymology_1">Etymology 1</h3>
   </div>
   ...
   <p>
       <!-- The orthographic form we want. -->
       <strong class="Latn headword" lang="la">...</strong>
   </p>
   ...
   <ul>
       <!-- The pronunciation we want. -->
       <span class="IPA">...</span>
   </ul>

2. Some pages share a single "Pronunciation" section (an ``h3`` under the
   Latin ``h2``) across all etymologies. The etymologies themselves contain
   only headwords, no pronunciation lists. E.g., ``/wiki/amo`` has one
   Pronunciation h3 followed by Etymology 1 and Etymology 2, each with an
   ``amō`` headword but no pron ul of their own. In that case we fall back
   to the shared Pronunciation section's prons for every headword in every
   etymology.

3. For entries that don't have "Etymology" sections, the underlying HTML
   structure is very similar, with everything moved up one level,
   from <h3> for an etymology to <h2> for Latin.
"""

import typing

from wikipron.html_utils import HTMLResponse

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR

if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.html_utils import Element
    from wikipron.typing import Iterator, WordPronPair


_HEADING_XPATH_SELECTOR = '//div[contains(@class, "mw-heading")]'

# Predicate that restricts a following-sibling of the section heading to
# elements still within that section — i.e. whose nearest preceding heading
# sibling (at the section's level or higher) is the section's own heading.
# For the "Latin" h2 section we only stop at the next h2, allowing h3
# sub-sections through. For an "Etymology_N" h3 section we stop at the next
# h2 or h3.
_SCOPED_TO_SECTION_TEMPLATE = """
preceding-sibling::div[
    contains(@class, "mw-heading") and ({stop_headings})
][1][{heading}[@id = "{tag}"]]
"""

_HEADWORDS_XPATH_TEMPLATE = """
//div[{heading}[@id = "{tag}"]]
  /following-sibling::p[
    .//strong[@class = "Latn headword" and @lang = "la"]
    and
    {scoped_to_section}
  ]
"""

_PRON_ULS_XPATH_TEMPLATE = """
//div[{heading}[@id = "{tag}"]]
  /following-sibling::ul[
    descendant::a[@title = "Appendix:Latin pronunciation"]
    and
    {scoped_to_section}
  ]
"""

_DIALECT_LI_FILTER_TEMPLATE = """
.//li[
  sup[a[@title = "Appendix:Latin pronunciation"]]
  and
  span[contains(@class, "IPA")]
  and
  .//span[(contains(@class, "ib-content")
           or contains(@class, "label-content"))
          and a[{dialects_text}]]
]
"""


def _get_tags(request: HTMLResponse) -> list[str]:
    """Extract the Latin Etymology ID tags from the page content."""
    tags = []
    found_latin = False
    for heading in request.html.xpath(_HEADING_XPATH_SELECTOR):
        h2s = heading.xpath("h2")
        if h2s:
            tag_id = h2s[0].attrs.get("id", "")
            if tag_id == "Latin":
                found_latin = True
            elif found_latin:
                break
            continue
        if not found_latin:
            continue
        h3s = heading.xpath("h3")
        if h3s:
            tag_id = h3s[0].attrs.get("id", "")
            if tag_id.startswith("Etymology"):
                tags.append(tag_id)
    if not tags:
        tags = ["Latin"]
    return tags


def _get_shared_pronunciation_tag(request: HTMLResponse) -> str | None:
    """Return the id of a shared Pronunciation h3 under Latin, if any.

    "Shared" means an h3 whose id starts with "Pronunciation" that sits
    between the Latin h2 and the first Etymology h3 (so it applies to all
    subsequent etymologies, rather than being nested inside one).
    """
    found_latin = False
    for heading in request.html.xpath(_HEADING_XPATH_SELECTOR):
        h2s = heading.xpath("h2")
        if h2s:
            tag_id = h2s[0].attrs.get("id", "")
            if tag_id == "Latin":
                found_latin = True
            elif found_latin:
                return None
            continue
        if not found_latin:
            continue
        h3s = heading.xpath("h3")
        if h3s:
            tag_id = h3s[0].attrs.get("id", "")
            if tag_id.startswith("Pronunciation"):
                return tag_id
            if tag_id.startswith("Etymology"):
                return None
    return None


def _section_pron_uls(
    request: HTMLResponse, tag: str, heading: str
) -> "list[Element]":
    stop_headings = "h2" if heading == "h2" else "h2 or h3"
    scoped_to_section = _SCOPED_TO_SECTION_TEMPLATE.format(
        heading=heading, tag=tag, stop_headings=stop_headings
    )
    xpath = _PRON_ULS_XPATH_TEMPLATE.format(
        heading=heading, tag=tag, scoped_to_section=scoped_to_section
    )
    return request.html.xpath(xpath)


def _section_headword_ps(
    request: HTMLResponse, tag: str, heading: str
) -> "list[Element]":
    stop_headings = "h2" if heading == "h2" else "h2 or h3"
    scoped_to_section = _SCOPED_TO_SECTION_TEMPLATE.format(
        heading=heading, tag=tag, stop_headings=stop_headings
    )
    xpath = _HEADWORDS_XPATH_TEMPLATE.format(
        heading=heading, tag=tag, scoped_to_section=scoped_to_section
    )
    return request.html.xpath(xpath)


def _prons_from_ul(ul_element: "Element", config: "Config") -> "Iterator[str]":
    """Yield prons from a pronunciation <ul>, applying any dialect filter."""
    if config.dialect:
        dialects_text = " or ".join(
            f'contains(text(), "{d.strip()}")'
            for d in config.dialect.split("|")
        )
        filter_xpath = _DIALECT_LI_FILTER_TEMPLATE.format(
            dialects_text=dialects_text
        )
        for li in ul_element.xpath(filter_xpath):
            yield from yield_pron(li, IPA_XPATH_SELECTOR, config)
    else:
        yield from yield_pron(ul_element, IPA_XPATH_SELECTOR, config)


def _word_from_headword_p(p_element: "Element") -> str | None:
    strong_els = p_element.xpath(
        './/strong[@class = "Latn headword" and @lang = "la"]'
    )
    if not strong_els:
        return None
    # text is sometimes incorrectly appended with " (" or " (+" as the
    # beginning of morphological information.
    return strong_els[0].text.rstrip(" (+")


def extract_word_pron_latin(
    word: str, request: HTMLResponse, config: "Config"
) -> "Iterator[WordPronPair]":
    # For Latin, we don't use the title word from the Wiktionary page,
    # because it never has macrons (necessary for Latin vowel length).
    # We get the word from each section (etymology, or the Latin section
    # itself if no etymologies).
    tags = _get_tags(request)
    shared_pron_uls: "list[Element] | None" = None
    for tag in tags:
        heading = "h2" if tag == "Latin" else "h3"
        headword_ps = _section_headword_ps(request, tag, heading)
        pron_uls = _section_pron_uls(request, tag, heading)
        if pron_uls:
            # Both queries return nodes in document order; the i-th
            # headword pairs with the i-th pronunciation list within the
            # section.
            for p_el, ul_el in zip(headword_ps, pron_uls):
                latin_word = _word_from_headword_p(p_el)
                if latin_word is None:
                    continue
                for pron in _prons_from_ul(ul_el, config):
                    yield latin_word, pron
        elif tag != "Latin":
            # No pron in this etymology — fall back to a shared
            # Pronunciation section (if any) that applies across all
            # etymologies.
            if shared_pron_uls is None:
                shared_tag = _get_shared_pronunciation_tag(request)
                shared_pron_uls = (
                    _section_pron_uls(request, shared_tag, "h3")
                    if shared_tag is not None
                    else []
                )
            for p_el in headword_ps:
                latin_word = _word_from_headword_p(p_el)
                if latin_word is None:
                    continue
                for ul_el in shared_pron_uls:
                    for pron in _prons_from_ul(ul_el, config):
                        yield latin_word, pron
