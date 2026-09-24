"""uztext: Uzbek text toolkit for Cyrillic, current Latin and new Latin.

>>> to_latin("Ўзбекистон")
'Oʻzbekiston'
>>> to_new("Oʻzbekiston")
'Özbekiston'
"""

from ._core import from_new, normalize, search_key, to_cyrillic, to_latin, to_new
from ._numbers import sum_words

__version__ = "0.1.0"

__all__ = [
    "from_new",
    "normalize",
    "search_key",
    "sum_words",
    "to_cyrillic",
    "to_latin",
    "to_new",
]
