/**
 * Transliteration, apostrophe normalisation and search keys.
 * Mirrors python/src/uztext/_core.py line for line. Any change here needs the
 * same change there and a corpus case that pins it.
 */

import {
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
} from "./data.js";

const LETTER = /^\p{L}$/u;

function isLetter(ch: string): boolean {
  return LETTER.test(ch);
}

function isUpper(ch: string): boolean {
  return ch !== ch.toLowerCase();
}

function isCased(ch: string): boolean {
  return ch.toLowerCase() !== ch.toUpperCase();
}

function has(table: object, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(table, key);
}

/**
 * Upper-case a multi-letter replacement for the capital at chars[i].
 * Ш becomes SH inside an all-caps word and Sh otherwise: the next cased
 * character decides; at the end of a word the previous one does.
 */
function upperMulti(lat: string, chars: readonly string[], i: number): string {
  if (Array.from(lat).length === 1) return lat.toUpperCase();
  let caps = false;
  if (i + 1 < chars.length && isCased(chars[i + 1])) {
    caps = isUpper(chars[i + 1]);
  } else if (i > 0 && isCased(chars[i - 1])) {
    caps = isUpper(chars[i - 1]);
  }
  return caps ? lat.toUpperCase() : lat[0].toUpperCase() + lat.slice(1);
}

/** Copy the casing pattern of src (lower, Title or UPPER) to repl. */
function applyCase(src: readonly string[], repl: string): string {
  const s = src.join("");
  if (src.length > 1 && s === s.toUpperCase() && s !== s.toLowerCase()) {
    return repl.toUpperCase();
  }
  if (src.length > 0 && isUpper(src[0])) {
    return repl[0].toUpperCase() + repl.slice(1);
  }
  return repl;
}

/** Split into [isWord, chunk] runs; words are maximal runs of letters. */
function words(chars: readonly string[]): Array<[boolean, string[]]> {
  const out: Array<[boolean, string[]]> = [];
  let start = 0;
  for (let i = 1; i <= chars.length; i++) {
    if (i === chars.length || isLetter(chars[i]) !== isLetter(chars[start])) {
      out.push([isLetter(chars[start]), chars.slice(start, i)]);
      start = i;
    }
  }
  return out;
}

function startsWith(word: readonly string[], stem: string): boolean {
  return word.join("").toLowerCase().startsWith(stem);
}

// ---------------------------------------------------------------------------
// Apostrophes

/**
 * Fix apostrophe look-alikes and Unicode composition.
 *  - NFC composition (O + combining diaeresis -> Ö).
 *  - Ș ș (comma below) -> Ş ş (cedilla).
 *  - Any look-alike after o/g -> U+02BB (oʻ, gʻ).
 *  - Any look-alike between two other letters -> U+02BC (tutuq belgisi).
 *  - Anything else (quotes around words, feet/minutes after digits) is kept.
 */
export function normalize(text: string): string {
  const chars = Array.from(
    text.normalize("NFC").replace(/Ș/g, "Ş").replace(/ș/g, "ş"),
  );
  const out: string[] = [];
  const n = chars.length;
  for (let i = 0; i < n; i++) {
    const ch = chars[i];
    if (APOSTROPHES.has(ch)) {
      const prev = i > 0 ? chars[i - 1] : "";
      const nxt = i + 1 < n ? chars[i + 1] : "";
      if (prev === "o" || prev === "O" || prev === "g" || prev === "G") {
        out.push(OKINA);
        continue;
      }
      if (prev && nxt && isLetter(prev) && isLetter(nxt)) {
        out.push(TUTUQ);
        continue;
      }
    }
    out.push(ch);
  }
  return out.join("");
}

// ---------------------------------------------------------------------------
// Cyrillic -> current Latin

function cyrScan(word: readonly string[], start: number): string {
  const out: string[] = [];
  const n = word.length;
  for (let i = start; i < n; i++) {
    const ch = word[i];
    const lc = ch.toLowerCase();
    const prev = i > 0 ? word[i - 1].toLowerCase() : "";
    const nxt = i + 1 < n ? word[i + 1].toLowerCase() : "";
    let lat: string;
    if (lc === "е") {
      lat = i === 0 || CYR_VOWELS.has(prev) || prev === "ъ" || prev === "ь" ? "ye" : "e";
    } else if (lc === "ц") {
      lat = CYR_VOWELS.has(prev) ? "ts" : "s";
    } else if (lc === "ъ") {
      // Dropped after ў (мўъжиза -> moʻjiza) and between a consonant and
      // е/ё/ю/я (объект -> obyekt); otherwise the tutuq (маъюс -> maʼyus).
      const iotated = ["е", "ё", "ю", "я"].includes(nxt) && !CYR_VOWELS.has(prev);
      lat = prev === "ў" || iotated ? "" : TUTUQ;
    } else if (lc === "ь") {
      lat = "";
    } else if (lc === "с" && nxt === "ҳ") {
      lat = "s" + TUTUQ;
    } else if (has(CYR_TO_LAT, lc)) {
      lat = CYR_TO_LAT[lc];
    } else {
      out.push(ch);
      continue;
    }
    if (ch !== lc && lat) lat = upperMulti(lat, word, i);
    out.push(lat);
  }
  return out.join("");
}

function cyrWord(word: readonly string[]): string {
  for (const [stem, repl] of CYR_PREFIX_EXCEPTIONS) {
    if (startsWith(word, stem)) {
      const len = Array.from(stem).length;
      return applyCase(word.slice(0, len), repl) + cyrScan(word, len);
    }
  }
  return cyrScan(word, 0);
}

function cyrToLat(text: string): string {
  return words(Array.from(text))
    .map(([w, c]) => (w ? cyrWord(c) : c.join("")))
    .join("");
}

// ---------------------------------------------------------------------------
// Current Latin -> Cyrillic

function latStartOrVowel(word: readonly string[], i: number): boolean {
  if (i === 0) return true;
  const prev = word[i - 1].toLowerCase();
  if (LAT_VOWELS.has(prev)) return true;
  return prev === OKINA && i >= 2 && word[i - 2].toLowerCase() === "o";
}

function latScan(word: readonly string[], start: number): string {
  const out: string[] = [];
  const n = word.length;
  let i = start;
  while (i < n) {
    const ch = word[i];
    const lc = ch.toLowerCase();
    const nxt = i + 1 < n ? word[i + 1].toLowerCase() : "";
    const nxt2 = i + 2 < n ? word[i + 2] : "";
    let step = 1;
    let cyr: string;
    if ((lc === "o" || lc === "g") && nxt === OKINA) {
      cyr = lc === "o" ? "ў" : "ғ";
      step = 2;
    } else if (lc === "s" && nxt === "h") {
      cyr = "ш";
      step = 2;
    } else if (lc === "c" && nxt === "h") {
      cyr = "ч";
      step = 2;
    } else if (lc === "y" && nxt === "e") {
      if (latStartOrVowel(word, i)) {
        cyr = "е";
        step = 2;
      } else {
        cyr = "й";
      }
    } else if (lc === "y" && (nxt === "a" || nxt === "o" || nxt === "u") && nxt2 !== OKINA) {
      cyr = ({ a: "я", o: "ё", u: "ю" } as Record<string, string>)[nxt];
      step = 2;
    } else if (lc === "e") {
      cyr = latStartOrVowel(word, i) ? "э" : "е";
    } else if (ch === TUTUQ) {
      const prev = i > 0 ? word[i - 1].toLowerCase() : "";
      cyr = prev === "s" && nxt === "h" ? "" : "ъ";
    } else if (has(LAT_TO_CYR, lc)) {
      cyr = LAT_TO_CYR[lc];
    } else {
      cyr = ch;
    }
    if (isUpper(ch)) cyr = cyr.toUpperCase();
    out.push(cyr);
    i += step;
  }
  return out.join("");
}

function latWord(word: readonly string[]): string {
  const lw = word.join("").toLowerCase();
  if (has(LAT_EXACT_EXCEPTIONS, lw)) return applyCase(word, LAT_EXACT_EXCEPTIONS[lw]);
  for (const [stem, repl] of LAT_PREFIX_EXCEPTIONS) {
    if (startsWith(word, stem)) {
      const len = Array.from(stem).length;
      return applyCase(word.slice(0, len), repl) + latScan(word, len);
    }
  }
  return latScan(word, 0);
}

function latToCyr(text: string): string {
  return words(Array.from(text))
    .map(([w, c]) => (w ? latWord(c) : c.join("")))
    .join("");
}

// ---------------------------------------------------------------------------
// Current Latin <-> new Latin

function curToNew(text: string): string {
  const chars = Array.from(text);
  const out: string[] = [];
  const n = chars.length;
  let i = 0;
  while (i < n) {
    const pair = (chars[i] + (i + 1 < n ? chars[i + 1] : "")).toLowerCase();
    if (has(CUR_TO_NEW, pair)) {
      const nw = CUR_TO_NEW[pair];
      out.push(isUpper(chars[i]) ? nw.toUpperCase() : nw);
      i += 2;
    } else {
      out.push(chars[i]);
      i += 1;
    }
  }
  return out.join("");
}

function newToCur(text: string): string {
  const chars = Array.from(text);
  return chars
    .map((ch, i) => {
      const lc = ch.toLowerCase();
      if (!has(NEW_TO_CUR, lc)) return ch;
      const cur = NEW_TO_CUR[lc];
      return ch !== lc ? upperMulti(cur, chars, i) : cur;
    })
    .join("");
}

// ---------------------------------------------------------------------------
// Public API

/** Any script -> current Latin (1995 alphabet). */
export function toLatin(text: string): string {
  return newToCur(cyrToLat(normalize(text)));
}

/** Any script -> Cyrillic. */
export function toCyrillic(text: string): string {
  return latToCyr(newToCur(normalize(text)));
}

/** Any script -> new Latin (Ö Ğ Ş Ç, Senate-approved 10 Sep 2026). */
export function toNew(text: string): string {
  return curToNew(cyrToLat(normalize(text)));
}

/** New Latin -> current Latin. Leaves Cyrillic untouched. */
export function fromNew(text: string): string {
  return newToCur(normalize(text));
}

/** Fold every script and apostrophe variant to one lower-case key. */
export function searchKey(text: string): string {
  return toNew(text).toLowerCase().split(TUTUQ).join("").split(OKINA).join("");
}
