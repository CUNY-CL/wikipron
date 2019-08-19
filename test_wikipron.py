import datetime
import inspect
import os
import re
import shutil
import tempfile

import pytest
import requests
import requests_html

from wikipron import (
    __doc__,
    Config,
    _PAGE_TEMPLATE,
    _PHONEMES_REGEX,
    _PHONES_REGEX,
    _get_cli_args,
    scrape,
)


_TERMINAL_COMMAND = "wikipron"

_TODAY = datetime.date.today()
_DATE_TODAY = _TODAY.isoformat()
_DATE_FUTURE = (_TODAY + datetime.timedelta(days=10)).isoformat()
_DATE_RECENT_PAST = (_TODAY - datetime.timedelta(days=10)).isoformat()
_DATE_DISTANT_PAST = (_TODAY - datetime.timedelta(days=20)).isoformat()


def _config_factory(**kwargs) -> Config:
    """Create a Config object for testing."""
    config_dict = {"key": "eng"}  # The one default; may be overridden.
    config_dict.update(**kwargs)
    return Config(**config_dict)


def test_output():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "foobar.tsv")
        config = _config_factory(output=file_path)
        assert config.output.name == file_path


@pytest.mark.parametrize(
    "casefold, input_word, expected_word",
    [(True, "FooBar", "foobar"), (False, "FooBar", "FooBar")],
)
def test_casefold(casefold, input_word, expected_word):
    config = _config_factory(casefold=casefold)
    assert config.casefold(input_word) == expected_word


@pytest.mark.parametrize(
    "no_stress, no_syllable_boundaries, expected_pron",
    [
        (True, True, "lɪŋɡwɪstɪks"),
        (True, False, "lɪŋ.ɡwɪs.tɪks"),
        (False, True, "lɪŋˈɡwɪstɪks"),
        (False, False, "lɪŋ.ˈɡwɪs.tɪks"),
    ],
)
def test_process_pron(no_stress, no_syllable_boundaries, expected_pron):
    config = _config_factory(
        no_stress=no_stress, no_syllable_boundaries=no_syllable_boundaries
    )
    assert config.process_pron("lɪŋ.ˈɡwɪs.tɪks") == expected_pron


@pytest.mark.parametrize(
    "error, cut_off_date, word_available_date, source_word, expected_word",
    [
        # Input cut_off_date is invalid.
        (True, _DATE_FUTURE, None, None, None),
        (True, "not-a-valid_date", None, None, None),
        # Input cut_off_date is valid.
        (False, None, _DATE_RECENT_PAST, "foobar", "foobar"),
        (False, _DATE_TODAY, _DATE_TODAY, "foobar", "foobar"),
        (False, _DATE_TODAY, _DATE_RECENT_PAST, "foobar", "foobar"),
        (False, _DATE_RECENT_PAST, _DATE_DISTANT_PAST, "foobar", "foobar"),
        (False, _DATE_RECENT_PAST, _DATE_TODAY, "foobar", None),
        # Now check that filtering works due to the word itself.
        (False, None, _DATE_RECENT_PAST, "a phrase", None),
        (False, None, _DATE_RECENT_PAST, "hyphen-ated", None),
        (False, None, _DATE_RECENT_PAST, "prefix-", None),
        (False, None, _DATE_RECENT_PAST, "-suffix", None),
        (False, None, _DATE_RECENT_PAST, "hasdigit2", None),
    ],
)
def test_process_word(
    error, cut_off_date, word_available_date, source_word, expected_word
):
    if error:
        with pytest.raises(ValueError):
            _config_factory(cut_off_date=cut_off_date)
    else:
        config = _config_factory(cut_off_date=cut_off_date)
        assert (
            config.process_word(source_word, word_available_date)
            == expected_word
        )


@pytest.mark.parametrize(
    "phonetic, ipa_regex, word_in_ipa",
    [(True, _PHONES_REGEX, "[foobar]"), (False, _PHONEMES_REGEX, "/foobar/")],
)
def test_ipa_regex(phonetic, ipa_regex, word_in_ipa):
    config = _config_factory(phonetic=phonetic)
    # Make sure we use the correct regex depending on phonetic vs phonemic.
    assert config.ipa_regex == ipa_regex
    # Make sure the IPA extraction by regex works.
    assert re.search(ipa_regex, word_in_ipa).group(1) == "foobar"


@pytest.mark.parametrize(
    "dialect, require_dialect_label, expected_li_selector",
    [
        (
            None,
            False,
            (
                "\n//li[\n"
                "  sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                "  (true()\n"
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "US",
            False,
            (
                "\n//li[\n"
                "  sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content" and a[text() = "US"]]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "US",
            True,
            (
                "\n//li[\n"
                "  sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content" and a[text() = "US"]])\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "General American | US",
            False,
            (
                "\n//li[\n"
                "  sup[a[\n"
                '    @title = "Appendix:English pronunciation"\n'
                "    or\n"
                '    @title = "wikipedia:English phonology"\n'
                "  ]]\n"
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content" and a[text() = "General American" or text() = "US"]]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
    ],
)
def test_li_selector(dialect, require_dialect_label, expected_li_selector):
    config = _config_factory(
        key="en", dialect=dialect, require_dialect_label=require_dialect_label
    )
    assert config.li_selector == expected_li_selector


def _can_connect_to_wiktionary():
    try:
        requests.get("https://en.wiktionary.org/wiki/linguistics")
    except (requests.ConnectionError, requests.ConnectTimeout):
        return False
    else:
        return True


@pytest.mark.skipif(not _can_connect_to_wiktionary(), reason="need Internet")
def test_american_english_dialect_selection():
    # Pick a word for which Wiktionary has dialect-specified pronunciations
    # for both US and non-US English.
    word = "mocha"
    html_session = requests_html.HTMLSession()
    response = html_session.get(_PAGE_TEMPLATE.format(word=word))
    # Construct two configs to demonstrate the US dialect (non-)selection.
    config_only_us = _config_factory(key="en", dialect="US | American English")
    config_any_dialect = _config_factory(key="en")
    # Apply each config's XPath selector.
    results_only_us = response.html.xpath(config_only_us.li_selector)
    results_any_dialect = response.html.xpath(config_any_dialect.li_selector)
    assert (
        len(results_any_dialect)  # containing both US and non-US results
        > len(results_only_us)  # containing only the US result
        > 0
    )


@pytest.mark.skipif(not _can_connect_to_wiktionary(), reason="need Internet")
def test_require_dialect_label():
    # Pick a word for which Wiktionary doesn't specify the dialect at all.
    word = "examine"
    html_session = requests_html.HTMLSession()
    response = html_session.get(_PAGE_TEMPLATE.format(word=word))
    # Construct two configs to test the "require_dialect_label" param.
    config_params = dict(key="en", dialect="US | American English")
    config_dialect_optional = _config_factory(**config_params)
    config_dialect_required = _config_factory(
        **config_params, require_dialect_label=True
    )
    # Apply each config's XPath selector.
    results_dialect_optional = response.html.xpath(
        config_dialect_optional.li_selector
    )
    results_dialect_required = response.html.xpath(
        config_dialect_required.li_selector
    )
    assert len(results_dialect_optional) > len(results_dialect_required) == 0


@pytest.mark.skipif(not _can_connect_to_wiktionary(), reason="need Internet")
@pytest.mark.parametrize(
    "key, language",
    [
        ("eng", "English"),
        # Test that 'sup[a[@title = "wikipedia:Slovak phonology"]]' works.
        ("slk", "Slovak"),
    ],
)
@pytest.mark.timeout(2)
def test_scrape(key, language):
    """A smoke test for scrape()."""
    n = 10  # number of word-pron pairs to scrape
    config = _config_factory(key=key)
    assert config.language == language
    pairs = []
    for i, (word, pron) in enumerate(scrape(config)):
        if i >= n:
            break
        pairs.append((word, pron))
    assert len(pairs) == n
    assert all(word and pron for (word, pron) in pairs)


@pytest.mark.parametrize(
    "expected_language, keys",
    [
        # Languages that the iso639 package can directly handle.
        ("English", {"en", "eng", "english", "English"}),
        ("Spanish", {"spa", "es"}),
        # Languages handled by our own _LANGUAGE_CODES dict.
        ("Greek", {"el", "ell", "gre", "Greek"}),
        ("Slovene", {"sl", "slv", "Slovene", "Slovenian"}),
    ],
)
def test_language(expected_language, keys):
    for key in keys:
        config = _config_factory(key=key)
        assert config.language == expected_language, f"key = {key}"


def test_terminal_command():
    assert shutil.which(_TERMINAL_COMMAND), (
        f'The terminal command "{_TERMINAL_COMMAND}" does not exist. '
        "Is the package not installed correctly? "
        f'Or is the command "{_TERMINAL_COMMAND}" not defined in setup.py?'
    )
    smoke_test_command = f"{_TERMINAL_COMMAND} --help"
    help_manual = os.popen(smoke_test_command).read()
    assert __doc__ in help_manual, (
        f'The command "{_TERMINAL_COMMAND}" exists but does not work. '
        f'The smoke test with "{smoke_test_command}" may have diagnostic '
        "information to stderr."
    )


def test_cli_args_match_config_args():
    config_args = inspect.getfullargspec(Config.__init__)
    cli_args = _get_cli_args(["eng"])
    assert cli_args.__dict__ == {**config_args.kwonlydefaults, "key": "eng"}, (
        "CLI and Config.__init__ must have the same args and their defaults."
    )
