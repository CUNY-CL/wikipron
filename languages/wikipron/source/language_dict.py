LANGUAGES = { 
  # ISO 639-1 "eu", ISO 639-2 "baq/eus"
  # 232 e
  "baq": {
    "iso639_name": "Basque",
    "wiktionary_name": "Basque",
    "casefold": True
  },
  # ISO 639-1 "kw"
  # 370 e
  # "cor": {
  #   "iso639_name": "Cornish",
  #   "wiktionary_name": "Cornish",
  #   "casefold": True
  # },
  # # # ISO 639-3 only.
  # # # 182 e
  # "dlm": {
  #   "iso639_name": "Dalmatian",
  #   "wiktionary_name": "Dalmatian",
  #   "casefold": True
  # }
}




# ISO 639-2 Code and English name obtained from the Library of Congress website: https://www.loc.gov/standards/iso639-2/php/code_list.php
# ISO 639-2 3 Char Code [str]: { 
#   "iso639_name": [str] ISO 639-2 Language Name(s),
#   "wiktionary_name": [str] English Wiktionary name (listed as Canonical name, ex. https://en.wiktionary.org/wiki/Category:Romanian_language),
#   "casefold": [bool]
# }

# Template:
  # "": {
  #   "iso639_name": "",
  #   "wiktionary_name": "",
  #   "casefold": False
  # }

# ISO 639-1 is listed in a comment if it is the language code listed by Wiktionary
# In case of multiple ISO 639-2 codes, I've selected the key as those designated B (bibliographic), but have included B and T (terminology) in a comment as B/T.
# ISO 639-3 Code used with Classical Nahuatl, Cantonese, and Serbo-Croatian
# LANGUAGES = {
#   "ady": {
#     "iso639_name": "Adygei; Adyghe",
#     "wiktionary_name": "Adyghe",
#     "casefold": True
#   },
#   # ISO 639-1 "sq", ISO 639-2 "alb/sqi"
#   "alb": {
#     "iso639_name": "Albanian",
#     "wiktionary_name": "Albanian",
#     "casefold": True
#   },
#   "grc": {
#     "iso639_name": "Greek, Ancient (to 1453)",
#     "wiktionary_name": "Ancient Greek",
#     "casefold": True
#   },
#  # ISO 639-1 code is "ar"
#   "ara": {
#     "iso639_name": "Arabic",
#     "wiktionary_name": "Arabic",
#     "casefold": False
#   }, 
#   "arc": {
#     "iso639_name": "Official Aramaic (700-300 BCE); Imperial Aramaic (700-300 BCE)",
#     "wiktionary_name": "Aramaic",
#     "casefold": False
#   },
#   # ISO 639-1 "hy", ISO 639-2 "arm/hye"
#   "arm": {
#     "iso639_name": "Armenian",
#     "wiktionary_name": "Armenian",
#     "casefold": True
#   },
#   # ISO 639-1 "as"
#   "asm": {
#     "iso639_name": "Assamese",
#     "wiktionary_name": "Assamese",
#     "casefold": False
#   },
#    # ISO 639-1 "az"
#   "aze": {
#     "iso639_name": "Azerbaijani",
#     "wiktionary_name": "Azerbaijani",
#     "casefold": True
#   },
#   # ISO 639-1 "ba"
#   "bak": {
#     "iso639_name": "Bashkir",
#     "wiktionary_name": "Bashkir",
#     "casefold": True
#   },
#   # ISO 639-1 "be"
#   "bel": {
#     "iso639_name": "Belarusian",
#     "wiktionary_name": "Belarusian",
#     "casefold": True
#   },
#   # ISO 639-1 "bg"
#   "bul": {
#     "iso639_name": "Bulgarian",
#     "wiktionary_name": "Bulgarian",
#     "casefold": True
#   },
#   # ISO 639-1 "my", ISO 639-2 "bur/mya"
#   "bur": {
#     "iso639_name": "Burmese",
#     "wiktionary_name": "Burmese",
#     "casefold": False
#   },
#   # ISO 639-3 only. (See comments above Chinese)
#   "yue": {
#     "iso639_name": "Yue Chinese	",
#     "wiktionary_name": "Cantonese",
#     "casefold": False
#   },
#   # ISO 639-1 "ca"
#   "cat": {
#     "iso639_name": "Catalan; Valencian",
#     "wiktionary_name": "Catalan",
#     "casefold": True
#   },
#   # ISO 639-1 "zh", ISO 639-2 "chi/zho"
#   # For info on how Cantonese and Mandarin are distinguished within ISO 639-2 see: http://www.loc.gov/standards/iso639-2/faq.html#24
#   "chi": {
#     "iso639_name": "Chinese",
#     "wiktionary_name": "Chinese",
#     "casefold": False
#   },
#   # ISO 639-3 only.
#   "nci": {
#     "iso639_name": "Classical Nahuatl",
#     "wiktionary_name": "Classical Nahuatl",
#     "casefold": True
#   },
#   "syc": {
#     "iso639_name": "Classical Syriac",
#     "wiktionary_name": "Classical Syriac",
#     "casefold": False
#   },
#   # ISO 639-1 "cs", ISO 639-2 "cze/ces"
#   "cze": {
#     "iso639_name": "Czech",
#     "wiktionary_name": "Czech",
#     "casefold": True
#   },
#   # ISO 639-1 "da"
#   "dan": {
#     "iso639_name": "Danish",
#     "wiktionary_name": "Danish",
#     "casefold": True
#   },
#   # ISO 639-1 "nl", ISO 639-2 "dut/nld"
#   "dut": {
#     "iso639_name": "Dutch; Flemish",
#     "wiktionary_name": "Dutch",
#     "casefold": True
#   },
#   "egy": {
#     "iso639_name": "Egyptian (Ancient)",
#     "wiktionary_name": "Egyptian",
#     # Bit of a guess on whether to apply casefolding. No entries on wiktionary appear to have casing anyway.
#     "casefold": False
#   },
#   # ISO 639-1 "en"
#   "eng": {
#     "iso639_name": "English",
#     "wiktionary_name": "English",
#     "casefold": True
#   },
#   # ISO 639-1 "eo"
#   "epo": {
#     "iso639_name": "Esperanto",
#     "wiktionary_name": "Esperanto",
#     "casefold": True
#   },
#   # ISO 639-1 "fo"
#   "fao": {
#     "iso639_name": "Faroese",
#     "wiktionary_name": "Faroese",
#     "casefold": True
#   },
#   # ISO 639-1 "fi"
#   "fin": {
#     "iso639_name": "Finnish",
#     "wiktionary_name": "Finnish",
#     "casefold": True
#   },
#   # ISO 639-1 "fr", ISO 639-2 "fre/fra"
#   "fre": {
#     "iso639_name": "French",
#     "wiktionary_name": "French",
#     "casefold": True
#   },
#   # ISO 639-1 "gl"
#   "glg": {
#     "iso639_name": "Galician",
#     "wiktionary_name": "Galician",
#     "casefold": True
#   },
#   # ISO 639-1 "ka", ISO 639-2 "geo/kat"
#   "geo": {
#     "iso639_name": "Georgian",
#     "wiktionary_name": "Georgian",
#     # From what I can tell, Mkhedruli - the current Georgian script - occasionally uses "Mtavruli" which is defined as having a capital-like effect. Mkhedruli is described as both unicase and bicameral.
#     # https://en.wikipedia.org/wiki/Georgian_language#Writing_system -- the section on Computing may be of interest should we run into problems.
#     # Asomtavruli letters are also used in several Wikitionary entries. (Unicameral, so shouldn't matter, but just something to note.)
#     "casefold": False
#   },
#   # ISO 639-1 "de", ISO 639-2 "ger/deu"
#   "ger": {
#     "iso639_name": "German",
#     "wiktionary_name": "German",
#     "casefold": True
#   },
#   # ISO 639-1 "el", ISO 639-2 "gre/ell"
#   "gre": {
#     "iso639_name": "Greek, Modern (1453-)",
#     "wiktionary_name": "Greek",
#     "casefold": True
#   },
#   # ISO 639-1 "hi"
#   "hin": {
#     "iso639_name": "Hindi",
#     "wiktionary_name": "Hindi",
#     "casefold": False
#   },
#   # ISO 639-1 "hu"
#   "hun": {
#     "iso639_name": "Hungarian",
#     "wiktionary_name": "Hungarian",
#     "casefold": True
#   },
#   # ISO 639-1 "is", ISO 639-2 "ice/isl"
#   "ice": {
#     "iso639_name": "Icelandic",
#     "wiktionary_name": "Icelandic",
#     "casefold": True
#   },
#   # ISO 639-1 "io"
#   "ido": {
#     "iso639_name": "Ido",
#     "wiktionary_name": "Ido",
#     "casefold": True
#   },
#   # ISO 639-1 "id"
#   "ind": {
#     "iso639_name": "Indonesian",
#     "wiktionary_name": "Indonesian",
#     "casefold": True
#   },
#   # ISO 639-1 "ga"
#   "gle": {
#     "iso639_name": "Irish",
#     "wiktionary_name": "Irish",
#     "casefold": True
#   },
#   # ISO 639-1 "it"
#   "ita": {
#     "iso639_name": "Italian",
#     "wiktionary_name": "Italian",
#     "casefold": True
#   },
#   # ISO 639-1 "ja"
#   "jpn": {
#     "iso639_name": "Japanese",
#     "wiktionary_name": "Japanese",
#     "casefold": False
#   }, 
#   # ISO 639-1 "km"
#   "khm": {
#     "iso639_name": "Central Khmer",
#     "wiktionary_name": "Khmer",
#     "casefold": False
#   },
#   # ISO 639-1 "ko"
#   "kor": {
#     "iso639_name": "Korean",
#     "wiktionary_name": "Korean",
#     "casefold": False
#   },
#   # ISO 639-1 "ku"
#   "kur": {
#     "iso639_name": "Kurdish",
#     "wiktionary_name": "Kurdish",
#     # Although the Sorani alphabet appears to be unicase.
#     "casefold": True
#   },
#   # ISO 639-1 "la"
#   "lat": {
#     "iso639_name": "Latin",
#     "wiktionary_name": "Latin",
#     "casefold": True
#   },
#   # ISO 639-1 "lv"
#   "lav": {
#     "iso639_name": "Latvian",
#     "wiktionary_name": "Latvian",
#     "casefold": True
#   },
#   # ISO 639-1 "lt"
#   "lit": {
#     "iso639_name": "Lithuanian",
#     "wiktionary_name": "Lithuanian",
#     "casefold": True
#   },
#   "dsb": {
#     "iso639_name": "Lower Sorbian",
#     "wiktionary_name": "Lower Sorbian",
#     "casefold": True
#   },
#   # ISO 639-1 "lb"
#   "ltz": {
#     "iso639_name": "Luxembourgish; Letzeburgesch",
#     "wiktionary_name": "Luxembourgish",
#     "casefold": True
#   },
#   # ISO 639-1 "mk", ISO 639-2 "mac/mkd"
#   "mac": {
#     "iso639_name": "Macedonian",
#     "wiktionary_name": "Macedonian",
#     "casefold": True
#   },
#   # ISO 639-1 "ms", ISO 639-2 "may/msa"
#   "may": {
#     "iso639_name": "Malay",
#     "wiktionary_name": "Malay",
#     # Assuming all entries are in Rumi, the Latin script. Jawi, an Arabic script also exists.
#     "casefold": True
#   },
#   # ISO 639-1 "mt"
#   "mlt": {
#     "iso639_name": "Maltese",
#     "wiktionary_name": "Maltese",
#     "casefold": True
#   },
#   "enm": {
#     "iso639_name": "English, Middle (1100-1500)",
#     "wiktionary_name": "Middle English",
#     "casefold": True
#   },
#   # ISO 639-1 "mn"
#   "mon": {
#     "iso639_name": "Mongolian	",
#     "wiktionary_name": "Mongolian",
#     # Assuming that all entries will be in Cyrillic script
#     "casefold": True
#   },
#   # ISO 639-1 "se"
#   "sme": {
#     "iso639_name": "Northern Sami",
#     "wiktionary_name": "Northern Sami",
#     "casefold": True
#   },
#   # ISO 639-1 "no"
#   "nor": {
#     "iso639_name": "Norwegian",
#     "wiktionary_name": "Norwegian",
#     "casefold": True
#   },
#   # ISO 639-1 "nb"
#   "nob": {
#     "iso639_name": "Bokmål, Norwegian; Norwegian Bokmål",
#     "wiktionary_name": "Norwegian Bokmål",
#     "casefold": True
#   },
#   # ISO 639-1 "nn"
#   "nno": {
#     "iso639_name": "Norwegian Nynorsk; Nynorsk, Norwegian",
#     "wiktionary_name": "Norwegian Nynorsk",
#     "casefold": True
#   },
#   "ang": {
#     "iso639_name": "English, Old (ca.450-1100)",
#     "wiktionary_name": "Old English",
#     "casefold": True
#   },
#   "sga": {
#     "iso639_name": "Irish, Old (to 900)",
#     "wiktionary_name": "Old Irish",
#     "casefold": True
#   },
#   # ISO 639-1 "fa", ISO 639-2 "per/fas"
#   "per": {
#     "iso639_name": "Persian",
#     "wiktionary_name": "Persian",
#     "casefold": False
#   },
#   # ISO 639-1 "pl"
#   "pol": {
#     "iso639_name": "Polish",
#     "wiktionary_name": "Polish",
#     "casefold": True
#   },
#   # ISO 639-1 "pt"
#   "por": {
#     "iso639_name": "Portuguese",
#     "wiktionary_name": "Portuguese",
#     "casefold": True
#   },
#   # ISO 639-1 "ro", ISO 639-2 "rum/ron"
#   "rum": {
#     "iso639_name": "Romanian; Moldavian; Moldovan",
#     "wiktionary_name": "Romanian",
#     "casefold": True
#   },
#   # ISO 639-1 "ru"
#   "rus": {
#     "iso639_name": "Russian",
#     "wiktionary_name": "Russian",
#     "casefold": True
#   },
#   # ISO 639-1 "sa"
#   "san": {
#     "iso639_name": "Sanskrit",
#     "wiktionary_name": "Sanskrit",
#     # Not sure here. There are too many potential scripts listed to check them all. 
#     "casefold": False
#   },
#   # ISO 639-1 "gd"
#   "gla": {
#     "iso639_name": "Gaelic; Scottish Gaelic",
#     "wiktionary_name": "Scottish Gaelic",
#     "casefold": True
#   },
#   # ISO 639-1 "sh" (listed as deprecated). ISO 639-2 Serbo-Croatian codes are deprecated as well. "hbs" is ISO 639-3 only. Bosnian, Croatian, Serbian and Montenegrin have their own ISO 639-2 codes
#   "hbs": {
#     "iso639_name": "Serbo-Croatian",
#     "wiktionary_name": "Serbo-Croatian",
#     "casefold": True
#   },
#   # ISO 639-1 "sk", ISO 639-2 "slo/slk"
#   "slo": {
#     "iso639_name": "Slovak",
#     "wiktionary_name": "Slovak",
#     "casefold": True
#   },
#   # ISO 639-1 "sl"
#   "slv": {
#     "iso639_name": "Slovenian",
#     "wiktionary_name": "Slovene",
#     "casefold": True
#   },
#   # ISO 639-1 "es"
#   "spa": {
#     "iso639_name": "Spanish; Castilian",
#     "wiktionary_name": "Spanish",
#     "casefold": True
#   },
#   # ISO 639-1 "sv"
#   "swe": {
#     "iso639_name": "Swedish",
#     "wiktionary_name": "Swedish",
#     "casefold": True
#   },
#   # ISO 639-1 "tl"
#   "tgl": {
#     "iso639_name": "Tagalog",
#     "wiktionary_name": "Tagalog",
#     "casefold": True
#   },
#   # ISO 639-1 "ta"
#   "tam": {
#     "iso639_name": "Tamil",
#     "wiktionary_name": "Tamil",
#     "casefold": False
#   },
#   # ISO 639-1 "th"
#   "tha": {
#     "iso639_name": "Thai",
#     "wiktionary_name": "Thai",
#     "casefold": False
#   },
#   # ISO 639-1 "tr"
#   "tur": {
#     "iso639_name": "Turkish",
#     "wiktionary_name": "Turkish",
#     "casefold": True
#   },
#   # ISO 639-1 "uk"
#   "ukr": {
#     "iso639_name": "Ukrainian",
#     "wiktionary_name": "Ukrainian",
#     "casefold": True
#   },
#   # ISO 639-1 "vi"
#   "vie": {
#     "iso639_name": "Vietnamese",
#     "wiktionary_name": "Vietnamese",
#     "casefold": True
#   },
#   # ISO 639-1 "cy", ISO 639-2 "wel/cym"
#   "wel": {
#     "iso639_name": "Welsh",
#     "wiktionary_name": "Welsh",
#     "casefold": True
#   },
#   # ISO 639-1 "zu"
#   "zul": {
#     "iso639_name": "Zulu",
#     "wiktionary_name": "Zulu",
#     "casefold": True
#   }

# }