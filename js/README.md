# uztext (JavaScript / TypeScript)

Uzbek text toolkit for Cyrillic, current Latin (oʻ gʻ sh ch) and the new Latin alphabet
approved by the Senate on 10 Sep 2026 (Ö Ğ Ş Ç; awaiting the president's signature as of
24 Sep 2026). ESM + CommonJS, TypeScript types, zero runtime dependencies.

```js
import { toLatin, toCyrillic, toNew, fromNew, normalize, searchKey, sumWords } from "uztext";

toLatin("Ўзбекистон Республикаси");            // "Oʻzbekiston Respublikasi"
toNew("Oʻzbekiston, Toshkent shahri");         // "Özbekiston, Toşkent şahri"
sumWords("1 250 000,50", { script: "cyrillic" }); // "бир миллион икки юз эллик минг сўм эллик тийин"
```

The same behaviour ships as the Python package `uztext`, and both pass the shared corpus.
Full documentation, sources and limitations: <https://github.com/abafaboy/uztext>
