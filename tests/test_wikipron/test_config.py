import datetime
import re

import pytest
import requests
from lxml import html as lxml_html

from wikipron.config import _PHONEMES_REGEX, _PHONES_REGEX
from wikipron.html_utils import HTMLResponse, HTMLTree
from wikipron.scrape import _PAGE_TEMPLATE, HTTP_HEADERS

from . import can_connect_to_wiktionary, config_factory

_TODAY = datetime.date.today()
_DATE_TODAY = _TODAY.isoformat()
_DATE_FUTURE = (_TODAY + datetime.timedelta(days=10)).isoformat()
_DATE_RECENT_PAST = (_TODAY - datetime.timedelta(days=10)).isoformat()
_DATE_DISTANT_PAST = (_TODAY - datetime.timedelta(days=20)).isoformat()


@pytest.mark.parametrize(
    "casefold, input_word, expected_word",
    [(True, "FooBar", "foobar"), (False, "FooBar", "FooBar")],
)
def test_casefold(casefold, input_word, expected_word):
    config = config_factory(casefold=casefold)
    assert config.casefold(input_word) == expected_word


@pytest.mark.parametrize(
    "stress, syllable_boundaries, input_pron, expected_pron",
    [
        (False, False, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ ɡ w ɪ s t ɪ k s"),
        (False, True, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ . ɡ w ɪ s . t ɪ k s"),
        (True, False, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ ˈɡ w ɪ s t ɪ k s"),
        (True, True, "lɪŋ.ˈɡwɪs.tɪks", "l ɪ ŋ . ˈɡ w ɪ s . t ɪ k s"),
        # GH-59: Prons with only stress or syllable boundaries are skipped.
        (True, True, "ˈ", None),
        (True, True, ".", None),
        (True, True, "", None),
    ],
)
def test_process_pron(stress, syllable_boundaries, input_pron, expected_pron):
    config = config_factory(
        stress=stress, syllable_boundaries=syllable_boundaries
    )
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "segment, input_pron, expected_pron",
    [
        (True, "lɛ̃.ɡɥis.tik", "l ɛ̃ . ɡ ɥ i s . t i k"),
        (True, "kʰæt", "kʰ æ t"),
        (True, "ad͡ʒisɐ̃w", "a d͡ʒ i s ɐ̃ w"),
        (True, "ovoɫˈnʲɤ", "o v o ɫ ˈnʲ ɤ"),
        # GH-83: Challenging IPA tokenizations.
        (True, "ˌæb.oʊˈmaɪ.sɪn", "ˌæ b . o ʊ ˈm a ɪ . s ɪ n"),
        (True, "ʷoˈtɤu̯", "ʷo ˈt ɤ u̯"),
        (True, "ⁿdaˈɽá.ma", "ⁿd a ˈɽ á . m a"),
        (False, "lɛ̃.ɡɥis.tik", "lɛ̃.ɡɥis.tik"),
        (True, "ʔɓaːn˧˩ ŋaː˦ˀ˥", "ʔ ɓ aː n ˧˩ # ŋ aː ˦ˀ˥"),
    ],
)
def test_segment(segment, input_pron, expected_pron):
    config = config_factory(segment=segment)
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "tone, input_pron, expected_pron",
    [
        (True, "aˈɓa.ɽé", "a ˈɓ a . ɽ é"),
        (False, "aˈɓa.ɽé", "a ˈɓ a . ɽ e"),
        (
            False,
            "feɪ̯³⁵ʈ͡ʂaɪ̯³⁵kʰwaɪ̯⁵¹⁻⁵³lɤ⁵¹ʂweɪ̯²¹⁴⁻²¹⁽⁴⁾",
            "f e ɪ̯ ʈ͡ʂ a ɪ̯ kʰ w a ɪ̯ l ɤ ʂ w e ɪ̯",
        ),
        (
            False,
            "kra˨˩.duːk̚˨˩.ton˥˩.kʰaː˩˩˦",
            "k r a . d uː k̚ . t o n . kʰ aː",
        ),
        (False, "aˈt͡ʃe.w⁽ᵝ⁾á", "a ˈt͡ʃ e . w ⁽ᵝ ⁾ a"),
    ],
)
def test_tone(tone, input_pron, expected_pron):
    config = config_factory(tone=tone)
    assert config.process_pron(input_pron) == expected_pron


@pytest.mark.parametrize(
    "error, cut_off_date, word_available_date, expected",
    [
        # Input cut_off_date is invalid.
        (True, _DATE_FUTURE, None, None),
        (True, "not-a-valid_date", None, None),
        # Input cut_off_date is valid.
        (False, None, _DATE_RECENT_PAST, _DATE_TODAY),
        (False, _DATE_TODAY, _DATE_TODAY, _DATE_TODAY),
        (False, _DATE_TODAY, _DATE_RECENT_PAST, _DATE_TODAY),
        (False, _DATE_RECENT_PAST, _DATE_DISTANT_PAST, _DATE_RECENT_PAST),
        (False, _DATE_RECENT_PAST, _DATE_TODAY, _DATE_RECENT_PAST),
    ],
)
def test_cut_off_date(error, cut_off_date, word_available_date, expected):
    if error:
        with pytest.raises(ValueError):
            config_factory(cut_off_date=cut_off_date)
    else:
        config = config_factory(cut_off_date=cut_off_date)
        assert config.cut_off_date == expected


@pytest.mark.parametrize(
    "narrow, ipa_regex, word_in_ipa",
    [(True, _PHONES_REGEX, "[foobar]"), (False, _PHONEMES_REGEX, "/foobar/")],
)
def test_ipa_regex(narrow, ipa_regex, word_in_ipa):
    config = config_factory(narrow=narrow)
    # Make sure we use the correct regex depending on narrow vs broad.
    assert config.ipa_regex == ipa_regex
    # Make sure the IPA extraction by regex works.
    assert re.search(ipa_regex, word_in_ipa).group(1) == "foobar"


@pytest.mark.parametrize(
    "dialect, expected_pron_xpath_selector",
    [
        (
            None,
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "    or\n"
                '    @title = "w:English language"\n'
                "  ]]]\n"
                "  and\n"
                '  span[contains(@class, "IPA")]\n'
                "  \n"
                "]\n"
            ),
        ),
        (
            "US",
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "    or\n"
                '    @title = "w:English language"\n'
                "  ]]]\n"
                "  and\n"
                '  span[contains(@class, "IPA")]\n'
                "  and\n"
                '  (.//span[contains(@class, "ib-content")]//a[contains(text(), "US")]\n'  # noqa: E501
                '   or .//span[contains(@class, "ib-content") and (contains(text(), "US"))]\n'  # noqa: E501
                '   or ancestor::li//span[contains(@class, "ib-content")]//a[contains(text(), "US")]\n'  # noqa: E501
                '   or ancestor::li//span[contains(@class, "ib-content") and (contains(text(), "US"))]\n'  # noqa: E501
                '   or (count(.//span[contains(@class, "ib-content")][.//a])\n'  # noqa: E501
                '       - count(.//li//span[contains(@class, "ib-content")][.//a]) = 0\n'  # noqa: E501
                '       and count(ancestor::li//span[contains(@class, "ib-content")][.//a]) = 0))\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "General American | US",
            (
                "\n(//li|//p)[\n"
                "  (.|span)[sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "    or\n"
                '    @title = "w:English language"\n'
                "  ]]]\n"
                "  and\n"
                '  span[contains(@class, "IPA")]\n'
                "  and\n"
                '  (.//span[contains(@class, "ib-content")]//a[contains(text(), "General American") or contains(text(), "US")]\n'  # noqa: E501
                '   or .//span[contains(@class, "ib-content") and (contains(text(), "General American") or contains(text(), "US"))]\n'  # noqa: E501
                '   or ancestor::li//span[contains(@class, "ib-content")]//a[contains(text(), "General American") or contains(text(), "US")]\n'  # noqa: E501
                '   or ancestor::li//span[contains(@class, "ib-content") and (contains(text(), "General American") or contains(text(), "US"))]\n'  # noqa: E501
                '   or (count(.//span[contains(@class, "ib-content")][.//a])\n'  # noqa: E501
                '       - count(.//li//span[contains(@class, "ib-content")][.//a]) = 0\n'  # noqa: E501
                '       and count(ancestor::li//span[contains(@class, "ib-content")][.//a]) = 0))\n'  # noqa: E501
                "]\n"
            ),
        ),
    ],
)
def test_pron_xpath_selector(dialect, expected_pron_xpath_selector):
    config = config_factory(key="en", dialect=dialect)
    assert config.pron_xpath_selector == expected_pron_xpath_selector


# GH-591: On some pages (e.g. Bengali হুমায়রা) Wiktionary wraps the dialect
# label in <span class="usage-label-accent">, so <span class="ib-content"> is a
# grandchild of the <li>, not a direct child. The dialect XPath must use the
# descendant axis (.//span) to find it; otherwise the count(...)=0 fallback
# fires for every entry and all dialects leak into every dialect's output file.
_BENGALI_DIALECT_HTML = """
<ul>
<li>
<span class="usage-label-accent">
<span class="ib-brac label-brac">(</span>
<span class="ib-content label-content">
<a title="w:West Bengali dialect">Rarh</a>
</span>
<span class="ib-brac label-brac">)</span>
</span>
<sup><a title="wikipedia:Bengali phonology">key</a></sup>
<span class="IPA nowrap">/humaḛɾa/</span>
</li>
<li>
<span class="usage-label-accent">
<span class="ib-brac label-brac">(</span>
<span class="ib-content label-content">
<a title="w:Dhaka">Dhaka</a>
</span>
<span class="ib-brac label-brac">)</span>
</span>
<sup><a title="wikipedia:Bengali phonology">key</a></sup>
<span class="IPA nowrap">/humaḛɹa/</span>
</li>
</ul>
"""


def test_bengali_dialect_outer_wrapper_selection():
    tree = HTMLTree(lxml_html.fromstring(_BENGALI_DIALECT_HTML))
    config_rarh = config_factory(key="ben", dialect="Rarh | Standard Bengali")
    config_dhaka = config_factory(key="ben", dialect="Dhaka")
    config_any = config_factory(key="ben")
    # No dialect: both pronunciations are selected.
    assert len(tree.xpath(config_any.pron_xpath_selector)) == 2
    # Each dialect filter selects only its own li (the bug selected both).
    assert len(tree.xpath(config_rarh.pron_xpath_selector)) == 1
    assert len(tree.xpath(config_dhaka.pron_xpath_selector)) == 1


# A general pronunciation whose only label is a non-accent qualifier ("strong
# form" -- plain text, not an <a> link) must be kept for a dialect, while a
# sibling line tagged with a different accent is excluded.
_UNLINKED_QUALIFIER_HTML = """
<ul>
<li>
<span class="ib-brac">(</span>
<span class="ib-content">
<span class="usage-label-accent">strong form</span>
</span>
<span class="ib-brac">)</span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/ˈstrɒŋ/</span>
</li>
<li>
<span class="ib-brac">(</span>
<span class="ib-content"><span class="usage-label-accent">
<a title="w:Received Pronunciation">UK</a>
</span></span>
<span class="ib-brac">)</span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/ˈjuːkeɪ/</span>
</li>
</ul>
"""


def test_unlinked_qualifier_dialect_selection():
    tree = HTMLTree(lxml_html.fromstring(_UNLINKED_QUALIFIER_HTML))
    config_us = config_factory(key="en", dialect="US | General American")
    config_any = config_factory(key="en")
    # No dialect: both lines are selected.
    assert len(tree.xpath(config_any.pron_xpath_selector)) == 2
    # US: the "strong form" line carries no accent label of its own, so it is
    # kept as a general pronunciation; the UK-tagged line is excluded.
    us_nodes = tree.xpath(config_us.pron_xpath_selector)
    assert len(us_nodes) == 1
    assert "strong form" in us_nodes[0].text
    assert "UK" not in us_nodes[0].text


# Wiktionary can place the accent label on an outer <li> and the IPA on inner
# <li>s (there-type). Each inner line must inherit the ancestor's accent.
_NESTED_ACCENT_OUTER_HTML = """
<ul>
<li>
<span class="ib-content"><span class="usage-label-accent">
<a title="w:American English">US</a>
</span></span>
<ul>
<li>
<span class="ib-content">
<span class="usage-label-accent">strong form</span>
</span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/ðɛɹ/</span>
</li>
</ul>
</li>
<li>
<span class="ib-content"><span class="usage-label-accent">
<a title="w:Received Pronunciation">UK</a>
</span></span>
<ul>
<li>
<span class="ib-content">
<span class="usage-label-accent">strong form</span>
</span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/ðɛə/</span>
</li>
</ul>
</li>
</ul>
"""


def test_nested_accent_outer_dialect_selection():
    tree = HTMLTree(lxml_html.fromstring(_NESTED_ACCENT_OUTER_HTML))
    config_us = config_factory(key="en", dialect="US | General American")
    config_uk = config_factory(key="en", dialect="UK | Received Pronunciation")
    config_any = config_factory(key="en")
    assert len(tree.xpath(config_any.pron_xpath_selector)) == 2
    # Each inner line inherits its accent from the enclosing <li>.
    us_nodes = tree.xpath(config_us.pron_xpath_selector)
    uk_nodes = tree.xpath(config_uk.pron_xpath_selector)
    assert len(us_nodes) == 1 and "/ðɛɹ/" in us_nodes[0].text
    assert len(uk_nodes) == 1 and "/ðɛə/" in uk_nodes[0].text


# A general pronunciation on an outer <li> with accent variants nested in
# sub-<li>s (bus/cookie-type). The general line is kept (its own labels,
# ignoring the nested variants', contain no accent); the nested non-US variant
# is excluded.
_GENERAL_OUTER_NESTED_ACCENT_HTML = """
<ul>
<li>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/bʌs/</span>
<ul>
<li>
<span class="ib-content"><span class="usage-label-accent">
<a title="w:English language">Northern England</a>
</span></span>
<sup><a title="Appendix:English pronunciation">key</a></sup>
<span class="IPA">/bʊs/</span>
</li>
</ul>
</li>
</ul>
"""


def test_general_outer_dialect_selection():
    tree = HTMLTree(lxml_html.fromstring(_GENERAL_OUTER_NESTED_ACCENT_HTML))
    config_us = config_factory(key="en", dialect="US | General American")
    config_any = config_factory(key="en")
    # No dialect: both the general line and the nested variant are selected.
    assert len(tree.xpath(config_any.pron_xpath_selector)) == 2
    # US: only the general outer line is kept; the nested "Northern England"
    # variant is excluded (its own accent label does not match US).
    us_nodes = tree.xpath(config_us.pron_xpath_selector)
    assert len(us_nodes) == 1
    assert "/bʌs/" in us_nodes[0].text


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
def test_american_english_dialect_selection():
    # Pick a word for which Wiktionary has dialect-specified pronunciations
    # for both US and non-US English.
    word = "mocha"
    session = requests.Session()
    session.headers.update(HTTP_HEADERS)
    raw = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10)
    response = HTMLResponse(raw)
    # Construct two configs to demonstrate the US dialect (non-)selection.
    config_only_us = config_factory(key="en", dialect="US | American English")
    config_any_dialect = config_factory(key="en")
    # Apply each config's XPath selector.
    results_only_us = response.html.xpath(config_only_us.pron_xpath_selector)
    results_any_dialect = response.html.xpath(
        config_any_dialect.pron_xpath_selector
    )
    assert (
        len(results_any_dialect)  # containing both US and non-US results
        > len(results_only_us)  # containing only the US result
        > 0
    )


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
def test_spanish_dialect_selection():
    # Pick a word for which Wiktionary has dialect-specified pronunciations
    # for both Castilian and Latin American Spanish.
    word = "códice"
    session = requests.Session()
    session.headers.update(HTTP_HEADERS)
    raw = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10)
    response = HTMLResponse(raw)
    config_only_spain = config_factory(key="es", dialect="Spain | Castilian")
    config_only_la = config_factory(key="es", dialect="Latin America")
    config_any_dialect = config_factory(key="es")
    # Apply each config's XPath selector.
    results_only_spain = response.html.xpath(
        config_only_spain.pron_xpath_selector
    )
    results_only_la = response.html.xpath(config_only_la.pron_xpath_selector)
    results_any_dialect = response.html.xpath(
        config_any_dialect.pron_xpath_selector
    )
    assert (
        len(results_any_dialect)  # containing both all results
        > len(results_only_spain)  # containing only the Spain result
        == len(results_only_la)  # containing only the LA result
        > 0
    )


@pytest.mark.parametrize(
    "word, dialect, segment, expected_pron",
    [
        ("keratin", "US | General American", True, "ˈk ɛ ɹ ə t ɪ n"),
        ("keratin", "US | General American", False, "ˈkɛɹətɪn"),
        ("Likert", "UK | Received Pronunciation", True, "ˈl ɪ k . ə t"),
        ("Likert", "UK | Received Pronunciation", False, "ˈlɪk.ət"),
        ("minor", "US | General American", True, "ˈm a ɪ . n ɚ"),
        ("minor", "US | General American", False, "ˈmaɪ.nɚ"),
        ("nurture", "US | General American", True, "ˈn ɜː ɹ . t͡ʃ ɚ"),
        ("nurture", "US | General American", False, "ˈnɜːɹ.t͡ʃɚ"),
    ],
)
@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
def test_english_pron(word, dialect, segment, expected_pron):
    session = requests.Session()
    session.headers.update(HTTP_HEADERS)
    raw = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10)
    response = HTMLResponse(raw)
    config = config_factory(key="en", dialect=dialect, segment=segment)
    pairs = config.extract_word_pron(word, response, config)
    _, pron = next(pairs)
    assert pron == expected_pron


@pytest.mark.parametrize("parens", ["skip", "show", "expand"])
def test_parens_attribute(parens):
    config = config_factory(parens=parens)
    assert config.parens == parens


def test_parens_invalid():
    with pytest.raises(ValueError):
        config_factory(parens="invalid")


@pytest.mark.parametrize(
    "expected_language, keys",
    [
        # Languages that the iso639 package can directly handle.
        ("English", {"en", "eng", "English"}),
        ("Spanish", {"spa", "es"}),
        # Languages handled by our own _LANGUAGE_CODES dict.
        ("Greek", {"el", "ell", "gre", "Greek"}),
        ("Slovene", {"sl", "slv", "Slovene", "Slovenian"}),
        # For all Proto-X languages. X may contain hyphens in the middle.
        ("Proto-Germanic", {"Proto-Germanic", "proto-germanic"}),
        ("Proto-Balto-Slavic", {"Proto-Balto-Slavic", "proto-balto-slavic"}),
    ],
)
def test_language(expected_language, keys):
    for key in keys:
        config = config_factory(key=key)
        assert config.language == expected_language, f"key = {key}"
