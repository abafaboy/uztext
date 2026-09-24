/**
 * uztext: Uzbek text toolkit for Cyrillic, current Latin and new Latin.
 *
 *     toLatin("Ўзбекистон") // "Oʻzbekiston"
 *     toNew("Oʻzbekiston")  // "Özbekiston"
 */
export { fromNew, normalize, searchKey, toCyrillic, toLatin, toNew } from "./core.js";
export { sumWords } from "./numbers.js";
export type { Script, SumWordsOptions } from "./numbers.js";
export const VERSION = "0.1.0";
