from wikipron.extract.blt import extract_word_pron_blt
from wikipron.extract.cmn import extract_word_pron_cmn
from wikipron.extract.jpn import extract_word_pron_jpn
from wikipron.extract.khb import extract_word_pron_lu
from wikipron.extract.khm import extract_word_pron_khmer
from wikipron.extract.lat import extract_word_pron_latin
from wikipron.extract.nan import extract_word_pron_nan
from wikipron.extract.shn import extract_word_pron_shan
from wikipron.extract.tha import extract_word_pron_thai
from wikipron.extract.vie import extract_word_pron_vie
from wikipron.extract.yue import extract_word_pron_yue


# All extraction functions must have the exact same function signature.
# The key has to be the language name used by Wiktionary.
EXTRACTION_FUNCTIONS = {
    "Cantonese": extract_word_pron_yue,
    "Chinese": extract_word_pron_cmn,
    "Japanese": extract_word_pron_jpn,
    "Khmer": extract_word_pron_khmer,
    "Latin": extract_word_pron_latin,
    "Lü": extract_word_pron_lu,
    "Min Nan": extract_word_pron_nan,
    "Shan": extract_word_pron_shan,
    "Tai Dam": extract_word_pron_blt,
    "Thai": extract_word_pron_thai,
    "Vietnamese": extract_word_pron_vie,
}
