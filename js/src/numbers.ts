/** Amounts in words for invoices (sumWords). Mirrors python/src/uztext/_numbers.py. */

import { toCyrillic, toLatin, toNew } from "./core.js";
import { MAX_AMOUNT, ONES, SCALES, TENS, ZERO } from "./data.js";

export type Script = "latin" | "cyrillic" | "new";

export interface SumWordsOptions {
  /** Output script. Default "latin". */
  script?: Script;
  /** Currency name in current Latin (any apostrophe). Default "so'm"; "" drops it. */
  currency?: string;
  /** Subunit name. Default "tiyin"; "" drops it. */
  subunit?: string;
}

const SCRIPTS: Record<Script, (text: string) => string> = {
  latin: toLatin,
  cyrillic: toCyrillic,
  new: toNew,
};

const SPACES = /[    ]/g;
const DIGITS = /^[0-9]+$/;
const GROUPED = /^[0-9]{1,3}(?:[.,][0-9]{3})+$/;

/** Parse "1 250 000,50", "1,250,000.50", "1250000.5" -> [1250000, 50]. */
function parseString(raw: string): [number, number] {
  const bad = () => new RangeError(`not an amount: ${JSON.stringify(raw)}`);
  const s = raw.trim().replace(SPACES, "");
  const last = Math.max(s.lastIndexOf("."), s.lastIndexOf(","));
  let intPart = s;
  let frac = "";
  if (last >= 0 && s.length - last - 1 >= 1 && s.length - last - 1 <= 2) {
    intPart = s.slice(0, last);
    frac = s.slice(last + 1);
    if (!DIGITS.test(frac)) throw bad();
  }
  if (GROUPED.test(intPart) && !intPart.startsWith("0")) {
    // Thousands separators must all be the same character and must not be
    // the decimal separator.
    const seps = new Set(intPart.replace(/[0-9]/g, ""));
    if (seps.size !== 1 || (frac && seps.has(s[last]))) throw bad();
    intPart = intPart.replace(/[.,]/g, "");
  }
  if (!DIGITS.test(intPart)) throw bad();
  return [Number(intPart), frac ? Number(frac.padEnd(2, "0")) : 0];
}

/** Parse a canonical number string ("1250000.5") from a JS number. */
function parsePlain(s: string): [number, number] {
  const dot = s.indexOf(".");
  const intPart = dot < 0 ? s : s.slice(0, dot);
  let frac = dot < 0 ? "" : s.slice(dot + 1);
  if (!DIGITS.test(intPart) || (frac && !DIGITS.test(frac))) {
    throw new RangeError(`not an amount: ${JSON.stringify(s)}`);
  }
  frac = frac.replace(/0+$/, "");
  if (frac.length > 2) throw new RangeError(`more than two decimals: ${JSON.stringify(s)}`);
  return [Number(intPart), Number(frac.padEnd(2, "0"))];
}

function parse(amount: unknown): [number, number] {
  if (typeof amount === "number") {
    if (Number.isInteger(amount)) {
      if (amount < 0) throw new RangeError("amount must not be negative");
      return [amount, 0];
    }
    return parsePlain(String(amount));
  }
  if (typeof amount === "string") return parseString(amount);
  throw new TypeError("amount must be a number or a string");
}

function belowThousand(n: number): string[] {
  const words: string[] = [];
  const hundreds = Math.floor(n / 100);
  const rest = n % 100;
  if (hundreds) words.push(ONES[hundreds], "yuz");
  const tens = Math.floor(rest / 10);
  const ones = rest % 10;
  if (tens) words.push(TENS[tens]);
  if (ones) words.push(ONES[ones]);
  return words;
}

function intWords(n: number): string {
  if (n === 0) return ZERO;
  const words: string[] = [];
  for (const [value, name] of SCALES) {
    const group = Math.floor(n / value);
    n %= value;
    if (group) words.push(...belowThousand(group), name);
  }
  words.push(...belowThousand(n));
  return words.join(" ");
}

/**
 * Write an amount in Uzbek words, e.g. for an invoice.
 *
 *     sumWords("1 250 000,50") // "bir million ikki yuz ellik ming soʻm ellik tiyin"
 *
 * amount is a number or a string with up to two decimals ("," or "." as
 * decimal separator; spaces, "," or "." as thousands separators). The
 * integer part may be at most 999 999 999 999.
 */
export function sumWords(amount: number | string, options: SumWordsOptions = {}): string {
  const { script = "latin", currency = "so'm", subunit = "tiyin" } = options;
  if (!Object.prototype.hasOwnProperty.call(SCRIPTS, script)) {
    throw new RangeError(`script must be one of ${Object.keys(SCRIPTS).join(", ")}`);
  }
  const [whole, cents] = parse(amount);
  if (whole > MAX_AMOUNT) throw new RangeError(`amount must not exceed ${MAX_AMOUNT}`);
  const parts = [intWords(whole), currency];
  if (cents) parts.push(intWords(cents), subunit);
  return SCRIPTS[script](parts.filter((p) => p).join(" "));
}
