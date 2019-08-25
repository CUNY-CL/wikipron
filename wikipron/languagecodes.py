# Map from a ISO 639 code or common name to its Wiktionary language name.
# ISO 639-3: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab  # noqa: E501
# Wiktionary: https://en.wiktionary.org/wiki/Category:Terms_with_IPA_pronunciation_by_language  # noqa: E501
# TODO: Expand this as needed to cover additional languages.
LANGUAGE_CODES = {
    # Greek. Would have been "Greek, Modern (1453-)" in ISO 639.
    "el": "Greek",
    "ell": "Greek",
    "gre": "Greek",
    "greek": "Greek",
    "modern greek": "Greek",
    # Slovene. Would have been "Slovenian" in ISO 639.
    "sl": "Slovene",
    "slv": "Slovene",
    "slovene": "Slovene",
    "slovenian": "Slovene",
    # Ancient Greek. Would have been "Greek, Ancient (to 1453)" in ISO 639.
    "grc": "Ancient Greek",
    "ancient greek": "Ancient Greek",
    # Aramaic. Would have been "Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)" in ISO 639.  # noqa: E501
    "arc": "Aramaic",
    "aramaic": "Aramaic",
    # Cantonese. ISO 639-3 only, not handled by the iso639 Python package.
    # TODO: Cantonese scraping not working.
    "yue": "Cantonese",
    "cantonese": "Cantonese",
    # Classical Nahuatl. ISO 639-3 only, not handled by the iso639 Python package.  # noqa: E501
    "nci": "Classical Nahuatl",
    "nahuatl": "Classical Nahuatl",
    "classical nahuatl": "Classical Nahuatl",
    "aztec": "Classical Nahuatl",
    # Egyptian. Would have been "Egyptian (Ancient)" in ISO 639.
    "egy": "Egyptian",
    "egyptian": "Egyptian",
    "ancient egyptian": "Egyptian",
    # Khmer. Would have been "Central Khmer" by the iso639 Python package.
    # TODO: Khmer scraping not working.
    "khm": "Khmer",
    "khmer": "Khmer",
    "central khmer": "Khmer",
    # Middle English. Would have been "English, Middle (1100-1500)" in ISO 639.
    "enm": "Middle English",
    "middle english": "Middle English",
    # Norwegian Bokmål. Would have been "Bokmål, Norwegian" by the iso639 Python package.  # noqa: E501
    "nob": "Norwegian Bokmål",
    "norwegian bokmål": "Norwegian Bokmål",
    # Old English. Would have been "English, Old (ca. 450-1100)" in ISO 639.
    "ang": "Old English",
    "old english": "Old English",
    # Old Irish. Would have been "Irish, Old (to 900)" in ISO 639.
    "sga": "Old Irish",
    "old irish": "Old Irish",
    # Proto-Germanic. Not handled by either ISO 639 or the iso639 Python package.  # noqa: E501
    # TODO: Proto-Germanic scraping not working.
    "proto-germanic": "Proto-Germanic",
    # Serbo-Croatian. ISO 639-3 only, not handled by the iso639 Python package.
    "hbs": "Serbo-Croatian",
    "serbo-croatian": "Serbo-Croatian",
}
