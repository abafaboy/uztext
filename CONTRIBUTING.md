# Contributing

Thank you! The most useful thing you can do takes five minutes: **add a word to the corpus.**

## 1. Add a corpus case (easiest)

Every behaviour of uztext is pinned by [`corpus/cases.json`](corpus/cases.json). The Python and
JavaScript test suites both run every case, so a new case protects both packages at once.

Add one line to the `cases` array:

```json
{"id": "to_latin-224", "fn": "to_latin", "input": "қовун", "expected": "qovun", "source": "IZOH"}
```

- `id`: the function name plus the next free number for that function. Ids must be unique.
- `fn`: one of `to_latin`, `to_cyrillic`, `to_new`, `from_new`, `normalize`, `search_key`,
  `sum_words`.
- `input` and `expected`: write `ʻ` (U+02BB) in oʻ/gʻ and `ʼ` (U+02BC) for the tutuq in
  `expected`. `input` may use any apostrophe; that is the point of `normalize`.
- `args` (optional, `sum_words` only): `{"script": "cyrillic" | "new", "currency": "...", "subunit": "..."}`.
- `error: true` instead of `expected` if the call must fail.
- `source`: where the spelling comes from. Use a key from [docs/RULES.md](docs/RULES.md)
  (for example `IZOH` for izoh.uz, `IMLO` for imlo.uz, `RULES-1995 §17`), or a URL.
- `confidence: "unverified"` if you are not sure and no source settles it, with a `note`
  saying why.

Then run both suites (see below). If a case fails, that is a bug report, and a very good one.
Open a PR with just the case if you don't want to fix the code yourself.

**Good cases:** loanwords with ц, ъ, ь (*militsiya → милиция* is a known gap), all-caps text,
mixed scripts, real-world apostrophe mess, amounts from real invoices.

## 2. Add an exception word

Latin → Cyrillic can't recover ц/ъ/ь from rules alone. Words go in the exception lists in
**both** `python/src/uztext/_data.py` and `js/src/data.ts`, plus a corpus case, plus a row
in docs/RULES.md with its source. The tests fail if an exception has no corpus case.

## 3. Change a rule

Rules live in `python/src/uztext/_core.py` and `js/src/core.ts`, which mirror each other line for
line. Change both, add corpus cases, and cite the source in docs/RULES.md. Rules no source
confirms are marked **UNVERIFIED** in RULES.md, and their cases are tagged in the corpus.

## Running the tests

```sh
(cd python && PYTHONPATH=src python3 -m unittest discover -s tests -t .)
(cd js && npm install && npm test)
```

If you change `js/src` or `web/template.html`, rebuild the demo page:

```sh
(cd js && npm run build:web)
```

CI checks that `web/index.html` is up to date.

## New alphabet

The law approved by the Senate on 10 Sep 2026 is awaiting signature, and its spelling rules
are unpublished (see docs/ALPHABET.md). If you find the signed text or the new orthography
rules, please open an issue with the link. That is the single most valuable update right now.
