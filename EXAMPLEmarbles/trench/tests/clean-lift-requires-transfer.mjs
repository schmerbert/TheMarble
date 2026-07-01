#!/usr/bin/env node
import { access } from "node:fs/promises";
import { spawn } from "node:child_process";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const target = path.join(trenchRoot, "context-register", "bronze-pin-transfer-missing.md");

function runLiftWithoutTransfer() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "bronze pin transfer missing",
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
        "sealed below ash lens 103",
        "--recorder",
        "instance:second-pass",
        "--source",
        "field sheet FS-104",
        "--evidence",
        "context fields recorded",
        "--crossing",
        "Lift",
      ],
      { cwd: trenchRoot }
    );

    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (code) => resolve({ code, stderr }));
  });
}

async function exists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

const result = await runLiftWithoutTransfer();
const fileExists = await exists(target);

if (result.code === 0 || fileExists) {
  console.error("FAIL: clean Lift succeeded without physical transfer fields.");
  process.exit(1);
}

if (!result.stderr.includes("Lift Gate refusal")) {
  console.error("FAIL: write failed, but not through the Lift Gate.");
  console.error(result.stderr);
  process.exit(1);
}

console.log("PASS: clean Lift requires physical transfer fields.");
