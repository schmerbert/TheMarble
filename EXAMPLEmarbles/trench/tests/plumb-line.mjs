#!/usr/bin/env node
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const tempRoot = await mkdtemp(path.join(os.tmpdir(), "trench-plumb-line-"));

async function seed() {
  await mkdir(path.join(tempRoot, "context-register"), { recursive: true });
  await mkdir(path.join(tempRoot, "field-notebook"), { recursive: true });
  await mkdir(path.join(tempRoot, "damage-record"), { recursive: true });

  await writeFile(
    path.join(tempRoot, "context-register", "bronze-pin.md"),
    "bronze pin lifted from Context 104 after full record"
  );
  await writeFile(
    path.join(tempRoot, "field-notebook", "bronze-pin-visible.md"),
    "bronze pin visible but relationship still unresolved"
  );
  await writeFile(
    path.join(tempRoot, "damage-record", "bronze-pin-old.md"),
    "bronze pin from prior trench has Broken Chain warning"
  );
}

function runPlumbLine() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [path.join(trenchRoot, "tools", "plumb-line.mjs"), "--query", "bronze pin"],
      { cwd: tempRoot }
    );

    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

try {
  await seed();
  const result = await runPlumbLine();
  if (result.code !== 0) {
    console.error("FAIL: Plumb Line failed.");
    console.error(result.stderr);
    process.exit(1);
  }

  for (const label of ["[Ground]", "[Pressure]", "[Warning]"]) {
    if (!result.stdout.includes(label)) {
      console.error(`FAIL: Plumb Line did not return ${label}.`);
      console.error(result.stdout);
      process.exit(1);
    }
  }

  console.log("PASS: Plumb Line returned labeled trench context.");
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}
