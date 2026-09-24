"""Letter tables and exception lists.

Every entry here is mirrored in ``js/src/data.ts``; both test suites check
that each exception is exercised by ``corpus/cases.json``. Sources for each
rule are listed in ``docs/RULES.md``.
"""

# U+02BB MODIFIER LETTER TURNED COMMA: the mark in oʻ and gʻ.
OKINA = "ʻ"
# U+02BC MODIFIER LETTER APOSTROPHE: the tutuq belgisi.
TUTUQ = "ʼ"

# Characters people type instead of ʻ or ʼ.
APOSTROPHES = frozenset(
    "'"  # U+0027 APOSTROPHE
    "`"  # U+0060 GRAVE ACCENT
    "´"  # ´ ACUTE ACCENT
    "‘"  # ‘ LEFT SINGLE QUOTATION MARK
    "’"  # ’ RIGHT SINGLE QUOTATION MARK
    "‛"  # ‛ SINGLE HIGH-REVERSED-9 QUOTATION MARK
    "ʻ"  # ʻ MODIFIER LETTER TURNED COMMA
    "ʼ"  # ʼ MODIFIER LETTER APOSTROPHE
    "ʹ"  # ʹ MODIFIER LETTER PRIME
    "ʽ"  # ʽ MODIFIER LETTER REVERSED COMMA
    "′"  # ′ PRIME
    "＇"  # ＇ FULLWIDTH APOSTROPHE
)

CYR_VOWELS = frozenset("аеёиоуэюяў")

CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l",
    "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s",
    "т": "t", "у": "u", "ф": "f", "х": "x", "ч": "ch", "ш": "sh",
    "э": "e", "ю": "yu", "я": "ya", "ў": "o" + OKINA, "қ": "q",
    "ғ": "g" + OKINA, "ҳ": "h",
    # Not part of the Uzbek Cyrillic alphabet; Uzbek spelling replaces
    # them with шч and и (see docs/RULES.md, marked unverified).
    "щ": "shch", "ы": "i",
}

LAT_VOWELS = frozenset("aeiou")

LAT_TO_CYR = {
    "a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ",
    "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н",
    "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т",
    "u": "у", "v": "в", "x": "х", "y": "й", "z": "з",
}

# Cyrillic -> Latin: stems whose Latin spelling does not follow the letter
# rules (1995 rules §1: "sentabr, noyabr kabi soʻzlarda").
CYR_PREFIX_EXCEPTIONS = (
    ("сентябр", "sentabr"),
    ("октябр", "oktabr"),
)

# Latin -> Cyrillic: whole words only.
LAT_EXACT_EXCEPTIONS = {
    "sirk": "цирк",
    "sex": "цех",
    "nol": "ноль",
}

# Latin -> Cyrillic: stems; the rest of the word follows the letter rules.
# No stem is a prefix of another (checked by the tests), so order is free.
LAT_PREFIX_EXCEPTIONS = (
    ("konstitutsiya", "конституция"),
    ("federatsiya", "федерация"),
    ("kvitansiya", "квитанция"),
    ("kompyuter", "компьютер"),
    ("politsiya", "полиция"),
    ("stansiya", "станция"),
    ("mo" + OKINA + "jiza", "мўъжиза"),
    ("sentabr", "сентябрь"),
    ("konsert", "концерт"),
    ("subyekt", "субъект"),
    ("oktabr", "октябрь"),
    ("noyabr", "ноябрь"),
    ("dekabr", "декабрь"),
    ("prinsip", "принцип"),
    ("fevral", "февраль"),
    ("yanvar", "январь"),
    ("litsey", "лицей"),
    ("sement", "цемент"),
    ("obyekt", "объект"),
    ("atelye", "ателье"),
    ("aksiya", "акция"),
    ("aprel", "апрель"),
    ("syezd", "съезд"),
    ("pyesa", "пьеса"),
    ("vitse", "вице"),
    ("iyun", "июнь"),
    ("iyul", "июль"),
)

# Current Latin <-> new (2026) Latin.
CUR_TO_NEW = {
    "o" + OKINA: "ö",
    "g" + OKINA: "ğ",
    "sh": "ş",
    "ch": "ç",
}
NEW_TO_CUR = {"ö": "o" + OKINA, "ğ": "g" + OKINA, "ş": "sh", "ç": "ch"}

# Number words (current Latin); converted to other scripts after assembly.
ONES = ("", "bir", "ikki", "uch", "to" + OKINA + "rt", "besh", "olti",
        "yetti", "sakkiz", "to" + OKINA + "qqiz")
TENS = ("", "o" + OKINA + "n", "yigirma", "o" + OKINA + "ttiz", "qirq",
        "ellik", "oltmish", "yetmish", "sakson", "to" + OKINA + "qson")
SCALES = ((10**9, "milliard"), (10**6, "million"), (10**3, "ming"))
ZERO = "nol"
MAX_AMOUNT = 999_999_999_999
