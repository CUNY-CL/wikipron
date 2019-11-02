from wikipron.extract.default import extract_word_pron_default
from wikipron.extract.khm import extract_word_pron_khm


EXTRACTION_FUNCTIONS = {
    "default": extract_word_pron_default,
    # Key has to be the language name used by Wiktionary.
    "Khmer": extract_word_pron_khm,
}
