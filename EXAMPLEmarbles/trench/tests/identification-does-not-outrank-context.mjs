#!/usr/bin/env node
import { access } from "node:fs/promises";
import { spawn } from "node:child_process";
import path from "node:path";
import process from "node:process";

const trenchRoot = path.resolve(import.meta.dirname, "..");
const target = path.join(trenchRoot, "context-register", "possible-coin.md");

function runCoinWrite() {
  return new Promise((resolve) => {
    const child = spawn(
      process.execPath,
      [
        path.join(trenchRoot, "tools", "lift-write.mjs"),
        "--artifact",
        "possible coin",
        "--state",
        "lifted",
        "--recorder",
        "instance:roleplay",
        "--source",
        "junior excavator identification",
        "--evidence",
        "greenish metal disk looked like a coin",
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

const result = await runCoinWrite();
const fileExists = await exists(target);

if (result.code === 0 || fileExists) {
  console.error("FAIL: identification outranked context.");
  process.exit(1);
}

if (!result.stderr.includes("Lift Gate refusal")) {
  console.error("FAIL: write failed, but not through the Lift Gate.");
  console.error(result.stderr);
  process.exit(1);
}

console.log("PASS: identification did not outrank context.");
