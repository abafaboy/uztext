# Rules implemented, and where they come from

Each rule below names its source, using the keys in the corpus `source` field (listed at the end
of this page). Rules no source confirms are marked **UNVERIFIED**. Their corpus cases carry
`"confidence": "unverified"`, or the rule has no corpus case at all.

All functions accept text in any of the three scripts. They first run `normalize()`, then
convert.

## Cyrillic → current Latin (`to_latin`)

| Cyrillic | Latin | Rule | Source |
|---|---|---|---|
| а б в г д ж з и й к л м н о п р с т у ф х | a b v g d j z i y k l m n o p r s t u f x | one to one | WP, LAW-1995 |
| ё ю я | yo yu ya | always | WP |
| ч ш | ch sh | always | WP; RULES-1995 §17, §19 |
| ў қ ғ ҳ | oʻ q gʻ h | ʻ is U+02BB | WP |
| э | e | always | WP |
| е | **ye** at the start of a word, after a vowel, after ъ or ь; otherwise **e** | *yer, poyezd, obyekt, pyesa* / *kel, telefon* | WP ("Cyrillic Е е at the beginning of a word and after a vowel is Ye ye"); RULES-1995 §6, §25 |
| ц | **ts** after a vowel, otherwise **s** | *litsey, politsiya* / *sirk, konsert, aksiya* | WP ("rendered … as Ts ts after a vowel, otherwise as S s"); Latin headwords in IZOH |
| ъ | **ʼ** (U+02BC, tutuq belgisi) | *maʼno, sanʼat, eʼlon, maʼyus, Qurʼon* | RULES-1995 §32; KUN-2021 |
| ъ | dropped between a consonant and е/ё/ю/я | *объект → obyekt, субъект → subyekt, съезд → syezd* | IZOH, IMLO |
| ъ | dropped after ў | *мўъжиза → moʻjiza* | IMLO |
| ь | dropped | *ноль → nol, компьютер → kompyuter, ателье → atelye* | IZOH, IMLO |
| сҳ | **sʼh** | keeps *s+h* from being read as *sh*: *Исҳоқ → Isʼhoq, асҳоб → asʼhob* | RULES-1995 §17 ("Sh harflari ikki tovushni ifodalasa, ular orasiga ʼ tutuq belgisi qoʻyiladi: Isʼhoq, asʼhob") |
| сентябр-, октябр- | sentabr-, oktabr- | exception: no *y* | RULES-1995 §1 ("sentabr, noyabr kabi soʻzlarda"); IMLO |
| щ ы | shch, i | **UNVERIFIED**: not letters of the Uzbek alphabet. WP says Uzbek replaces them with шч and и, and we transliterate that replacement. No corpus case. | WP |

**Capitals.** A capital that becomes two Latin letters is written **SH** when the next letter
is a capital (or, at the end of a word, the previous one), and **Sh** otherwise.
So *ШАҲАР → SHAHAR*, *Шаҳар → Shahar*, *ТОШ → TOSH*, *Ш → Sh*. The same holds for Ch, Yo, Yu,
Ya, Ye, Ts and Sʼ. Oʻ/Gʻ need no such rule, since ʻ has no case. This follows from what the capitals
mean: all caps writes every letter as a capital, while title case capitalises only the first
letter of the digraph. No regulation spells it out (RULES-1995 §73 only covers sentence
capitalisation).

## Current Latin → Cyrillic (`to_cyrillic`)

This is the reverse of the table above, plus:

- **oʻ gʻ sh ch** → ў ғ ш ч. `yo yu ya` → ё ю я, except that *yoʻ* is й + ў (*yoʻl → йўл*).
- **ye** → е at the start of a word or after a vowel (*yer → ер, poyezd → поезд*).
  Otherwise *y* → й and *e* → е.
- **e** → **э** at the start of a word and after a vowel (*ekran → экран; poema → поэма,
  aerostat → аэростат*, RULES-1995 §7: "ae, oe … e yoziladi: aerostat, poema"), otherwise е.
- **ʼ** → ъ, except in **sʼh**, where it is dropped (*Isʼhoq → Исҳоқ*, RULES-1995 §17).
- **ts** → тс (*otsiz → отсиз*). The **ц** words can't be told apart by rule. *sirk* could be
  цирк or a native word, and *pensiya* has *-nsiya* but is пенсия. So they come from an explicit
  exception list, with sources:

| Latin | Cyrillic | Kind | Source |
|---|---|---|---|
| sirk | цирк | whole word (*sirka* "vinegar" is сирка) | IZOH |
| sex | цех | whole word | IZOH |
| nol | ноль | whole word (*nola* is нола) | IMLO |
| litsey, politsiya, stansiya, konsert, sement, federatsiya, aksiya, prinsip, kvitansiya, konstitutsiya, vitse- | лицей, полиция, станция, концерт, цемент, федерация, акция, принцип, квитанция, конституция, вице- | stem | IZOH |
| obyekt, subyekt, syezd | объект, субъект, съезд | stem | IZOH (Latin), IMLO (Cyrillic) |
| pyesa, atelye, kompyuter | пьеса, ателье, компьютер | stem | IZOH, IMLO |
| moʻjiza | мўъжиза | stem | IMLO |
| yanvar, fevral, aprel, iyun, iyul, sentabr, oktabr, noyabr, dekabr | январь, февраль, апрель, июнь, июль, сентябрь, октябрь, ноябрь, декабрь | stem | IMLO; RULES-1995 §1 |

A stem matches at the start of a word, and the rest of the word follows the normal rules:
*litseyda → лицейда*. For the ь-words this keeps ь before suffixes (*iyunda → июньда*), which
matches the case forms IMLO lists (*ательеда*, *июньда*). **UNVERIFIED** for suffixes IMLO
doesn't list, because IMLO's case forms look machine-generated.

Known gaps. Words outside the list come out letter by letter:

- An unlisted ц-word comes out with тс or с: *militsiya → милитсия* (should be милиция).
  *pensiya → пенсия* shows why no *-nsiya → -нция* rule is safe.
- Consonant + *ye* in an unlisted word gives йе (*podyezd → подйезд*, not подъезд).
  **UNVERIFIED** fallback.
- Vowel + *ye* gives е, which is wrong for *konveyer* (конвейер). The 1995 rules don't cover it.

Add words to the list with a source. See CONTRIBUTING.md.

## Current Latin ↔ new Latin (`to_new`, `from_new`)

| Current | New | Source |
|---|---|---|
| oʻ Oʻ | ö Ö | GAZETA, TIMESCA, KURSIV |
| gʻ Gʻ | ğ Ğ | GAZETA, TIMESCA, KURSIV |
| sh Sh SH | ş Ş Ş | GAZETA, TIMESCA, KURSIV |
| ch Ch CH | ç Ç Ç | GAZETA, TIMESCA, KURSIV |
| ng | ng (unchanged) | GAZETA ("NG will be excluded from the alphabet"); UZA ("hozircha oʻzgartirmaslik") |
| ʼ (tutuq) | ʼ (unchanged) | GAZETA, KURSIV, YUZ: "28 letters and one apostrophe / tutuq belgisi" |
| sʼh | sʼh (unchanged) | **UNVERIFIED**: see below |

`from_new` goes the other way, using the same capitals rule: *ŞAHAR → SHAHAR*, *Şahar → Shahar*.

**sʼh under the new alphabet: UNVERIFIED.** In current Latin the tutuq in *Isʼhoq* marks
*s + h*, not *sh*. With Ş as its own letter the new rules might drop that tutuq (*Ishoq*). They
are not published yet (GAZETA: rules "will be separately enshrined in spelling rules"). uztext
keeps the tutuq, which is lossless both ways. If the new rules drop it, `to_new` changes and
`from_new` would need to insert ʼ between *s* and *h*.

**Code points (our choice).** The sources show glyphs, not code points. uztext writes U+00D6/F6,
U+011E/1F, U+015E/5F and U+00C7/E7, and `normalize` folds Romanian-style Ș ș (U+0218/19) and
decomposed forms into them. That folding is a design choice (**UNVERIFIED**, tagged in the
corpus).

## Apostrophe normaliser (`normalize`)

The Unicode roles come from WP: *"the letters Oʻ and Gʻ are properly rendered using the character
U+02BB ʻ MODIFIER LETTER TURNED COMMA"* and the tutuq belgisi uses *"U+02BC ʼ MODIFIER LETTER
APOSTROPHE"*. WP also notes that U+2018, U+2019 and U+0027 are often used instead.

Look-alikes handled (12): `'` U+0027, `` ` `` U+0060, `´` U+00B4, `‘` U+2018, `’` U+2019,
`‛` U+201B, `ʻ` U+02BB, `ʼ` U+02BC, `ʹ` U+02B9, `ʽ` U+02BD, `′` U+2032, `＇` U+FF07.

1. Text is NFC-composed.
2. A look-alike right after **o/O/g/G** becomes **U+02BB**.
3. A look-alike **between two letters** becomes **U+02BC** (tutuq).
4. Anything else is left alone: quotes around words (*'Salom'*), feet after digits (*5'*).

Rule 2 assumes a tutuq never directly follows *o* or *g* in standard Latin spelling. Cyrillic
*ўъ* is written *oʻ* (*мўъжиза → moʻjiza*, IMLO), which supports this, but it is an inference
(**UNVERIFIED** as a general rule). A known false positive: an English quote ending in *o* or
*g* (*'go'*) gets U+02BB. Use `normalize` on Uzbek text.

## Search keys (`search_key`)

`search_key(text) = lower(to_new(text))` with every ʼ and ʻ removed. So *Oʻzbekiston,
O'zbekiston, O‘ZBEKISTON, Ўзбекистон, Özbekiston* all give `özbekiston`, and *sanʼat, san'at,
sanat, Санъат* all give `sanat`. This targets the problem officials gave as a reason for the
reform: more than ten apostrophe variants, which search systems treat as different words
(TIMESCA). The key is a design choice, not a spelling standard. It keeps ö/ğ/ş/ç distinct from
o/g/s/c, so *ot* (horse) and *oʻt* (fire) stay different.

## Amounts in words (`sum_words`)

| | |
|---|---|
| 1–9 | bir, ikki, uch, toʻrt, besh, olti, yetti, sakkiz, toʻqqiz (WB, with *yetti* per RULES-1995 §25) |
| 10–90 | oʻn, yigirma, oʻttiz, qirq, ellik, oltmish, yetmish, sakson, toʻqson (WB; *yigirma* per IZOH) |
| 100, 10³, 10⁶, 10⁹ | yuz, ming, million, milliard (WB) |
| 0 | nol (Cyrillic ноль, IMLO) |
| order | higher orders first, each numeral a separate word (WB: "In compound numerals the lower orders of numerals follow the higher. Each numeral is written separately") |
| *bir* before yuz/ming | always written: *bir yuz oʻn toʻqqiz* (119), *bir ming toʻqqiz yuz toʻqson ikki* (1992) (WB examples) |
| currency | soʻm = 100 tiyin; Cyrillic сўм, тийин (WP-SUM) |

Output: `<integer words> soʻm [<tiyin words> tiyin]`. The tiyin part is left out when it is
zero. Range: 0 to 999 999 999 999 soʻm, with up to two decimals. Cyrillic and new-Latin output
come from the Latin words through `to_cyrillic` and `to_new`.

**UNVERIFIED:** *bir* before a bare *yuz* or *ming* (100 → *bir yuz soʻm*, 1000 → *bir ming
soʻm*). WB only shows *bir* inside compounds, and OMNI lists bare *юз* and *минг* for 100 and
1000. I found no regulation on it. Those corpus cases are tagged.

### Source disagreements found

- **7 and 70.** WB spells them *etti*, *etmish*. RULES-1995 §25 has *yetti*, and Cyrillic етти
  → *yetti* by the е rule. uztext follows the 1995 rules.
- **20 in Cyrillic.** OMNI gives *ийгирма*; IZOH gives *ЙИГИРМА*. uztext gives йигирма.
- **100 / 1000.** OMNI lists bare *юз*, *минг*; WB uses *bir yuz*, *bir ming* in compounds.
  See above.
- **Cyrillic of loanwords.** IZOH's Cyrillic column is marked as produced by Lotin.uz. It gives
  *АТЕЛЕ* and *СЕЗД* where IMLO, a spelling dictionary, gives *ателье* and *съезд*. uztext takes
  Cyrillic spellings from IMLO and Latin headwords from IZOH.

## Sources (keys used in `corpus/cases.json`)

- **LAW-1995**: Law No. 71-I of 6 May 1995 amending the Law "On introducing the Uzbek alphabet based on the Latin script" (26 letters + 3 letter combinations). <https://lex.uz/docs/-116158>. Original law of 2 Sep 1993: <https://lex.uz/docs/-112286>
- **RULES-1995**: Cabinet of Ministers Resolution No. 339 of 24 Aug 1995, "Oʻzbek tilining asosiy imlo qoidalari" (main spelling rules). <https://lex.uz/docs/-1625271>
- **WP**: Wikipedia, "Uzbek alphabet" (correspondence table, footnotes on Е and Ц, Unicode notes). <https://en.wikipedia.org/wiki/Uzbek_alphabet>
- **IZOH**: Izoh.uz, explanatory dictionary of Uzbek. Latin headwords, e.g. <https://izoh.uz/word/sirk>, <https://izoh.uz/word/litsey>, <https://izoh.uz/word/obyekt>
- **IMLO**: Imlo.uz, Uzbek spelling dictionary. Cyrillic headwords, e.g. <https://imlo.uz/uz/word/mo%E2%80%98jiza>, <https://imlo.uz/uz/word/atelye>, <https://imlo.uz/uz/word/oktabr>
- **KUN-2021**: Ravshan Jomonov, "Ayirish (ъ) belgisi: oʻzbek tilidagi oʻrni va oʻzbek-lotin alifbosida ifodalanishi", Kun.uz, 21 Feb 2021. <https://kun.uz/news/2021/02/21/ayirish-belgisi-ozbek-tilidagi-orni-va-ozbek-lotin-alifbosida-ifodalanishi>
- **WB**: Wikibooks, "Uzbek/Numerals and Fractions". <https://en.wikibooks.org/wiki/Uzbek/Numerals_and_Fractions>
- **OMNI**: Omniglot, "Numbers in Uzbek". <https://www.omniglot.com/language/numbers/uzbek.htm>
- **WP-SUM**: Wikipedia, "Uzbekistani sum". <https://en.wikipedia.org/wiki/Uzbekistani_sum>
- **GAZETA, TIMESCA, KURSIV, UZA, YUZ**: reform coverage. See [ALPHABET.md](ALPHABET.md).
