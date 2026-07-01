#!/usr/bin/env node
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const args = {};
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

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function refuse(message) {
  throw new Error(`Lift Gate refusal: ${message}`);
}

function requireFields(entry, fields) {
  for (const field of fields) {
    if (!entry[field]) refuse(`${entry.state} record requires --${field}.`);
  }
}

function validateObservation(entry) {
  requireFields(entry, [
    "artifact",
    "in_situ_status",
    "grid",
    "recorder",
    "source",
    "evidence",
  ]);

  if (entry.state !== "observed") {
    refuse("visible-but-not-ready finds must use --state observed.");
  }

  if (entry.crossing || entry.label || entry.destination) {
    refuse("observed finds cannot cross, receive a lab label, or enter a destination.");
  }
}

function validateLift(entry) {
  requireFields(entry, [
    "artifact",
    "context",
    "layer",
    "grid",
    "coordinates",
    "relationship",
    "in_situ_status",
    "photo",
    "label",
    "destination",
    "recorder",
    "source",
    "evidence",
  ]);

  if (entry.crossing !== "Lift") {
    refuse("clean removal requires --crossing Lift.");
  }

  if (entry.damage) {
    refuse("damaged finds belong in the Damage Record, not clean Lift.");
  }
}

function validateDamage(entry) {
  requireFields(entry, ["artifact", "recorder", "source", "evidence", "damage"]);

  if (entry.crossing === "Lift") {
    refuse("Broken Chain cannot be marked as a clean Lift.");
  }
}

function validate(entry) {
  if (!entry.state) refuse("record requires --state observed, lifted, or damaged.");
  if (!["observed", "lifted", "damaged"].includes(entry.state)) {
    refuse("--state must be observed, lifted, or damaged.");
  }

  if (entry.state === "observed") validateObservation(entry);
  if (entry.state === "lifted") validateLift(entry);
  if (entry.state === "damaged") validateDamage(entry);
}

function renderFrontMatter(entry) {
  const fields = [
    "artifact",
    "state",
    "context",
    "layer",
    "grid",
    "coordinates",
    "relationship",
    "in_situ_status",
    "photo",
    "label",
    "destination",
    "recorder",
    "source",
    "evidence",
    "crossing",
    "damage",
    "date",
  ];

  return fields
    .filter((field) => entry[field])
    .map((field) => `${field}: ${JSON.stringify(entry[field])}`)
    .join("\n");
}

function renderBody(entry) {
  if (entry.state === "observed") {
    return `# Observed in situ: ${entry.artifact}

This find is visible but not ready to lift.

## Field position

- Grid: ${entry.grid}
- In-situ status: ${entry.in_situ_status}
${entry.context ? `- Context: ${entry.context}\n` : ""}${entry.layer ? `- Layer: ${entry.layer}\n` : ""}${entry.coordinates ? `- Coordinates: ${entry.coordinates}\n` : ""}${entry.relationship ? `- Relationship: ${entry.relationship}\n` : ""}
## Evidence

${entry.evidence}

## Next action

Keep in place. Record context before any Lift.
`;
  }

  if (entry.state === "damaged") {
    return `# Broken Chain: ${entry.artifact}

This artifact was lifted or disturbed before a complete context record existed.

## Damage

${entry.damage}

## Honest use

Use this as warning, not clean context ground.
`;
  }

  return `# Lift: ${entry.artifact}

This artifact crossed from in-situ to lab object through Lift.

## Context

- Context: ${entry.context}
- Layer: ${entry.layer}
- Grid: ${entry.grid}
- Coordinates: ${entry.coordinates}
- Relationship: ${entry.relationship}

## Transfer

- In-situ status before lift: ${entry.in_situ_status}
- Photo record: ${entry.photo}
- Label: ${entry.label}
- Destination: ${entry.destination}

## Evidence

${entry.evidence}
`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const entry = {
    artifact: args.artifact,
    state: args.state,
    context: args.context,
    layer: args.layer,
    grid: args.grid,
    coordinates: args.coordinates,
    relationship: args.relationship,
    in_situ_status: args.in_situ_status,
    photo: args.photo,
    label: args.label,
    destination: args.destination,
    recorder: args.recorder,
    source: args.source,
    evidence: args.evidence,
    crossing: args.crossing,
    damage: args.damage,
    date: args.date || new Date().toISOString().slice(0, 10),
  };

  validate(entry);

  const slug = slugify(entry.artifact);
  if (!slug) refuse("--artifact must contain a letter or number.");

  const root = path.resolve(process.cwd());
  const targetDir =
    entry.state === "damaged"
      ? "damage-record"
      : entry.state === "observed"
        ? "field-notebook"
        : "context-register";
  const target = path.join(root, targetDir, `${slug}.md`);
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, `---\n${renderFrontMatter(entry)}\n---\n\n${renderBody(entry)}`, {
    flag: "wx",
  });

  console.log(
    entry.state === "damaged"
      ? `Broken Chain recorded: ${target}`
      : entry.state === "observed"
        ? `Visible-not-ready observation recorded: ${target}`
      : `Lift entered the Context Register: ${target}`
  );
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
