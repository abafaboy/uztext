# uztext (Python)

Uzbek text toolkit for Cyrillic, current Latin (oʻ gʻ sh ch) and the new Latin alphabet
approved by the Senate on 10 Sep 2026 (Ö Ğ Ş Ç; awaiting the president's signature as of
24 Sep 2026). Zero dependencies, Python 3.10+.

```python
from uztext import to_latin, to_cyrillic, to_new, from_new, normalize, search_key, sum_words

to_latin("Ўзбекистон Республикаси")   # 'Oʻzbekiston Respublikasi'
to_new("Oʻzbekiston, Toshkent shahri")  # 'Özbekiston, Toşkent şahri'
sum_words("1 250 000,50")             # 'bir million ikki yuz ellik ming soʻm ellik tiyin'
```

CLI: `uztext to-latin|to-cyrillic|to-new|from-new|normalize|search-key|sum-words [text]`
(reads stdin when no text is given).

The same behaviour ships as the npm package `uztext`, and both pass the shared corpus.
Full documentation, sources and limitations: <https://github.com/abafaboy/uztext>
