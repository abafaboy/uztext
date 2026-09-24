// Run every case in corpus/cases.json against the built ESM package.
// One test per case, so the summary line counts corpus cases.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import * as uztext from "../dist/esm/index.js";
import * as data from "../dist/esm/data.js";

const corpus = JSON.parse(readFileSync(new URL("../../corpus/cases.json", import.meta.url), "utf8"));
const CASES = corpus.cases;

const TEXT_FNS = {
  to_latin: uztext.toLatin,
  to_cyrillic: uztext.toCyrillic,
  to_new: uztext.toNew,
  from_new: uztext.fromNew,
  normalize: uztext.normalize,
  search_key: uztext.searchKey,
};

function runCase(c) {
  if (c.fn === "sum_words") return uztext.sumWords(c.input, c.args ?? {});
  return TEXT_FNS[c.fn](c.input);
}

for (const c of CASES) {
  test(c.id, () => {
    if (c.error) {
      assert.throws(() => runCase(c), (e) => e instanceof RangeError || e instanceof TypeError);
    } else {
      assert.equal(runCase(c), c.expected, c.note);
    }
  });
}

test("corpus: ids unique", () => {
  const ids = CASES.map((c) => c.id);
  assert.equal(new Set(ids).size, ids.length);
});

test("corpus: every function covered", () => {
  assert.deepEqual(
    [...new Set(CASES.map((c) => c.fn))].sort(),
    [...Object.keys(TEXT_FNS), "sum_words"].sort(),
  );
});

test("corpus: every exception exercised", () => {
  const inputs = CASES.filter((c) => c.fn === "to_latin" || c.fn === "to_cyrillic").map((c) =>
    String(c.input).toLowerCase(),
  );
  const stems = [
    ...data.LAT_PREFIX_EXCEPTIONS.map(([s]) => s),
    ...Object.keys(data.LAT_EXACT_EXCEPTIONS),
    ...data.CYR_PREFIX_EXCEPTIONS.map(([s]) => s),
  ];
  for (const stem of stems) assert.ok(inputs.some((i) => i.includes(stem)), stem);
});

test("corpus: no stem is a prefix of another", () => {
  for (const table of [data.LAT_PREFIX_EXCEPTIONS, data.CYR_PREFIX_EXCEPTIONS]) {
    for (const [a] of table) for (const [b] of table) assert.ok(!(a !== b && b.startsWith(a)), `${a} ${b}`);
  }
});

test("api: exports and version", () => {
  const pkg = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));
  assert.equal(uztext.VERSION, pkg.version);
  assert.deepEqual(
    Object.keys(uztext).sort(),
    ["VERSION", "fromNew", "normalize", "searchKey", "sumWords", "toCyrillic", "toLatin", "toNew"],
  );
  assert.throws(() => uztext.sumWords(null), TypeError);
});
