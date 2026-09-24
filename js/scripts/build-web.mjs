// Inline the built ESM modules into web/template.html -> web/index.html,
// a single offline file. No bundler: the modules are concatenated in
// dependency order with their import/export syntax removed, inside an IIFE
// that exposes `uztext` as a global.
import { readFileSync, writeFileSync } from "node:fs";

const MODULES = ["data.js", "core.js", "numbers.js"];
const PUBLIC = ["toLatin", "toCyrillic", "toNew", "fromNew", "normalize", "searchKey", "sumWords"];

const dist = new URL("../dist/esm/", import.meta.url);
const body = MODULES.map((name) =>
  readFileSync(new URL(name, dist), "utf8")
    .replace(/^import[\s\S]*?from\s+"[^"]+";\n/gm, "")
    .replace(/^export (const|function) /gm, "$1 ")
    .replace(/^\/\/# sourceMappingURL=.*$/gm, "")
    .trim(),
).join("\n\n");

if (/^\s*(import|export)\b/m.test(body)) {
  throw new Error("build-web: leftover import/export in bundle");
}

const version = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")).version;
const bundle =
  `var uztext = (function () {\n"use strict";\n${body}\n` +
  `return { VERSION: ${JSON.stringify(version)}, ${PUBLIC.join(", ")} };\n})();`;

const template = readFileSync(new URL("../../web/template.html", import.meta.url), "utf8");
if (!template.includes("/*UZTEXT_BUNDLE*/")) throw new Error("build-web: placeholder missing");
writeFileSync(
  new URL("../../web/index.html", import.meta.url),
  template.replace("/*UZTEXT_BUNDLE*/", () => bundle),
);
console.log(`web/index.html written (uztext ${version})`);
