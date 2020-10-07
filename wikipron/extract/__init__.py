from wikipron.extract.cmn import extract_word_pron_cmn
from wikipron.extract.jpn import extract_word_pron_jpn
from wikipron.extract.khb import extract_word_pron_lu
from wikipron.extract.khm import extract_word_pron_khmer
from wikipron.extract.lat import extract_word_pron_latin
from wikipron.extract.tha import extract_word_pron_thai
from wikipron.extract.vie import extract_word_pron_vie


# All extraction functions must have the exact same function signature.
# The key has to be the language name used by Wiktionary.
EXTRACTION_FUNCTIONS = {
    "Chinese": extract_word_pron_cmn,
    "Japanese": extract_word_pron_jpn,
    "Khmer": extract_word_pron_khmer,
    "Latin": extract_word_pron_latin,
    "Lü": extract_word_pron_lu,
    "Thai": extract_word_pron_thai,
    "Vietnamese": extract_word_pron_vie,
}
