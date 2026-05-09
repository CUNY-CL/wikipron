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
    # Min Nan / Southern Min. Would be "Min Nan Chinese" in ISO 639-3.
    "nan": "Min Nan",
    "min nan": "Min Nan",
    "min nan chinese": "Min Nan",
    "southern min": "Min Nan",
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
    # Old Galician-Portuguese. Not an ISO 639 language. Wiktionary renamed
    # this from "Old Portuguese".
    "roa-opt": "Old Galician-Portuguese",
    "old portuguese": "Old Galician-Portuguese",
    "old galician-portuguese": "Old Galician-Portuguese",
    "opt": "Old Galician-Portuguese",  # TODO: Drop? opt is Opata in ISO 639-3.  # noqa: E501
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
    "cmn": "Mandarin",
    "chinese": "Mandarin",
    "mandarin": "Mandarin",
    "mandarin chinese": "Mandarin",
    # Gan Chinese.
    "gan": "Gan",
    "gan chinese": "Gan",
    # Hakka Chinese.
    "hak": "Hakka",
    "hakka": "Hakka",
    "hakka chinese": "Hakka",
    # Jin Chinese. Would be "Jinyu Chinese" in ISO 639-3.
    "cjy": "Jin",
    "jin": "Jin",
    "jin chinese": "Jin",
    "jinyu chinese": "Jin",
    # Northern Min Chinese. Would be "Min Bei Chinese" in ISO 639-3.
    "mnp": "Northern Min",
    "northern min": "Northern Min",
    "min bei chinese": "Northern Min",
    # Eastern Min Chinese. Would be "Min Dong Chinese" in ISO 639-3.
    "cdo": "Eastern Min",
    "eastern min": "Eastern Min",
    "min dong chinese": "Eastern Min",
    # Puxian Min Chinese. Would be "Pu-Xian Chinese" in ISO 639-3.
    "cpx": "Puxian Min",
    "puxian min": "Puxian Min",
    "pu-xian chinese": "Puxian Min",
    # Leizhou Chinese / Leizhou Min.
    "luh": "Leizhou Min",
    "leizhou min": "Leizhou Min",
    "leizhou chinese": "Leizhou Min",
    # Southern Pinghua.
    "csp": "Southern Pinghua",
    "southern pinghua": "Southern Pinghua",
    # Wu Chinese.
    "wuu": "Wu",
    "wu": "Wu",
    "wu chinese": "Wu",
    # Xiang Chinese.
    "hsn": "Xiang",
    "xiang": "Xiang",
    "xiang chinese": "Xiang",
    # Old Chinese.
    "och": "Old Chinese",
    "old chinese": "Old Chinese",
    # Middle Chinese. Would be "Late Middle Chinese" in ISO 639-3.
    "ltc": "Middle Chinese",
    "middle chinese": "Middle Chinese",
    "late middle chinese": "Middle Chinese",
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
    # Central Bikol. Wiktionary renamed this from "Bikol Central".
    "bcl": "Central Bikol",
    "bikol central": "Central Bikol",
    "central bikol": "Central Bikol",
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
    # Acehnese. Would be "Achinese" in ISO 639-3.
    "ace": "Acehnese",
    "acehnese": "Acehnese",
    "achinese": "Acehnese",
    # Ainu. Would be "Ainu (Japan)" in ISO 639-3.
    "ain": "Ainu",
    "ainu": "Ainu",
    # Aromanian. Would be "Macedo-Romanian" in ISO 639-3.
    "rup": "Aromanian",
    "aromanian": "Aromanian",
    "macedo-romanian": "Aromanian",
    # Barngarla. Would be "Banggarla" in ISO 639-3.
    "bjb": "Barngarla",
    "barngarla": "Barngarla",
    "banggarla": "Barngarla",
    # Carpathian Rusyn. Would be "Rusyn" in ISO 639-3.
    "rue": "Carpathian Rusyn",
    "rusyn": "Carpathian Rusyn",
    "carpathian rusyn": "Carpathian Rusyn",
    # Chichewa. Would be "Nyanja" in ISO 639-3.
    "nya": "Chichewa",
    "chichewa": "Chichewa",
    "nyanja": "Chichewa",
    # East Circassian. Wiktionary renamed this from "Kabardian".
    "kbd": "East Circassian",
    "kabardian": "East Circassian",
    "east circassian": "East Circassian",
    # Franco-Provençal. Would be "Arpitan" in ISO 639-3.
    "frp": "Franco-Provençal",
    "franco-provençal": "Franco-Provençal",
    "arpitan": "Franco-Provençal",
    # Guaraní.
    "grn": "Guaraní",
    "guarani": "Guaraní",
    "guaraní": "Guaraní",
    # Gullah. Would be "Sea Island Creole English" in ISO 639-3.
    "gul": "Gullah",
    "gullah": "Gullah",
    "sea island creole english": "Gullah",
    # Haitian Creole. Would be "Haitian" in ISO 639-3.
    "hat": "Haitian Creole",
    "haitian creole": "Haitian Creole",
    "haitian": "Haitian Creole",
    # Iraqi Arabic. Would be "Mesopotamian Arabic" in ISO 639-3.
    "acm": "Iraqi Arabic",
    "iraqi arabic": "Iraqi Arabic",
    "mesopotamian arabic": "Iraqi Arabic",
    # Juba Arabic. Would be "Sudanese Creole Arabic" in ISO 639-3.
    "pga": "Juba Arabic",
    "juba arabic": "Juba Arabic",
    "sudanese creole arabic": "Juba Arabic",
    # Juǀ'hoan.
    "ktz": "Juǀ'hoan",
    "juǀ'hoan": "Juǀ'hoan",
    # Kalami. Would be "Gawri" in ISO 639-3.
    "gwc": "Kalami",
    "kalami": "Kalami",
    "gawri": "Kalami",
    # Kapampangan. Would be "Pampanga" in ISO 639-3.
    "pam": "Kapampangan",
    "kapampangan": "Kapampangan",
    "pampanga": "Kapampangan",
    # Kari'na. Would be "Galibi Carib" in ISO 639-3.
    "car": "Kari'na",
    "kari'na": "Kari'na",
    "galibi carib": "Kari'na",
    # Konkani.
    "kok": "Konkani",
    "konkani": "Konkani",
    # Kurtöp. Would be "Kurtokha" in ISO 639-3.
    "xkz": "Kurtöp",
    "kurtöp": "Kurtöp",
    "kurtokha": "Kurtöp",
    # Kurux. Would be "Kurukh" in ISO 639-3.
    "kru": "Kurux",
    "kurux": "Kurux",
    "kurukh": "Kurux",
    # Kwak'wala. Would be "Kwakiutl" in ISO 639-3.
    "kwk": "Kwak'wala",
    "kwak'wala": "Kwak'wala",
    "kwakiutl": "Kwak'wala",
    # Maguindanao. Would be "Maguindanaon" in ISO 639-3.
    "mdh": "Maguindanao",
    "maguindanao": "Maguindanao",
    "maguindanaon": "Maguindanao",
    # Malay. Would be "Malay (macrolanguage)" in ISO 639-3.
    "msa": "Malay",
    "malay": "Malay",
    # Māori. Wiktionary writes it with a macron.
    "mri": "Māori",
    "maori": "Māori",
    "māori": "Māori",
    # Middle High German. Would be "Middle High German (ca. 1050-1500)" in
    # ISO 639-3.
    "gmh": "Middle High German",
    "middle high german": "Middle High German",
    # Nepali. Would be "Nepali (macrolanguage)" in ISO 639-3.
    "nep": "Nepali",
    "nepali": "Nepali",
    # Nheengatu. Would be "Nhengatu" in ISO 639-3.
    "yrl": "Nheengatu",
    "nheengatu": "Nheengatu",
    "nhengatu": "Nheengatu",
    # North Levantine Arabic. Would be "Levantine Arabic" in ISO 639-3.
    "apc": "North Levantine Arabic",
    "north levantine arabic": "North Levantine Arabic",
    "levantine arabic": "North Levantine Arabic",
    # Nuosu. Wiktionary renamed this from "Sichuan Yi".
    "iii": "Nuosu",
    "nuosu": "Nuosu",
    "sichuan yi": "Nuosu",
    # Nupe. Would be "Nupe-Nupe-Tako" in ISO 639-3.
    "nup": "Nupe",
    "nupe": "Nupe",
    "nupe-nupe-tako": "Nupe",
    # Nǀuu. Would be "Nǁng" in ISO 639-3.
    "ngh": "Nǀuu",
    "nǀuu": "Nǀuu",
    "nǁng": "Nǀuu",
    # Ojibwe. Would be "Ojibwa" in ISO 639-3.
    "oji": "Ojibwe",
    "oj": "Ojibwe",
    "ojibwe": "Ojibwe",
    "ojibwa": "Ojibwe",
    # Old East Slavic. Would be "Old Russian" in ISO 639-3.
    "orv": "Old East Slavic",
    "old east slavic": "Old East Slavic",
    "old russian": "Old East Slavic",
    # Old Javanese. Would be "Kawi" in ISO 639-3.
    "kaw": "Old Javanese",
    "old javanese": "Old Javanese",
    "kawi": "Old Javanese",
    # Oriya. Would be "Oriya (macrolanguage)" in ISO 639-3.
    "ori": "Oriya",
    "oriya": "Oriya",
    # Ossetian. Would be "Iron Ossetic" in ISO 639-3.
    "oss": "Ossetian",
    "os": "Ossetian",
    "ossetian": "Ossetian",
    "iron ossetic": "Ossetian",
    # Palula. Wiktionary renamed this from "Phalura".
    "phl": "Palula",
    "palula": "Palula",
    "phalura": "Palula",
    # Pannonian Rusyn. Would be "Ruthenian" in ISO 639-3.
    "rsk": "Pannonian Rusyn",
    "pannonian rusyn": "Pannonian Rusyn",
    "ruthenian": "Pannonian Rusyn",
    # Paraguayan Guarani. Would be "Paraguayan Guaraní" in ISO 639-3.
    "gug": "Paraguayan Guarani",
    "paraguayan guarani": "Paraguayan Guarani",
    "paraguayan guaraní": "Paraguayan Guarani",
    # Pichinglis. Would be "Fernando Po Creole English" in ISO 639-3.
    "fpe": "Pichinglis",
    "pichinglis": "Pichinglis",
    "fernando po creole english": "Pichinglis",
    # Rapa Nui. Would be "Rapanui" in ISO 639-3.
    "rap": "Rapa Nui",
    "rapa nui": "Rapa Nui",
    "rapanui": "Rapa Nui",
    # Romani. Would be "Romany" in ISO 639-3.
    "rom": "Romani",
    "romani": "Romani",
    "romany": "Romani",
    # Sassarese. Would be "Sassarese Sardinian" in ISO 639-3.
    "sdc": "Sassarese",
    "sassarese": "Sassarese",
    "sassarese sardinian": "Sassarese",
    # Senhaja de Srair. iso639's name uses the same spelling.
    "sjs": "Senhaja de Srair",
    "senhaja de srair": "Senhaja de Srair",
    "senhaja berber": "Senhaja de Srair",
    # Sinhalese. Would be "Sinhala" in ISO 639-3.
    "sin": "Sinhalese",
    "sinhalese": "Sinhalese",
    "sinhala": "Sinhalese",
    # South Levantine Arabic.
    "ajp": "South Levantine Arabic",
    "south levantine arabic": "South Levantine Arabic",
    # Swahili. Would be "Swahili (macrolanguage)" in ISO 639-3.
    "swa": "Swahili",
    "swahili": "Swahili",
    # Tashelhit. Would be "Tachelhit" in ISO 639-3.
    "shi": "Tashelhit",
    "tashelhit": "Tashelhit",
    "tachelhit": "Tashelhit",
    # Tokelauan. Would be "Tokelau" in ISO 639-3.
    "tkl": "Tokelauan",
    "tokelauan": "Tokelauan",
    "tokelau": "Tokelauan",
    # Tsuut'ina. Would be "Sarsi" in ISO 639-3.
    "srs": "Tsuut'ina",
    "tsuut'ina": "Tsuut'ina",
    "sarsi": "Tsuut'ina",
    # Ulwa (Nicaragua). iso639's name is "Ulwa".
    "ulw": "Ulwa (Nicaragua)",
    "ulwa": "Ulwa (Nicaragua)",
    "ulwa (nicaragua)": "Ulwa (Nicaragua)",
    # Venetan. Would be "Venetian" in ISO 639-3.
    "vec": "Venetan",
    "venetan": "Venetan",
    "venetian": "Venetan",
    # Waray-Waray. Would be "Waray (Philippines)" in ISO 639-3.
    "war": "Waray-Waray",
    "waray-waray": "Waray-Waray",
    "waray (philippines)": "Waray-Waray",
    # West Circassian. Wiktionary renamed this from "Adyghe".
    "ady": "West Circassian",
    "adyghe": "West Circassian",
    "west circassian": "West Circassian",
    # Western Pwo. Would be "Pwo Western Karen" in ISO 639-3.
    "pwo": "Western Pwo",
    "western pwo": "Western Pwo",
    "pwo western karen": "Western Pwo",
    # Ye'kwana. Wiktionary renamed this from "Maquiritari".
    "mch": "Ye'kwana",
    "ye'kwana": "Ye'kwana",
    "maquiritari": "Ye'kwana",
    # Yola.
    "yol": "Yola",
    "yola": "Yola",
    # Yucatec Maya. Would be "Yucateco" in ISO 639-3.
    "yua": "Yucatec Maya",
    "yucatec maya": "Yucatec Maya",
    "yucateco": "Yucatec Maya",
    # Languages whose Wiktionary code has no ISO 639 mapping.
    # Black Speech. Constructed language.
    "art-bsp": "Black Speech",
    "black speech": "Black Speech",
    # Champenois.
    "roa-cha": "Champenois",
    "champenois": "Champenois",
    # Chungli Ao.
    "njo-jgl": "Chungli Ao",
    "chungli ao": "Chungli Ao",
    # Eastern Khanty.
    "kca-eas": "Eastern Khanty",
    "eastern khanty": "Eastern Khanty",
    # Jersey Dutch.
    "gmw-jdt": "Jersey Dutch",
    "jersey dutch": "Jersey Dutch",
    # Komi-Yazva.
    "urj-kya": "Komi-Yazva",
    "komi-yazva": "Komi-Yazva",
    # Mariupol Greek.
    "grk-mar": "Mariupol Greek",
    "mariupol greek": "Mariupol Greek",
    # Northern Khanty.
    "kca-nor": "Northern Khanty",
    "northern khanty": "Northern Khanty",
    # Northern Mansi.
    "mns-nor": "Northern Mansi",
    "northern mansi": "Northern Mansi",
    # Old Czech.
    "zlw-ocs": "Old Czech",
    "old czech": "Old Czech",
    # Old Polish.
    "zlw-opl": "Old Polish",
    "old polish": "Old Polish",
    # Sarawak Malay.
    "poz-sml": "Sarawak Malay",
    "sarawak malay": "Sarawak Malay",
    # Slovincian.
    "zlw-slv": "Slovincian",
    "slovincian": "Slovincian",
    # Solon.
    "tuw-sol": "Solon",
    "solon": "Solon",
    # Hokkien. Wiktionary's separate "Hokkien" (nan-hbl) category is a
    # variety of Min Nan; resolve it to the existing Min Nan handler. The
    # "hokkien" dialect under nan in languages.json continues to handle
    # the variety-specific scrape.
    "hokkien": "Min Nan",
    "nan-hbl": "Min Nan",
}
