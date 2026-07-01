#!/usr/bin/env node
import { spawn } from "node:child_process";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const tests = [
  "visible-not-ready.mjs",
  "lifted-find-with-no-context-cut.mjs",
  "identification-does-not-outrank-context.mjs",
  "clean-lift-requires-transfer.mjs",
  "valid-lift.mjs",
  "broken-chain.mjs",
  "plumb-line.mjs",
];

for (const test of tests) {
  const result = await new Promise((resolve) => {
    const child = spawn(process.execPath, [path.join(trenchRoot, "tests", test)], {
      cwd: trenchRoot,
      stdio: "inherit",
    });
    child.on("close", (code) => resolve(code));
  });

  if (result !== 0) {
    process.exit(result);
  }
}
