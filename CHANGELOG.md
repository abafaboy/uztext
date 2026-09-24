# Changelog

This project follows [Semantic Versioning](https://semver.org/). Python and npm packages share
version numbers and behaviour.

## 0.1.0 (2026-09-24)

First release.

- `to_latin` / `toLatin`: Cyrillic (and new Latin) → current Latin, covering е/ye, ц/ts/s,
  ъ/ʼ, ь, сҳ → sʼh, month-name exceptions, and all-caps handling.
- `to_cyrillic` / `toCyrillic`: current (and new) Latin → Cyrillic, with a sourced exception
  list for ц, ъ and ь words.
- `to_new` / `toNew` and `from_new` / `fromNew`: current Latin ↔ the new alphabet approved by
  the Senate on 10 Sep 2026 (Ö Ğ Ş Ç), with the tutuq in sʼh kept as is.
- `normalize`: 12 apostrophe look-alikes → U+02BB (oʻ gʻ) / U+02BC (tutuq), plus NFC.
- `search_key` / `searchKey`: one key across scripts and apostrophe variants.
- `sum_words` / `sumWords`: amounts in words up to 999 999 999 999 soʻm plus tiyin, in all
  three scripts.
- `uztext` CLI (Python).
- Shared golden corpus of 699 cases (`corpus/cases.json`), passed by both packages.
- Offline demo page `web/index.html`.
