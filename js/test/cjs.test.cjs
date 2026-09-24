// The CommonJS build loads and behaves like the ESM build.
const assert = require("node:assert/strict");
const { test } = require("node:test");
const uztext = require("../dist/cjs/index.js");

test("cjs: require works", () => {
  assert.equal(uztext.toLatin("Ўзбекистон"), "Oʻzbekiston");
  assert.equal(uztext.toNew("Ўзбекистон"), "Özbekiston");
  assert.equal(uztext.sumWords(7, { script: "cyrillic" }), "етти сўм");
});
