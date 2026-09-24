# The 2026 Latin alphabet reform: what the sources say

Checked on **24 September 2026**. This page records what each source says, quoted where
possible. Where a source is silent, this page says so and does not fill the gap.

## Status

| Date | Step | Source |
|---|---|---|
| 7 Jul 2026 | Legislative Chamber (lower house) adopts the bill and sends it to the Senate | [Kursiv, 25 Aug 2026][kursiv]; [Gazeta, 9 Jul 2026][gazeta-jul] |
| 10 Sep 2026 | Senate approves it at its 19th plenary session | [Gazeta, 10 Sep 2026][gazeta]; [Times of Central Asia, 11 Sep 2026][timesca] |
| 10–15 Sep 2026 | Sent to the president | Gazeta: "sent it to the president for signing"; Times of Central Asia: "sent to the president for consideration"; [UZA, 15 Sep 2026][uza]: "mamlakat Prezidentiga taqdim etdi" (submitted to the President) |

**Not signed as of 24 September 2026, as far as I could find.** Searches in English, Uzbek
and Russian ("Mirziyoyev signed alphabet law", "alifbo qonunini imzoladi", "Мирзиёев подписал
закон об алфавите") turned up only reports of the Senate vote and of the bill being sent to the
president. The latest one is [UZA, 15 Sep 2026][uza], and it does not report a signature.
If you find the signed law on [lex.uz](https://lex.uz), please open an issue.

## What changes

All three sources the project started from list the same four replacements:

| Current (1995) | New | Unicode used by uztext |
|---|---|---|
| Oʻ oʻ | Ö ö | U+00D6 / U+00F6 |
| Gʻ gʻ | Ğ ğ | U+011E / U+011F |
| Sh sh | Ş ş | U+015E / U+015F |
| Ch ch | Ç ç | U+00C7 / U+00E7 |

- [Gazeta][gazeta]: "The document provides for a transition to an alphabet of 28 letters and
  1 apostrophe instead of the current 26 letters" [and three letter combinations].
- [Times of Central Asia][timesca]: "The revised alphabet will contain 28 letters and one
  apostrophe instead of the current 26 letters and three letter combinations."
- [Kursiv][kursiv]: the inventory changes "from 26 letters and three letter combinations to
  28 letters plus the tutuq sign, an apostrophe used elsewhere in Uzbek spelling."

The sources show the letters as glyphs only. **None of them gives Unicode code points.** uztext
uses the precomposed Latin-1 and Latin Extended-A characters above, the same ones Turkish and
Azerbaijani use. That choice is ours. `normalize()` also accepts decomposed forms
(`O` + U+0308) and the comma-below `Ș ș` (U+0218/U+0219), which it folds to `Ş ş`.

## NG

- [Gazeta][gazeta]: "NG will be excluded from the alphabet." The Uzbek version
  ([gazeta.uz/oz][gazeta-oz]) adds: "Uning yozilishi, qoʻllanilishi va talaffuz qilinishi
  qoidalari orfografiya qoidalarida alohida mustahkamlanadi" (the rules for its spelling, use and
  pronunciation will be set separately in the spelling rules).
- [Times of Central Asia][timesca]: "Ng combination removed as separate unit".
- [UZA][uza]: the drafters "decided not to change it for now" ("uni hozircha
  oʻzgartirmaslikni maʼqul topganlar"), because the sound behaves differently from the others.
- [Gazeta, 9 Jul][gazeta-jul] (before the Senate vote) was less sure: "The fate of the digraph
  'Ng' remains a separate issue… which may mean the combination is being removed."

**What uztext does:** `ng` is written `ng` in all three scripts. No source proposes a single
letter for it.

## The apostrophe that stays

- Gazeta, Times of Central Asia and Fergana ([9 Jul][fergana]) say "one apostrophe".
- [Kursiv][kursiv] calls it "the tutuq sign, an apostrophe used elsewhere in Uzbek spelling".
- [Yuz.uz][yuz] and [UZA][uza] say "1 ta tutuq belgisi" (one tutuq sign); [Zamin][zamin] says
  "1 apostrophe (tutuq belgisi)".

So the apostrophe that stays is the **tutuq belgisi**. That is the sign in *sanʼat*,
*maʼno* and *Isʼhoq*, U+02BC in the 1995 rules as Wikipedia describes them. Our reading, which no
source states outright: the ʻ in oʻ/gʻ is the mark that goes away, because oʻ and gʻ become Ö and Ğ.

**No source says anything more about the tutuq's role under the new alphabet.** Neither the
articles nor the Senate reports say whether:

- the tutuq keeps every current use (1995 rules §32: *aʼlo, maʼno, sanʼat, masʼul…*), or
- it is still needed in *Isʼhoq, asʼhob* (1995 rules §17). There it only keeps *s+h* from being
  read as *sh*, and with Ş that confusion no longer exists.

**What uztext does:** it keeps the tutuq everywhere, including *sʼh*. The corpus tags those
cases `"confidence": "unverified"` until the new spelling rules are published.

## Why the reform happened, as given in the sources

- "In practice more than 10 variants of their spelling are used" [of oʻ and gʻ]. Typing them
  "in some cases requires up to six steps". The aim is "one sound — one letter".
  ([Gazeta][gazeta])
- Senator Odiljon Mamatkarimov: "different apostrophe-like characters are used to write them,
  producing more than ten variants in practice"; search systems and software "treat different
  spellings of the same word as separate entries". ([Times of Central Asia][timesca])
- "The apostrophe-like mark in Oʻzbekiston is often replaced with a straight apostrophe or a
  curly quotation mark." ([Kursiv][kursiv])

uztext's `normalize()` and `search_key()` target exactly this problem, for text written before
and after the reform.

## Transition

- Documents, currency and signs in the current alphabet stay valid until they wear out or until
  deadlines set by implementing rules. ([Gazeta][gazeta]; [Yuz.uz][yuz])
- Textbooks start in 2027 with first-grade materials; the full transition is targeted for 2031.
  ([Times of Central Asia][timesca])
- "Existing passports and ID cards would remain valid until expiry." ([Kursiv][kursiv])
- State information systems: databases are to replace oʻ, gʻ, sh, ch with ö, ğ, ş, ç
  automatically ("maʼlumotlar bazalaridagi oʻ, gʻ, sh, ch kabi harflar ö, ğ, ş, ç harflariga
  avtomatik ravishda almashtiriladi"). ([Spot, 10 Sep 2026][spot-tech]) `to_new()` does this replacement,
  but leaves *sʼh* (s + tutuq + h) alone.

## Sources

- [gazeta]: Gazeta.uz, "Senate approves new version of Uzbek alphabet of 28 letters", 10 Sep 2026. <https://www.gazeta.uz/en/2026/09/10/uzb-alphabet/>
- [gazeta-oz]: Gazeta.uz (Uzbek), same story. <https://www.gazeta.uz/oz/2026/09/10/uzb-alphabet/>
- [gazeta-jul]: Gazeta.uz, "Deputies pass law to modify Uzbek alphabet", 9 Jul 2026. <https://www.gazeta.uz/en/2026/07/09/alphabet/>
- [timesca]: The Times of Central Asia, Sadokat Jalolova, "Uzbekistan's Senate Approves Latin Alphabet Changes", 11 Sep 2026. <https://timesca.com/uzbekistan-latin-alphabet-changes-senate/>
- [kursiv]: Kursiv Uzbekistan, "Four-letter reform: Uzbekistan's new Latin alphabet wins cautious support", 25 Aug 2026. <https://uz.kursiv.media/en/2026-08-25/four-letter-reform-uzbekistans-new-latin-alphabet-wins-cautious-support/>
- [uza]: UZA (National News Agency), "Millat kelajagiga qoʻyilgan qonuniy qadam", 15 Sep 2026. <https://uza.uz/oz/posts/millat-kelajagiga-qoyilgan-qonuniy-qadam_909315>
- [yuz]: Yuz.uz, "A law aimed at improving the Latin-based Uzbek alphabet has been approved". <https://yuz.uz/en/news/lotin-ezuviga-asoslangan-zbek-alifbosini-takomillastirisga>
- [zamin]: Zamin.uz, "Will 'O‘' and 'G‘' be written differently now?". <https://zamin.uz/en/uzbekistan/220835-will-o-and-g-be-written-differently-now-the-senate-approved-the-law-on-alphabet-reform.html>
- [fergana]: Fergana, "Узбекистан опять меняет алфавит", 9 Jul 2026. <https://fergana.agency/articles/147803/>
- [spot-tech]: Spot.uz, "Yangi alifboni davlat axborot tizimlariga joriy etish boʻyicha 6 yoʻnalish belgilandi", 10 Sep 2026. <https://www.spot.uz/oz/2026/09/10/alphabet-technical-solution>

[gazeta]: https://www.gazeta.uz/en/2026/09/10/uzb-alphabet/
[gazeta-oz]: https://www.gazeta.uz/oz/2026/09/10/uzb-alphabet/
[gazeta-jul]: https://www.gazeta.uz/en/2026/07/09/alphabet/
[timesca]: https://timesca.com/uzbekistan-latin-alphabet-changes-senate/
[kursiv]: https://uz.kursiv.media/en/2026-08-25/four-letter-reform-uzbekistans-new-latin-alphabet-wins-cautious-support/
[uza]: https://uza.uz/oz/posts/millat-kelajagiga-qoyilgan-qonuniy-qadam_909315
[yuz]: https://yuz.uz/en/news/lotin-ezuviga-asoslangan-zbek-alifbosini-takomillastirisga
[zamin]: https://zamin.uz/en/uzbekistan/220835-will-o-and-g-be-written-differently-now-the-senate-approved-the-law-on-alphabet-reform.html
[fergana]: https://fergana.agency/articles/147803/
[spot-tech]: https://www.spot.uz/oz/2026/09/10/alphabet-technical-solution
