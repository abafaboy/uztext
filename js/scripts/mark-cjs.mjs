// dist/cjs sits inside a "type": "module" package, so tell Node its .js
// files are CommonJS.
import { writeFileSync } from "node:fs";

writeFileSync(
  new URL("../dist/cjs/package.json", import.meta.url),
  JSON.stringify({ type: "commonjs" }) + "\n",
);
