from wikipron.extract.blt import extract_word_pron_blt
from wikipron.extract.eng import extract_word_pron_eng
from wikipron.extract.jpn import extract_word_pron_jpn
from wikipron.extract.khb import extract_word_pron_lu
from wikipron.extract.khm import extract_word_pron_khmer
from wikipron.extract.lat import extract_word_pron_latin
from wikipron.extract.shn import extract_word_pron_shan
from wikipron.extract.tha import extract_word_pron_thai
from wikipron.extract.vie import extract_word_pron_vie
from wikipron.extract.zho import extract_word_pron_zho

# All extraction functions must have the exact same function signature.
# The key has to be the language name used by Wiktionary.
EXTRACTION_FUNCTIONS = {
    # Chinese varieties: shared dispatch in zho.py keyed off
    # config.language. One walk over Category:Chinese terms with IPA
    # pronunciation feeds every variety's TSV.
    "Cantonese": extract_word_pron_zho,
    "Eastern Min": extract_word_pron_zho,
    "Gan": extract_word_pron_zho,
    "Hakka": extract_word_pron_zho,
    "Jin": extract_word_pron_zho,
    "Leizhou Min": extract_word_pron_zho,
    "Mandarin": extract_word_pron_zho,
    "Middle Chinese": extract_word_pron_zho,
    "Min Nan": extract_word_pron_zho,
    "Northern Min": extract_word_pron_zho,
    "Old Chinese": extract_word_pron_zho,
    "Puxian Min": extract_word_pron_zho,
    "Southern Pinghua": extract_word_pron_zho,
    "Wu": extract_word_pron_zho,
    "Xiang": extract_word_pron_zho,
    # Other languages.
    "English": extract_word_pron_eng,
    "Japanese": extract_word_pron_jpn,
    "Khmer": extract_word_pron_khmer,
    "Latin": extract_word_pron_latin,
    "Lü": extract_word_pron_lu,
    "Shan": extract_word_pron_shan,
    "Tai Dam": extract_word_pron_blt,
    "Thai": extract_word_pron_thai,
    "Vietnamese": extract_word_pron_vie,
}
