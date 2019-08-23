import pytest

from wikipron.scrape import scrape

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
