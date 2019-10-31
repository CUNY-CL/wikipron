import pytest

from wikipron.scrape import scrape, _skip_word, _skip_date

from . import can_connect_to_wiktionary, config_factory


@pytest.mark.skipif(not can_connect_to_wiktionary(), reason="need Internet")
@pytest.mark.parametrize(
    "key, language, other_params",
    [
        ("eng", "English", {}),
        # Test that 'sup[a[@title = "wikipedia:Slovak phonology"]]' works.
        ("slk", "Slovak", {}),
        # Test that the extra "span" layer for Korean is handled.
        # Korean data is mostly phonetic transcription only.
        ("kor", "Korean", {"phonetic": True}),
    ],
)
@pytest.mark.timeout(3)
def test_scrape(key, language, other_params):
    """A smoke test for scrape()."""
    n = 10  # number of word-pron pairs to scrape
    config = config_factory(key=key, **other_params)
    assert config.language == language
    pairs = []
    for i, (word, pron) in enumerate(scrape(config)):
        if i >= n:
            break
        pairs.append((word, pron))
    assert len(pairs) == n
    assert all(word and pron for (word, pron) in pairs)


@pytest.mark.parametrize(
    "word, expected",
    [
        ("foobar", False),
        ("a phrase", True),
        ("hyphen-ated", True),
        ("prefix-", True),
        ("-suffix", True),
        ("hasdigit2", True),
    ],
)
def test__skip_word(word, expected):
    assert _skip_word(word) == expected


@pytest.mark.parametrize(
    "date_from_word, cut_off_date, expected",
    [
        ("2019-10-15", "2019-10-20", False),
        ("2019-10-20", "2019-10-20", False),
        ("2019-10-25", "2019-10-20", True),
    ],
)
def test__skip_date(date_from_word, cut_off_date, expected):
    assert _skip_date(date_from_word, cut_off_date) == expected
