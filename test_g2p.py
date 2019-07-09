import datetime
import os
import tempfile

import pytest

from g2p import _Config, _PHONEMES_REGEX, _PHONES_REGEX, _get_cli_args


_TODAY = datetime.date.today()

_DATE_TODAY = _TODAY.isoformat()
_DATE_FUTURE = (_TODAY + datetime.timedelta(days=10)).isoformat()
_DATE_RECENT_PAST = (_TODAY - datetime.timedelta(days=10)).isoformat()
_DATE_DISTANT_PAST = (_TODAY - datetime.timedelta(days=20)).isoformat()


class _CLIArgs:
    """A representation of CLI args with attributes and their default value."""

    # We need to provide a value to the only obligatory arg.
    language = "eng"

    # All other args have their own default value.
    phonetic = False
    no_stress = False
    no_syllable_boundaries = False
    dialect = None
    require_dialect_label = False
    casefold = False
    cut_off_date = None
    output = None


def _config_factory(**kwargs):
    """Create a _Config object for testing."""
    cli_args = _CLIArgs()
    for arg, value in kwargs.items():
        setattr(cli_args, arg, value)

    return _Config(cli_args)


def test_cli_args():
    actual_cli_args = _get_cli_args(["eng"])
    expected_cli_args = _CLIArgs()
    for expected_arg, expected_value in vars(expected_cli_args):
        assert getattr(actual_cli_args, expected_arg) == expected_value


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
    "phonetic, ipa_regex", [(True, _PHONES_REGEX), (False, _PHONEMES_REGEX)]
)
def test_ipa_regex(phonetic, ipa_regex):
    config = _config_factory(phonetic=phonetic)
    assert config.ipa_regex == ipa_regex


@pytest.mark.parametrize(
    "dialect, require_dialect_label, expected_li_selector",
    [
        (
            None,
            False,
            (
                "\n//li[\n"
                '  sup[a[@title = "Appendix:English pronunciation"]]\n'
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (true\n'
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "US",
            False,
            (
                "\n//li[\n"
                '  sup[a[@title = "Appendix:English pronunciation"]]\n'
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content"][text() = "US"]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "US",
            True,
            (
                "\n//li[\n"
                '  sup[a[@title = "Appendix:English pronunciation"]]\n'
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content"][text() = "US"])\n'  # noqa: E501
                "]\n"
            ),
        ),
        (
            "General American | US",
            False,
            (
                "\n//li[\n"
                '  sup[a[@title = "Appendix:English pronunciation"]]\n'
                "  and\n"
                '  span[@class = "IPA"]\n'
                "  and\n"
                '  (span[@class = "ib-content qualifier-content"][text() = "General American" or text() = "US"]\n'  # noqa: E501
                '   or count(span[@class = "ib-content qualifier-content"]) = 0)\n'  # noqa: E501
                "]\n"
            ),
        ),
    ],
)
def test_li_selector(dialect, require_dialect_label, expected_li_selector):
    config = _config_factory(
        language="English",
        dialect=dialect,
        require_dialect_label=require_dialect_label,
    )
    assert config.li_selector == expected_li_selector
