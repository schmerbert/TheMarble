#!/usr/bin/env node
import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const args = { limit: "5" };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = "true";
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

async function walk(dir) {
  const entries = [];
  for (const item of await readdir(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      entries.push(...await walk(fullPath));
    } else if (item.isFile() && item.name.endsWith(".md")) {
      entries.push(fullPath);
    }
  }
  return entries;
}

function labelFor(filePath, root) {
  const relative = path.relative(root, filePath).replaceAll("\\", "/");
  if (relative.startsWith("context-register/")) return "Ground";
  if (relative.startsWith("damage-record/")) return "Warning";
  if (relative.startsWith("field-notebook/")) return "Pressure";
  if (relative === "SITE_BENCH.md" || relative.startsWith("site-bench/")) {
    return "Warning";
  }
  if (relative === "HANDOFF.md") return "Scent";
  return "Path";
}

function excerpt(content, query) {
  const lower = content.toLowerCase();
  const needle = query.toLowerCase();
  const index = lower.indexOf(needle);
  if (index === -1) return content.slice(0, 180).replace(/\s+/g, " ").trim();
  const start = Math.max(0, index - 70);
  const end = Math.min(content.length, index + query.length + 110);
  return content.slice(start, end).replace(/\s+/g, " ").trim();
}

async function readableMarkdownFiles(root) {
  const roots = [
    "context-register",
    "damage-record",
    "field-notebook",
    "site-bench",
    "SITE_BENCH.md",
    "HANDOFF.md",
    "MANIFEST.md",
    "BREATH.md",
  ];

  const files = [];
  for (const item of roots) {
    const fullPath = path.join(root, item);
    try {
      const info = await stat(fullPath);
      if (info.isDirectory()) files.push(...await walk(fullPath));
      if (info.isFile()) files.push(fullPath);
    } catch {
      // Young marbles may not have every region yet.
    }
  }
  return files;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.query) {
    throw new Error("Plumb Line requires --query.");
  }

  const root = path.resolve(process.cwd());
  const limit = Number.parseInt(args.limit, 10) || 5;
  const hits = [];

  for (const file of await readableMarkdownFiles(root)) {
    const content = await readFile(file, "utf8");
    if (!content.toLowerCase().includes(args.query.toLowerCase())) continue;
    hits.push({
      label: labelFor(file, root),
      file: path.relative(root, file).replaceAll("\\", "/"),
      excerpt: excerpt(content, args.query),
    });
  }

  for (const hit of hits.slice(0, limit)) {
    console.log(`[${hit.label}] ${hit.file}`);
    console.log(hit.excerpt);
    console.log("");
  }

  if (hits.length === 0) {
    console.log(`No Trench material found for: ${args.query}`);
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
