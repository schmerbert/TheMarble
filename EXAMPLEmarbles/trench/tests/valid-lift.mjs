#!/usr/bin/env node
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const tempRoot = await mkdtemp(path.join(os.tmpdir(), "trench-valid-lift-"));

function runValidLift() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "bronze pin",
        "--state",
        "lifted",
        "--context",
        "Context 104",
        "--layer",
        "brown silty layer",
        "--grid",
        "B4",
        "--coordinates",
        "x=12.44 y=7.20 z=1.36",
        "--relationship",
        "sealed below ash lens 103 and above floor 105",
        "--in_situ_status",
        "fully recorded in situ before removal",
        "--photo",
        "photo B4-104-017 with scale and north arrow",
        "--label",
        "TRB-B4-CTX104-F017",
        "--destination",
        "Find Tray 2",
        "--recorder",
        "instance:first-pass",
        "--source",
        "field sheet FS-104",
        "--evidence",
        "layer, grid, coordinates, and relationship recorded before removal",
        "--crossing",
        "Lift",
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
  const result = await runValidLift();
  if (result.code !== 0) {
    console.error("FAIL: valid Lift was refused.");
    console.error(result.stderr);
    process.exit(1);
  }

  const entry = await readFile(
    path.join(tempRoot, "context-register", "bronze-pin.md"),
    "utf8"
  );

  if (!entry.includes('crossing: "Lift"')) {
    console.error("FAIL: Lift entry did not record crossing.");
    process.exit(1);
  }

  if (!entry.includes("Context 104")) {
    console.error("FAIL: Lift entry did not record context.");
    process.exit(1);
  }

  if (!entry.includes("TRB-B4-CTX104-F017")) {
    console.error("FAIL: Lift entry did not record label.");
    process.exit(1);
  }

  console.log("PASS: valid Lift entered the Context Register.");
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}
