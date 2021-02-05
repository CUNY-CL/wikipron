# This is a map from an ISO 639 code or common name to its Wiktionary language name.  # noqa: E501
# Note that the iso639 Python package that WikiPron uses can handle only ISO 639-1 and 639-2 codes.  # noqa: E501
# ISO 639-3: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab  # noqa: E501
# Wiktionary: https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language  # noqa: E501
# TODO: Expand this as needed to cover additional languages.
LANGUAGE_CODES = {
    # Greek. Would be "Greek, Modern (1453-)" in ISO 639.
    "el": "Greek",
    "ell": "Greek",
    "gre": "Greek",
    "greek": "Greek",
    "modern greek": "Greek",
    # Slovene. Would be "Slovenian" in ISO 639.
    "sl": "Slovene",
    "slv": "Slovene",
    "slovene": "Slovene",
    "slovenian": "Slovene",
    # Ancient Greek. Would be "Greek, Ancient (to 1453)" in ISO 639.
    "grc": "Ancient Greek",
    "ancient greek": "Ancient Greek",
    # Aramaic. Would be "Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)" in ISO 639.  # noqa: E501
    "arc": "Aramaic",
    "aramaic": "Aramaic",
    # Cantonese. ISO 639-3 only.
    "yue": "Cantonese",
    "cantonese": "Cantonese",
    # Classical Nahuatl. ISO 639-3 only.
    "nci": "Classical Nahuatl",
    "nahuatl": "Classical Nahuatl",
    "classical nahuatl": "Classical Nahuatl",
    "aztec": "Classical Nahuatl",
    # Egyptian. Would be "Egyptian (Ancient)" in ISO 639.
    "egy": "Egyptian",
    "egyptian": "Egyptian",
    "ancient egyptian": "Egyptian",
    # Khmer. Would be "Central Khmer" by the iso639 package.
    "khm": "Khmer",
    "khmer": "Khmer",
    "central khmer": "Khmer",
    # Middle English. Would be "English, Middle (1100-1500)" in ISO 639.
    "enm": "Middle English",
    "middle english": "Middle English",
    # Norwegian Bokmål. Would be "Bokmål, Norwegian" by the iso639 package.
    "nob": "Norwegian Bokmål",
    "norwegian bokmål": "Norwegian Bokmål",
    # Old English. Would be "English, Old (ca. 450-1100)" in ISO 639.
    "ang": "Old English",
    "old english": "Old English",
    # Old Irish. Would be "Irish, Old (to 900)" in ISO 639.
    "sga": "Old Irish",
    "old irish": "Old Irish",
    # Serbo-Croatian. ISO 639-3 only.
    "hbs": "Serbo-Croatian",
    "serbo-croatian": "Serbo-Croatian",
    # Alemannic German. Would be "Alemannic, Alsatian, Swiss German" in ISO 639.  # noqa: E501
    "gsw": "Alemannic German",
    "alemannic german": "Alemannic German",
    "swiss german": "Alemannic German",
    "alsatian german": "Alemannic German",
    "alsatian": "Alemannic German",
    # Alutor. ISO 639-3 only.
    "alr": "Alutor",
    "alutor": "Alutor",
    "alyutor": "Alutor",
    # Carrier. ISO 639-3 only.
    "crx": "Carrier",
    "carrier": "Carrier",
    # Central Franconian. Not an ISO 639 language.
    "central franconian": "Central Franconian",
    # Dalmatian. ISO 639-3 only.
    "dlm": "Dalmatian",
    "dalmatian": "Dalmatian",
    "dalmatic": "Dalmatian",
    # Dongxiang. ISO 639-3 only.
    "sce": "Dongxiang",
    "dongxiang": "Dongxiang",
    # Egyptian Arabic. ISO 639-3 only.
    "arz": "Egyptian Arabic",
    "egyptian arabic": "Egyptian Arabic",
    # Gamilaraay. ISO 639-3 only.
    "kld": "Gamilaraay",
    "gamilaraay": "Gamilaraay",
    "kamilaroi": "Gamilaraay",
    # German Low German. Not an ISO 639 language.
    "german low german": "German Low German",
    # Gulf Arabic. ISO 639-3 only.
    "afb": "Gulf Arabic",
    "gulf arabic": "Gulf Arabic",
    # Hadza. ISO 639-3 only.
    "hts": "Hadza",
    "hadza": "Hadza",
    # Hijazi Arabic. ISO 639-3 only.
    "acw": "Hijazi Arabic",
    "hijazi arabic": "Hijazi Arabic",
    # Hunsrik. ISO 639-3 only.
    "hrx": "Hunsrik",
    "hunsrik": "Hunsrik",
    # Interlingua. Would be "Interlingua (International Auxiliary Language Association)" in ISO 639.  # noqa: E501
    "ina": "Interlingua",
    "interlingua": "Interlingua",
    # K'iche'. ISO 639-3 only.
    "quc": "K'iche'",
    "k'iche'": "K'iche'",
    "quiché": "K'iche'",
    # Libyan Arabic. ISO 639-3 only.
    "ayl": "Libyan Arabic",
    "libyan arabic": "Libyan Arabic",
    # Ligurian. ISO 639-3 only.
    "lij": "Ligurian",
    "ligurian": "Ligurian",
    # Limburgish. Would be "Limburgan, Limburger, Limburgish" in ISO 639.
    "lim": "Limburgish",
    "limburgish": "Limburgish",
    "limburgan": "Limburgish",
    "limburger": "Limburgish",
    "limburgic": "Limburgish",
    # Livonian. Would be "Liv" in ISO 639.
    "liv": "Livonian",
    "livonian": "Livonian",
    # Lü. ISO 639-3 only.
    "khb": "Lü",
    "lü": "Lü",
    # Mauritian Creole. Would be "Morisyen" in ISO 639.
    "mfe": "Mauritian Creole",
    "mauritian creole": "Mauritian Creole",
    "morisyen": "Mauritian Creole",
    "morisien": "Mauritian Creole",
    # Middle Dutch. Would be "Middle Dutch (ca. 1050-1350)" in ISO 639.
    "dum": "Middle Dutch",
    "middle dutch": "Middle Dutch",
    # Middle Low German. ISO 639-3 only.
    "gml": "Middle Low German",
    "middle low german": "Middle Low German",
    # Middle Welsh. ISO 639-3 only.
    "wlm": "Middle Welsh",
    "middle welsh": "Middle Welsh",
    # Min Nan. ISO 639-3 only.
    "nan": "Min Nan",
    "min nan": "Min Nan",
    # Mon. ISO 639-3 only.
    "mnw": "Mon",
    # North Frisian. Would be "Northern Frisian" in ISO 639.
    "frr": "North Frisian",
    "north frisian": "North Frisian",
    # Occitan. Would be "Occitan (post 1500)" in ISO 639.
    "oci": "Occitan",
    "occitan": "Occitan",
    # Old French. Would be "Old French (842-ca. 1400)" in ISO 639.
    "fro": "Old French",
    "old french": "Old French",
    # Old High German. Would be "Old High German (ca. 750-1050)" in ISO 639.
    "goh": "Old High German",
    "old high german": "Old High German",
    # Old Norse. Would be "Norse, Old" by the iso639 package.
    "non": "Old Norse",
    "old norse": "Old Norse",
    # Old Portuguese. Not an ISO 639 language.
    "old portuguese": "Old Portuguese",
    "roa-opt": "Old Portuguese",
    "opt": "Old Portuguese",
    # Old Saxon. ISO 639-3 only.
    "osx": "Old Saxon",
    "old saxon": "Old Saxon",
    # Old Spanish. ISO 639-3 only.
    "osp": "Old Spanish",
    "old spanish": "Old Spanish",
    # Old Tupi. Not an ISO 639 language.
    "tpw": "Old Tupi",
    "old tupi": "Old Tupi",
    "classical tupi": "Old Tupi",
    # Pashto. Would be "Pashto, Pushto" in ISO 639.
    "pus": "Pashto",
    "pashto": "Pashto",
    "pushto": "Pashto",
    # Piedmontese. ISO 639-3 only.
    "pms": "Piedmontese",
    "piedmontese": "Piedmontese",
    # Pipil. ISO 639-3 only.
    "ppl": "Pipil",
    "pipil": "Pipil",
    "nawat": "Pipil",
    "nicarao": "Pipil",
    # Pitjantjatjara. ISO 639-3 only.
    "pjt": "Pitjantjatjara",
    "pitjantjatjara": "Pitjantjatjara",
    # Punjabi. Would be "Panjabi, Punjabi" in ISO 639.
    "pan": "Punjabi",
    "panjabi": "Punjabi",
    "punjabi": "Punjabi",
    # Scanian. Not an ISO 639 language.
    "scanian": "Scanian",
    # Scottish Gaelic. Would be "Gaelic, Scottish Gaelic" in ISO 639.
    "gla": "Scottish Gaelic",
    "scottish gaelic": "Scottish Gaelic",
    "gaelic": "Scottish Gaelic",
    # Sylheti. ISO 639-3 only.
    "syl": "Sylheti",
    "sylheti": "Sylheti",
    # Taos. Would be "Northern Tiwa" in ISO 639.
    "twf": "Taos",
    "taos": "Taos",
    "northern tiwa": "Taos",
    # Tongan. Would be "Tonga (Tonga Islands)" in ISO 639.
    "ton": "Tongan",
    "tongan": "Tongan",
    "tonga": "Tongan",
    # Tzotzil. ISO 639-3 only.
    "tzo": "Tzotzil",
    "tzotzil": "Tzotzil",
    # Uyghur. Would be "Uighur, Uyghur" in ISO 639.
    "uig": "Uyghur",
    "uighur": "Uyghur",
    "uyghur": "Uyghur",
    # Wauja. Would be "Waurá" in ISO 639.
    "wau": "Wauja",
    "waurá": "Wauja",
    "wauja": "Wauja",
    # West Frisian. Would be "Western Frisian" in ISO 639.
    "fry": "West Frisian",
    "west frisian": "West Frisian",
    "western frisian": "West Frisian",
    # Western Apache. ISO 639-3 only.
    "apw": "Western Apache",
    "western apache": "Western Apache",
    # Westrobothnian. Not an ISO 639 language.
    "westrobothnian": "Westrobothnian",
    # White Hmong. Would be "Hmong Daw" in ISO 639.
    "mww": "White Hmong",
    "white hmong": "White Hmong",
    # Zazaki. Would be "Dimili, Dimli (macrolanguage), Kirdki, Kirmanjki (macrolanguage), Zaza, Zazaki" in ISO 639.  # noqa: E501
    "zza": "Zazaki",
    "zazaki": "Zazaki",
    "zaza": "Zazaki",
    "dimili": "Zazaki",
    "dimli": "Zazaki",
    "kirdki": "Zazaki",
    "kirmanjki": "Zazaki",
    # Okinawan. ISO 639-3 only.
    "ryu": "Okinawan",
    "okinawan": "Okinawan",
    "central okinawan": "Okinawan",
    # Ottoman Turkish. Would be "Ottoman Turkish (1500-1928)" in ISO 639.
    "ota": "Ottoman Turkish",
    "ottoman turkish": "Ottoman Turkish",
    # Brunei Malay. Would be "Brunei" in ISO 639. ISO 693-3 only.
    "kxd": "Brunei Malay",
    "brunei malay": "Brunei Malay",
    # Mecayapan Nahuatl.
    # Would be "Isthmus-Mecayapan Nahuatl" in ISO 639. ISO 693-3 only.
    "nhx": "Mecayapan Nahuatl",
    "mecayapan nahuatl": "Mecayapan Nahuatl",
    # Tetelcingo Nahuatl. ISO 639-3 only.
    "nhg": "Tetelcingo Nahuatl",
    "tetelcingo nahuatl": "Tetelcingo Nahuatl",
    # Bouyei. ISO 639-3 only.
    "pcc": "Bouyei",
    "bouyei": "Bouyei",
    # Lamboya. ISO 639-3 only.
    "lmy": "Laboya",
    "laboya": "Laboya",
    # Moroccan Arabic. ISO 639-3 only.
    "ary": "Moroccan Arabic",
    "moroccan arabic": "Moroccan Arabic",
    # Mandarin Chinese. ISO 639-3 only.
    "cmn": "Chinese",
    "chinese": "Chinese",
    # Abkhaz. Would be Abkhazian in ISO 639.
    "abk": "Abkhaz",
    "abkhaz": "Abkhaz",
    # Avar. Would be Avaric in ISO 639.
    "ava": "Avar",
    "avar": "Avar",
    # Buryat. Would be Buriat in ISO 639.
    "bua": "Buryat",
    "buryat": "Buryat",
    # Chukchi. Would be Chukot in ISO 639.
    "ckt": "Chukchi",
    "chukchi": "Chukchi",
    # Burushaski. ISO 639-3 only.
    "bsk": "Burushaski",
    "burushaski": "Burushaski",
    # Evenki. Not in iso639 lib.
    "evn": "Evenki",
    "evenki": "Evenki",
    # Southern Yukaghir. Not in iso639 lib.
    "yux": "Southern Yukaghir",
    "southern yukaghir": "Southern Yukaghir",
    # Tundra Nenets. Not in iso639 lib.
    "yrk": "Tundra Nenets",
    "tundra nenets": "Tundra Nenets",
    # Estonian. Not in iso639 lib.
    "ekk": "Estonian",
    "estonian": "Estonian",
    # Livvi. Not in iso639 lib.
    "olo": "Livvi",
    "livvi": "Livvi",
    # Kildin Sami. Not in iso639 lib.
    "sjd": "Kildin Sami",
    "kildin sami": "Kildin Sami",
    # Northern Yukaghir. Not in iso639 lib.
    "ykg": "Northern Yukaghir",
    "northern yukaghir": "Northern Yukaghir",
    # Nanai. Not in iso639 lib.
    "gld": "Nanai",
    "nanai": "Nanai",
    # Greenlandic. Would be Kalaallisut in ISO 639.
    "kal": "Greenlandic",
    "greenlandic": "Greenlandic",
    # Khanty. Not in iso639 lib.
    "kca": "Khanty",
    "khanty": "Khanty",
    # Ket. Not in iso639 lib.
    "ket": "Ket",
    # Komi-Permyak. Not in iso639 lib.
    "koi": "Komi-Permyak",
    "komi-permyak": "Komi-Permyak",
    # Komi-Zyrian. Not in iso639 lib.
    "kpv": "Komi-Zyrian",
    "komi-zyrian": "Komi-Zyrian",
    # Lak. Not in iso639 lib.
    "lbe": "Lak",
    "lak": "Lak",
    # Lezgi. Would be Lezghian in ISO 639.
    "lez": "Lezgi",
    "lezgi": "Lezgi",
    # Eastern Mari. Not in iso639 lib.
    "mhr": "Eastern Mari",
    "eastern mari": "Eastern Mari",
    # Mansi. Not in iso639 lib.
    "mns": "Mansi",
    "mansi": "Mansi",
    # Nganasan. Not in iso639 lib.
    "nio": "Nganasan",
    "nganasan": "Nganasan",
    # Nivkh. Not in iso639 lib.
    "niv": "Nivkh",
    "nivkh": "Nivkh",
    # Polabian. Note: The code is "sla" in ISO 639-2.
    "pox": "Polabian",
    "polabian": "Polabian",
    # Bahnar. Not in iso639 lib.
    "bdq": "Bahnar",
    "bahnar": "Bahnar",
    # Jeju or Jejueo. Not in iso639 lib.
    "jje": "Jeju",
    "jeju": "Jeju",
    "jejueo": "Jeju",
    # Lashi. Not in iso639 lib.
    "lsi": "Lashi",
    "lashi": "Lashi",
    # Miyako. Not in iso639 lib.
    "mvi": "Miyako",
    "miyako": "Miyako",
    # Pennsylvania German. Not in iso639 lib.
    "pdc": "Pennsylvania German",
    "pennsylvania german": "Pennsylvania German",
    # Namuyi. Not in iso639 lib.
    "nmy": "Namuyi",
    "namuyi": "Namuyi",
    # Tuvan. Would be "Tuvinian" in ISO 639.
    "tyv": "Tuvan",
    "tuvan": "Tuvan",
    # Bikol Central. Would be "Central Bikol" in ISO 639.
    "bcl": "Bikol Central",
    "bikol central": "Bikol Central",
    # Emilian. ISO 639-3 only.
    "egl": "Emilian",
    "emilian": "Emilian",
    # Ingrian. ISO 639-3 only.
    "izh": "Ingrian",
    "ingrian": "Ingrian",
    # Latgalian. ISO 639-3 only.
    "ltg": "Latgalian",
    "latgalian": "Latgalian",
    # San Pedro Amuzgos Amuzgo. ISO 639-3 only.
    "azg": "San Pedro Amuzgos Amuzgo",
    "san pedro amuzgos amuzgo": "San Pedro Amuzgos Amuzgo",
    # Kyrgyz. Would be "Kirghiz" in ISO 639.
    "kir": "Kyrgyz",
    "kyrgyz": "Kyrgyz",
    # Middle Irish. Would be "Irish, Middle (900-1200)" in ISO 639.
    "mga": "Middle Irish",
    "middle irish": "Middle Irish",
    # Middle Korean. ISO 639-3 only: "Korean, Middle (10th–16th centuries)".
    "okm": "Middle Korean",
    "middle korean": "Middle Korean",
    # Northern Kurdish. Looks ISO 639-3 only.
    "kmr": "Northern Kurdish",
    "northern kurdish": "Northern Kurdish",
    "kurmanji": "Northern Kurdish",
    "dng": "Dungan",  # ISO 639-3.
    "ofs": "Old Frisian",  # ISO 639-3.
    # Ilocano. "ilo" resolved to "Iloko" by iso639 lib.
    "ilo": "Ilocano",
    "iloko": "Ilocano",
    "ilocano": "Ilocano",
    # Jamaican Creole. ISO 639-3 only.
    "jam": "Jamaican Creole",
    "jamaican creole": "Jamaican Creole",
    # Limbu. ISO 639-3 only.
    "lif": "Limbu",
    "limbu": "Limbu",
    # Lombard. ISO 639-3 only.
    "lmo": "Lombard",
    "lombard": "Lombard",
    # Murui Huitoto. ISO 639-3 only.
    "huu": "Murui Huitoto",
    "murui huitoto": "Murui Huitoto",
    # Newar. Would be "Newari" or "Nepal Bhasa" in ISO 639.
    "new": "Newar",
    "newar": "Newar",
    "newari": "Newar",
    "nepal bhasa": "Newar",
    # Norman. ISO 639-3 only.
    "nrf": "Norman",
    "norman": "Norman",
    "jèrriais": "Norman",
    # Phalura. ISO 639-3 only.
    "phl": "Phalura",
    "phalura": "Phalura",
    # Plains Cree. ISO 639-3 only.
    "crk": "Plains Cree",
    "plains cree": "Plains Cree",
    # Pnar. ISO 639-3 only.
    "pbv": "Pnar",
    "pnar": "Pnar",
    # Saterland Frisian. ISO 639-3 only.
    "stq": "Saterland Frisian",
    "saterland frisian": "Saterland Frisian",
    "saterfriesisch": "Saterland Frisian",
    # South Levantine Arabic. ISO 639-3 only.
    "ajp": "South Levantine Arabic",
    "south levantine arabic": "South Levantine Arabic",
    # Western Lawa: ISO 639-3 only.
    "lcp": "Western Lawa",
    # Eastern Lawa: ISO 639-3 only.
    "lwl": "Eastern Lawa"
}
