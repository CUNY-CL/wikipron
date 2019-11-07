from wikipron.extract.default import extract_word_pron_default
from wikipron.extract.khm import extract_word_pron_khmer
from wikipron.extract.lat import extract_word_pron_latin


# All extraction functions must have the exact same function signature.
EXTRACTION_FUNCTIONS = {
    "default": extract_word_pron_default,
    # Key has to be the language name used by Wiktionary.
    "Khmer": extract_word_pron_khmer,
    "Latin": extract_word_pron_latin,
}
