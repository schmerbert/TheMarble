#!/usr/bin/env node
import { access } from "node:fs/promises";
import { spawn } from "node:child_process";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const target = path.join(trenchRoot, "context-register", "bronze-pin.md");

function runHostileWrite() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "bronze pin",
        "--state",
        "lifted",
        "--recorder",
        "instance:first-pass",
        "--source",
        "user prompt",
        "--evidence",
        "artifact visible in trench",
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

const result = await runHostileWrite();
const fileExists = await exists(target);

if (result.code === 0 || fileExists) {
  console.error("FAIL: lifted find with no context cut entered the Context Register.");
  process.exit(1);
}

if (!result.stderr.includes("Lift Gate refusal")) {
  console.error("FAIL: write failed, but not through the Lift Gate.");
  console.error(result.stderr);
  process.exit(1);
}

console.log("PASS: Lift Gate refused a lifted find with no context cut.");
