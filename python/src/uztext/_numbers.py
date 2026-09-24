"""Amounts in words for invoices (``sum_words``)."""

from __future__ import annotations

import re
from decimal import Decimal

from ._core import to_cyrillic, to_latin, to_new
from ._data import MAX_AMOUNT, ONES, SCALES, TENS, ZERO

_SPACES = re.compile("[    ]")
_DIGITS = re.compile(r"[0-9]+")
_GROUPED = re.compile(r"[0-9]{1,3}(?:[.,][0-9]{3})+")

_SCRIPTS = {"latin": to_latin, "cyrillic": to_cyrillic, "new": to_new}


def _parse_string(raw: str) -> tuple[int, int]:
    """Parse "1 250 000,50", "1,250,000.50", "1250000.5" -> (1250000, 50)."""
    s = _SPACES.sub("", raw.strip())
    last = max(s.rfind("."), s.rfind(","))
    int_part, frac = s, ""
    if last >= 0 and 1 <= len(s) - last - 1 <= 2:
        int_part, frac = s[:last], s[last + 1 :]
        if not _DIGITS.fullmatch(frac):
            raise ValueError(f"not an amount: {raw!r}")
    if _GROUPED.fullmatch(int_part) and not int_part.startswith("0"):
        # Thousands separators must all be the same character and must not be
        # the decimal separator.
        seps = set(re.sub("[0-9]", "", int_part))
        if len(seps) != 1 or (frac and s[last] in seps):
            raise ValueError(f"not an amount: {raw!r}")
        int_part = re.sub("[.,]", "", int_part)
    if not _DIGITS.fullmatch(int_part):
        raise ValueError(f"not an amount: {raw!r}")
    return int(int_part), int(frac.ljust(2, "0")) if frac else 0


def _parse_plain(s: str) -> tuple[int, int]:
    """Parse a canonical number string ("1250000.5") from a float/Decimal."""
    int_part, _, frac = s.partition(".")
    if not _DIGITS.fullmatch(int_part) or (frac and not _DIGITS.fullmatch(frac)):
        raise ValueError(f"not an amount: {s!r}")
    frac = frac.rstrip("0")
    if len(frac) > 2:
        raise ValueError(f"more than two decimals: {s!r}")
    return int(int_part), int(frac.ljust(2, "0"))


def _parse(amount: object) -> tuple[int, int]:
    if isinstance(amount, bool):
        raise TypeError("amount must be a number or a string")
    if isinstance(amount, int):
        if amount < 0:
            raise ValueError("amount must not be negative")
        return amount, 0
    if isinstance(amount, float):
        return _parse_plain(repr(amount))
    if isinstance(amount, Decimal):
        return _parse_plain(format(amount, "f"))
    if isinstance(amount, str):
        return _parse_string(amount)
    raise TypeError("amount must be a number or a string")


def _below_thousand(n: int) -> list[str]:
    words = []
    hundreds, rest = divmod(n, 100)
    if hundreds:
        words += [ONES[hundreds], "yuz"]
    tens, ones = divmod(rest, 10)
    if tens:
        words.append(TENS[tens])
    if ones:
        words.append(ONES[ones])
    return words


def _int_words(n: int) -> str:
    if n == 0:
        return ZERO
    words = []
    for value, name in SCALES:
        group, n = divmod(n, value)
        if group:
            words += _below_thousand(group) + [name]
    words += _below_thousand(n)
    return " ".join(words)


def sum_words(
    amount: int | float | str | Decimal,
    script: str = "latin",
    currency: str = "so'm",
    subunit: str = "tiyin",
) -> str:
    """Write an amount in Uzbek words, e.g. for an invoice.

    >>> sum_words("1 250 000,50")
    'bir million ikki yuz ellik ming soʻm ellik tiyin'

    ``amount`` is an int, float, Decimal or string with up to two decimals
    (``,`` or ``.`` as decimal separator; spaces, ``,`` or ``.`` as
    thousands separators). The integer part may be at most
    999 999 999 999. ``script`` is ``"latin"``, ``"cyrillic"`` or
    ``"new"``. ``currency`` and ``subunit`` are written in current Latin
    (any apostrophe) and converted to ``script``; an empty ``currency``
    drops the unit, an empty ``subunit`` drops the fractional part's unit.
    """
    if script not in _SCRIPTS:
        raise ValueError(f"script must be one of {', '.join(_SCRIPTS)}")
    whole, cents = _parse(amount)
    if whole > MAX_AMOUNT:
        raise ValueError(f"amount must not exceed {MAX_AMOUNT}")
    parts = [_int_words(whole), currency]
    if cents:
        parts += [_int_words(cents), subunit]
    return _SCRIPTS[script](" ".join(p for p in parts if p))
