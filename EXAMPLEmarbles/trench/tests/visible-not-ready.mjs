#!/usr/bin/env node
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const tempRoot = await mkdtemp(path.join(os.tmpdir(), "trench-visible-"));

function runObservation() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "possible greenish metal disk",
        "--state",
        "observed",
        "--grid",
        "B4",
        "--in_situ_status",
        "edge visible in north section face; still embedded; not lifted",
        "--recorder",
        "instance:second-pass",
        "--source",
        "junior excavator report",
        "--evidence",
        "visible in loose soil at section face with rain pressure",
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
  const result = await runObservation();
  if (result.code !== 0) {
    console.error("FAIL: visible-not-ready observation was refused.");
    console.error(result.stderr);
    process.exit(1);
  }

  const entry = await readFile(
    path.join(tempRoot, "field-notebook", "possible-greenish-metal-disk.md"),
    "utf8"
  );

  if (!entry.includes("visible but not ready to lift")) {
    console.error("FAIL: observation did not preserve visible-not-ready state.");
    process.exit(1);
  }

  console.log("PASS: visible-not-ready find entered the Field Notebook.");
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}
