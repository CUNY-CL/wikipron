# This is a map from an ISO 639 code or common name to its Wiktionary language name.  # noqa: E501
# ISO 639-3: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab  # noqa: E501
# Wiktionary: https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language  # noqa: E501
# TODO: Expand this as needed to cover additional languages.
LANGUAGE_CODES = {
    # Greek. Would be "Modern Greek (1453-)" in ISO 639-3.
    "el": "Greek",
    "ell": "Greek",
    "gre": "Greek",
    "greek": "Greek",
    "modern greek": "Greek",
    # Slovene. Would be "Slovenian" in ISO 639-3.
    "sl": "Slovene",
    "slv": "Slovene",
    "slovene": "Slovene",
    "slovenian": "Slovene",
    # Ancient Greek. Would be "Ancient Greek (to 1453)" in ISO 639-3.
    "grc": "Ancient Greek",
    "ancient greek": "Ancient Greek",
    # Aramaic. Would be "Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)" in ISO 639-3.  # noqa: E501
    "arc": "Aramaic",
    "aramaic": "Aramaic",
    # Cantonese. Would be "Yue Chinese" in ISO 639-3.
    "yue": "Cantonese",
    "cantonese": "Cantonese",
    "yue chinese": "Cantonese",
    # Classical Nahuatl.
    "nahuatl": "Classical Nahuatl",
    "aztec": "Classical Nahuatl",
    # Egyptian. Would be "Egyptian (Ancient)" in ISO 639-3.
    "egy": "Egyptian",
    "egyptian": "Egyptian",
    "ancient egyptian": "Egyptian",
    # Middle English. Would be "English, Middle (1100-1500)" in ISO 639-3.
    "enm": "Middle English",
    "middle english": "Middle English",
    # Old English. Would be "English, Old (ca. 450-1100)" in ISO 639-3.
    "ang": "Old English",
    "old english": "Old English",
    # Old Irish. Would be "Irish, Old (to 900)" in ISO 639-3.
    "sga": "Old Irish",
    "old irish": "Old Irish",
    # Alemannic German. Would be "Alemannic, Alsatian, Swiss German" in ISO 639-3.  # noqa: E501
    "gsw": "Alemannic German",
    "alemannic german": "Alemannic German",
    "swiss german": "Alemannic German",
    "alsatian german": "Alemannic German",
    "alsatian": "Alemannic German",
    # Alutor.
    "alyutor": "Alutor",
    # Central Franconian. Not an ISO 639 language.
    "central franconian": "Central Franconian",
    # Dalmatian.
    "dalmatic": "Dalmatian",
    # Gamilaraay.
    "kamilaroi": "Gamilaraay",
    # German Low German. Not an ISO 639 language.
    "german low german": "German Low German",
    # Interlingua. Would be "Interlingua (International Auxiliary Language Association)" in ISO 639.  # noqa: E501
    "ina": "Interlingua",
    "interlingua": "Interlingua",
    # Limburgish. Would be "Limburgan, Limburger, Limburgish" in ISO 639-3.
    "lim": "Limburgish",
    "limburgish": "Limburgish",
    "limburgan": "Limburgish",
    "limburger": "Limburgish",
    "limburgic": "Limburgish",
    # Livonian. Would be "Liv" in ISO 639-3.
    "liv": "Livonian",
    "livonian": "Livonian",
    # Mauritian Creole. Would be "Morisyen" in ISO 639-3.
    "mfe": "Mauritian Creole",
    "mauritian creole": "Mauritian Creole",
    "morisyen": "Mauritian Creole",
    "morisien": "Mauritian Creole",
    # Middle Dutch. Would be "Middle Dutch (ca. 1050-1350)" in ISO 639-3.
    "dum": "Middle Dutch",
    "middle dutch": "Middle Dutch",
    # Min Nan. Would be "Min Nan Chinese" in ISO 639-3.
    "nan": "Min Nan",
    "min nan": "Min Nan",
    "min nan chinese": "Min Nan",
    # North Frisian. Would be "Northern Frisian" in ISO 639-3.
    "frr": "North Frisian",
    "north frisian": "North Frisian",
    "northern frisian": "North Frisian",
    # Occitan. Would be "Occitan (post 1500)" in ISO 639-3.
    "oci": "Occitan",
    "occitan": "Occitan",
    # Old French. Would be "Old French (842-ca. 1400)" in ISO 639-3.
    "fro": "Old French",
    "old french": "Old French",
    # Old High German. Would be "Old High German (ca. 750-1050)" in ISO 639-3.
    "goh": "Old High German",
    "old high german": "Old High German",
    # Old Portuguese. Not an ISO 639 language.
    "old portuguese": "Old Portuguese",
    "roa-opt": "Old Portuguese",
    "opt": "Old Portuguese",  # TODO: Drop this? opt is Opata in ISO 639-3.
    # Old Tupi. Would be "Tupí" in ISO 639-3.
    "tpw": "Old Tupi",
    "old tupi": "Old Tupi",
    "classical tupi": "Old Tupi",
    "tupí": "Old Tupi",
    # Pashto. Would be "Pashto, Pushto" in ISO 639-3.
    "pus": "Pashto",
    "pashto": "Pashto",
    "pushto": "Pashto",
    # Piedmontese. Would be "Piemontese" in ISO 639-3.
    "pms": "Piedmontese",
    "piedmontese": "Piedmontese",
    "piemontese": "Piedmontese",
    # Pipil.
    "nawat": "Pipil",
    # Punjabi. Would be "Panjabi, Punjabi" in ISO 639-3.
    "pan": "Punjabi",
    "panjabi": "Punjabi",
    "punjabi": "Punjabi",
    # Scanian. Not an ISO 639 language.
    "scanian": "Scanian",
    # Taos. Would be "Northern Tiwa" in ISO 639-3.
    "twf": "Taos",
    "taos": "Taos",
    "northern tiwa": "Taos",
    # Tongan. Would be "Tonga (Tonga Islands)" in ISO 639-3.
    "ton": "Tongan",
    "tongan": "Tongan",
    "tonga": "Tongan",
    # Uyghur. Would be "Uighur, Uyghur" in ISO 639-3.
    "uig": "Uyghur",
    "uighur": "Uyghur",
    "uyghur": "Uyghur",
    # Wauja. Would be "Waurá" in ISO 639-3.
    "wau": "Wauja",
    "waurá": "Wauja",
    "wauja": "Wauja",
    # West Frisian. Would be "Western Frisian" in ISO 639-3.
    "fry": "West Frisian",
    "west frisian": "West Frisian",
    "western frisian": "West Frisian",
    # Westrobothnian. Not an ISO 639 language.
    "westrobothnian": "Westrobothnian",
    # White Hmong. Would be "Hmong Daw" in ISO 639-3.
    "mww": "White Hmong",
    "white hmong": "White Hmong",
    "hmong daw": "White Hmong",
    # Zazaki. Would be "Dimili, Dimli (macrolanguage), Kirdki, Kirmanjki (macrolanguage), Zaza, Zazaki" in ISO 639-3.  # noqa: E501
    "zza": "Zazaki",
    "zazaki": "Zazaki",
    "zaza": "Zazaki",
    "dimili": "Zazaki",
    "dimli": "Zazaki",
    "kirdki": "Zazaki",
    "kirmanjki": "Zazaki",
    # Okinawan. Would be "Central Okinawan" in ISO 639-3.
    "ryu": "Okinawan",
    "okinawan": "Okinawan",
    "central okinawan": "Okinawan",
    # Ottoman Turkish. Would be "Ottoman Turkish (1500-1928)" in ISO 639-3.
    "ota": "Ottoman Turkish",
    "ottoman turkish": "Ottoman Turkish",
    # Brunei Malay. Would be "Brunei" in ISO 639-3.
    "kxd": "Brunei Malay",
    "brunei malay": "Brunei Malay",
    "brunei": "Brunei Malay",
    # Mecayapan Nahuatl. Would be "Isthmus-Mecayapan Nahuatl" in ISO 639-3.
    "nhx": "Mecayapan Nahuatl",
    "mecayapan nahuatl": "Mecayapan Nahuatl",
    "isthmus-mecayapan nahautl": "Mecayapan Nahuatl",
    # Lamboya. Would be "Lamboya" in ISO 639-3.
    "lmy": "Laboya",
    "laboya": "Laboya",
    "lamboya": "Laboya",
    # Mandarin Chinese. Would be "Mandarin Chinese" in ISO 639-3.
    "cmn": "Chinese",
    "chinese": "cmn",
    "mandarin chinese": "cmn",
    # Abkhaz. Would be "Abkhazian" in ISO 639-3.
    "abk": "Abkhaz",
    "abkhaz": "Abkhaz",
    "abkhazian": "Abkhaz",
    # Avar. Would be "Avaric" in ISO 639-3.
    "ava": "Avar",
    "avar": "Avar",
    "avaric": "Avar",
    # Buryat. Would be "Buriat" in ISO 639-3.
    "bua": "Buryat",
    "buryat": "Buryat",
    "buriat": "Buryat",
    # Chukchi. Would be "Chukot" in ISO 639-3.
    "ckt": "Chukchi",
    "chukchi": "Chukchi",
    "chukot": "Chukchi",
    # Tundra Nenets. Would be "Nenets" in ISO 639-3.
    "yrk": "Tundra Nenets",
    "tundra nenets": "Tundra Nenets",
    "nenets": "Tundra Nenets",
    # Estonian. Would be "Standard Estonian" in ISO 639-3.
    "ekk": "Estonian",
    "standard estonian": "Estonian",
    # Greenlandic. Would be "Kalaallisut" in ISO 639-3.
    "kal": "Greenlandic",
    "greenlandic": "Greenlandic",
    "kalaallisut": "Greenlandic",
    # Lezgi. Would be "Lezghian" in ISO 639-3.
    "lez": "Lezgi",
    "lezgi": "Lezgi",
    "lezghian": "Lezgi",
    # Nivkh. Would be "Gilyak" in ISO 639-3.
    "niv": "Nivkh",
    "nivkh": "Nivkh",
    "gilyak": "Nivkh",
    # Jeju. Would be "Jejueo" in ISO 639-3.
    "jje": "Jeju",
    "jeju": "Jeju",
    "jejueo": "Jeju",
    # Tuvan. Would be "Tuvinian" in ISO 639-3.
    "tyv": "Tuvan",
    "tuvan": "Tuvan",
    "tuvinian": "Tuvan",
    # Bikol Central. Would be "Central Bikol" in ISO 639-3.
    "bcl": "Bikol Central",
    "bikol central": "Bikol Central",
    "central bikol": "Bikol Central",
    # Kyrgyz. Would be "Kirghiz" in ISO 639-3.
    "kir": "Kyrgyz",
    "kyrgyz": "Kyrgyz",
    "kirghiz": "Kyrgyz",
    # Middle Irish. Would be "Middle Irish (900-1200)" in ISO 639-3.
    "mga": "Middle Irish",
    "middle irish": "Middle Irish",
    # Middle Korean. Would be "Middle Korean (10th-16th cent.)" in ISO 639-3.
    "okm": "Middle Korean",
    "middle korean": "Middle Korean",
    # Northern Kurdish.
    "kurmanji": "Northern Kurdish",
    # Ilocano. Would be "Iloko" in ISO 639-3.
    "ilo": "Ilocano",
    "iloko": "Ilocano",
    "ilocano": "Ilocano",
    # Jamaican Creole. Would be "Jamaican Creole English" in ISO 639-3.
    "jam": "Jamaican Creole",
    "jamaican creole": "Jamaican Creole",
    "jamaican creole english": "Jamaican Creole",
    # Newar. Would be "Newari" or "Nepal Bhasa" in ISO 639-3.
    "new": "Newar",
    "newar": "Newar",
    "newari": "Newar",
    "nepal bhasa": "Newar",
    # Norman. Would be "Jèrriais" in ISO 639-3.
    "nrf": "Norman",
    "norman": "Norman",
    "jèrriais": "Norman",
    # Saterland Frisian. Would be "Saterfriesisch" in ISO 639-3.
    "stq": "Saterland Frisian",
    "saterland frisian": "Saterland Frisian",
    "saterfriesisch": "Saterland Frisian",
    # Nyah Kur. Would be "Nyahkur" in ISO 639-3.
    "cbn": "Nyah Kur",
    "nyah kur": "Nyah Kur",
    "nyahkur": "Nyah Kur",
    # Not-already-mentioned languages from languages.json that have
    # a difference between their iso639 and Wiktionary name.
    "ain": "Ainu",
    "rup": "Aromanian",
    "bjb": "Barngarla",
    "nya": "Chichewa",
    "grn": "Guaraní",
    "hat": "Haitian Creole",
    "ktz": "Juǀ'hoan",
    "pam": "Kapampangan",
    "kok": "Konkani",
    "kwk": "Kwak'wala",
    "msa": "Malay",
    "nep": "Nepali",
    "nup": "Nupe",
    "orv": "Old East Slavic",
    "kaw": "Old Javanese",
    "ori": "Oriya",
    "rap": "Rapa Nui",
    "rom": "Romani",
    "sdc": "Sassarese",
    "sin": "Sinhalese",
    "swa": "Swahili",
    "tkl": "Tokelauan",
    "srs": "Tsuut'ina",
    "yua": "Yucatec Maya",
}
