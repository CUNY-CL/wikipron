from wikipron.extract.default import extract_word_pron_default
from wikipron.extract.lat import extract_word_pron_lat


EXTRACTION_FUNCTIONS = {
    "default": extract_word_pron_default,
    # Key has to be the language name used by Wiktionary.
    "Latin": extract_word_pron_lat,
}
