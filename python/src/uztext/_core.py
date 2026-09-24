"""Transliteration, apostrophe normalisation and search keys.

The algorithm is mirrored line for line in ``js/src/core.ts``. Any change
here needs the same change there and a corpus case that pins it.
"""

from __future__ import annotations

import unicodedata

from ._data import (
    APOSTROPHES,
    CUR_TO_NEW,
    CYR_PREFIX_EXCEPTIONS,
    CYR_TO_LAT,
    CYR_VOWELS,
    LAT_EXACT_EXCEPTIONS,
    LAT_PREFIX_EXCEPTIONS,
    LAT_TO_CYR,
    LAT_VOWELS,
    NEW_TO_CUR,
    OKINA,
    TUTUQ,
)


def _is_letter(ch: str) -> bool:
    return ch.isalpha()


def _is_upper(ch: str) -> bool:
    return ch != ch.lower()


def _is_cased(ch: str) -> bool:
    return ch.lower() != ch.upper()


def _upper_multi(lat: str, chars: str, i: int) -> str:
    """Upper-case a multi-letter replacement for the capital at ``chars[i]``.

    ``Ш`` becomes ``SH`` inside an all-caps word and ``Sh`` otherwise: the
    next cased character decides; at the end of a word the previous one does.
    """
    if len(lat) == 1:
        return lat.upper()
    caps = False
    if i + 1 < len(chars) and _is_cased(chars[i + 1]):
        caps = _is_upper(chars[i + 1])
    elif i > 0 and _is_cased(chars[i - 1]):
        caps = _is_upper(chars[i - 1])
    return lat.upper() if caps else lat[0].upper() + lat[1:]


def _apply_case(src: str, repl: str) -> str:
    """Copy the casing pattern of ``src`` (lower, Title or UPPER) to ``repl``."""
    if len(src) > 1 and src == src.upper() and src != src.lower():
        return repl.upper()
    if src and _is_upper(src[0]):
        return repl[0].upper() + repl[1:]
    return repl


def _words(text: str):
    """Split into (is_word, chunk) runs; words are maximal runs of letters."""
    out = []
    start = 0
    for i in range(1, len(text) + 1):
        if i == len(text) or _is_letter(text[i]) != _is_letter(text[start]):
            out.append((_is_letter(text[start]), text[start:i]))
            start = i
    return out


# --------------------------------------------------------------------------
# Apostrophes


def normalize(text: str) -> str:
    """Fix apostrophe look-alikes and Unicode composition.

    * NFC composition (``O`` + combining diaeresis -> ``Ö``).
    * ``Ș ș`` (comma below) -> ``Ş ş`` (cedilla).
    * Any look-alike after ``o``/``g`` -> U+02BB (``oʻ``, ``gʻ``).
    * Any look-alike between two other letters -> U+02BC (tutuq belgisi).
    * Anything else (quotes around words, feet/minutes after digits) is kept.
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace("Ș", "Ş").replace("ș", "ş")
    out = []
    n = len(text)
    for i, ch in enumerate(text):
        if ch in APOSTROPHES:
            prev = text[i - 1] if i > 0 else ""
            nxt = text[i + 1] if i + 1 < n else ""
            if prev in ("o", "O", "g", "G"):
                out.append(OKINA)
                continue
            if prev and nxt and _is_letter(prev) and _is_letter(nxt):
                out.append(TUTUQ)
                continue
        out.append(ch)
    return "".join(out)


# --------------------------------------------------------------------------
# Cyrillic -> current Latin


def _cyr_scan(word: str, start: int) -> str:
    out = []
    n = len(word)
    for i in range(start, n):
        ch = word[i]
        lc = ch.lower()
        prev = word[i - 1].lower() if i > 0 else ""
        nxt = word[i + 1].lower() if i + 1 < n else ""
        if lc == "е":
            lat = "ye" if (i == 0 or prev in CYR_VOWELS or prev in ("ъ", "ь")) else "e"
        elif lc == "ц":
            lat = "ts" if prev in CYR_VOWELS else "s"
        elif lc == "ъ":
            # Dropped after ў (мўъжиза -> moʻjiza) and between a consonant and
            # е/ё/ю/я (объект -> obyekt); otherwise the tutuq (маъюс -> maʼyus).
            iotated = nxt in ("е", "ё", "ю", "я") and prev not in CYR_VOWELS
            lat = "" if (prev == "ў" or iotated) else TUTUQ
        elif lc == "ь":
            lat = ""
        elif lc == "с" and nxt == "ҳ":
            lat = "s" + TUTUQ
        elif lc in CYR_TO_LAT:
            lat = CYR_TO_LAT[lc]
        else:
            out.append(ch)
            continue
        if ch != lc and lat:
            lat = _upper_multi(lat, word, i)
        out.append(lat)
    return "".join(out)


def _cyr_word(word: str) -> str:
    lw = word.lower()
    for stem, repl in CYR_PREFIX_EXCEPTIONS:
        if lw.startswith(stem):
            return _apply_case(word[: len(stem)], repl) + _cyr_scan(word, len(stem))
    return _cyr_scan(word, 0)


def _cyr_to_lat(text: str) -> str:
    return "".join(_cyr_word(c) if w else c for w, c in _words(text))


# --------------------------------------------------------------------------
# Current Latin -> Cyrillic


def _lat_start_or_vowel(word: str, i: int) -> bool:
    if i == 0:
        return True
    prev = word[i - 1].lower()
    if prev in LAT_VOWELS:
        return True
    return prev == OKINA and i >= 2 and word[i - 2].lower() == "o"


def _lat_scan(word: str, start: int) -> str:
    out = []
    n = len(word)
    i = start
    while i < n:
        ch = word[i]
        lc = ch.lower()
        nxt = word[i + 1].lower() if i + 1 < n else ""
        nxt2 = word[i + 2] if i + 2 < n else ""
        step = 1
        if lc in ("o", "g") and nxt == OKINA:
            cyr = "ў" if lc == "o" else "ғ"
            step = 2
        elif lc == "s" and nxt == "h":
            cyr, step = "ш", 2
        elif lc == "c" and nxt == "h":
            cyr, step = "ч", 2
        elif lc == "y" and nxt == "e":
            if _lat_start_or_vowel(word, i):
                cyr, step = "е", 2
            else:
                cyr = "й"
        elif lc == "y" and nxt in ("a", "o", "u") and nxt2 != OKINA:
            cyr, step = {"a": "я", "o": "ё", "u": "ю"}[nxt], 2
        elif lc == "e":
            cyr = "э" if _lat_start_or_vowel(word, i) else "е"
        elif ch == TUTUQ:
            prev = word[i - 1].lower() if i > 0 else ""
            cyr = "" if (prev == "s" and nxt == "h") else "ъ"
        elif lc in LAT_TO_CYR:
            cyr = LAT_TO_CYR[lc]
        else:
            cyr = ch
        if _is_upper(ch):
            cyr = cyr.upper()
        out.append(cyr)
        i += step
    return "".join(out)


def _lat_word(word: str) -> str:
    lw = word.lower()
    if lw in LAT_EXACT_EXCEPTIONS:
        return _apply_case(word, LAT_EXACT_EXCEPTIONS[lw])
    for stem, repl in LAT_PREFIX_EXCEPTIONS:
        if lw.startswith(stem):
            return _apply_case(word[: len(stem)], repl) + _lat_scan(word, len(stem))
    return _lat_scan(word, 0)


def _lat_to_cyr(text: str) -> str:
    return "".join(_lat_word(c) if w else c for w, c in _words(text))


# --------------------------------------------------------------------------
# Current Latin <-> new Latin


def _cur_to_new(text: str) -> str:
    out = []
    n = len(text)
    i = 0
    while i < n:
        pair = text[i : i + 2].lower()
        if pair in CUR_TO_NEW:
            new = CUR_TO_NEW[pair]
            out.append(new.upper() if _is_upper(text[i]) else new)
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _new_to_cur(text: str) -> str:
    out = []
    for i, ch in enumerate(text):
        lc = ch.lower()
        if lc in NEW_TO_CUR:
            cur = NEW_TO_CUR[lc]
            out.append(_upper_multi(cur, text, i) if ch != lc else cur)
        else:
            out.append(ch)
    return "".join(out)


# --------------------------------------------------------------------------
# Public API


def to_latin(text: str) -> str:
    """Any script -> current Latin (1995 alphabet)."""
    return _new_to_cur(_cyr_to_lat(normalize(text)))


def to_cyrillic(text: str) -> str:
    """Any script -> Cyrillic."""
    return _lat_to_cyr(_new_to_cur(normalize(text)))


def to_new(text: str) -> str:
    """Any script -> new Latin (Ö Ğ Ş Ç, Senate-approved 10 Sep 2026)."""
    return _cur_to_new(_cyr_to_lat(normalize(text)))


def from_new(text: str) -> str:
    """New Latin -> current Latin. Leaves Cyrillic untouched."""
    return _new_to_cur(normalize(text))


def search_key(text: str) -> str:
    """Fold every script and apostrophe variant to one lower-case key."""
    key = to_new(text).lower()
    return key.replace(TUTUQ, "").replace(OKINA, "")
