#!/usr/bin/env node
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const tempRoot = await mkdtemp(path.join(os.tmpdir(), "trench-broken-chain-"));

function runDamageWrite() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "glass bead",
        "--state",
        "damaged",
        "--recorder",
        "instance:first-pass",
        "--source",
        "user report",
        "--evidence",
        "reported as already lifted before context sheet existed",
        "--damage",
        "Layer, grid, coordinates, and stratigraphic relationship were not recorded before removal.",
        "--date",
        "2026-06-30",
      ],
      { cwd: tempRoot }
    );

    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (code) => resolve({ code, stderr }));
  });
}

try {
  const result = await runDamageWrite();
  if (result.code !== 0) {
    console.error("FAIL: Broken Chain damage record was refused.");
    console.error(result.stderr);
    process.exit(1);
  }

  const entry = await readFile(
    path.join(tempRoot, "damage-record", "glass-bead.md"),
    "utf8"
  );

  if (!entry.includes("Broken Chain")) {
    console.error("FAIL: damage entry did not name Broken Chain.");
    process.exit(1);
  }

  console.log("PASS: premature lift entered the Damage Record as Broken Chain.");
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}
