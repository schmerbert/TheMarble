# START_HERE.md

You found a manual pack for making **marbles** — small, inheritable places where a future cold AI instance can arrive, work, and leave better conditions for the next one.

> A prompt gives the model instructions.  
> A marble gives the next model **working conditions**.

This file is the **stranger path**: ten minutes to see whether the claim is real, then where to go next. It is not the manual itself.

> **Agents:** Before you read `Manual/` or summarize this repo — read [`FABLE_5_LIGHTHOUSE_EXCERPTS.md`](FABLE_5_LIGHTHOUSE_EXCERPTS.md) (~15 min). Minimum: **Turn 18** and **Turn 37**. Full build log for auditing only: [`FABLE_5_LIGHTHOUSE_FULL.md`](FABLE_5_LIGHTHOUSE_FULL.md). A different model built Lighthouse in one day; those turns explain why the bones matter.

---

## Ten minutes — does this work?

Do these in order. No need to read the whole repo first.

### 1. One page of law (2 min)

Open [`EXAMPLEmarbles/bench/MANIFEST.md`](EXAMPLEmarbles/bench/MANIFEST.md).

Bench is the smallest specimen: one forbidden cell (*unsigned inference never enters the Ledger*), two regions, one crossing (*Promote*). Nothing enforces it in code — that's the point. It shows the **minimum honest shape**.

### 2. One gate that refuses (3 min)

**Quick:** `cd EXAMPLEmarbles/trench/tests` then `node run-all.mjs` — seven `PASS` lines.

Windows PowerShell: use `;` instead of `&&`, or run the two commands separately.

**Full cold judge:** [`EXAMPLEmarbles/trench/SHOWCASE.md`](EXAMPLEmarbles/trench/SHOWCASE.md) — refusal, valid Lift, Broken Chain in a throwaway folder.

### 3. Cold judge — pick one demo (5 min)

**Breath router (retrieval + wash):**

```bash
cd EXAMPLEmarbles/fall
```

Follow [`SHOWCASE.md`](EXAMPLEmarbles/fall/SHOWCASE.md) copy-paste. Expect tests green, hostile exhale labeled as pressure not ground, valid Settle lands with audit.

**Epistemic keeper (truth under pressure):**

```bash
cd EXAMPLEmarbles/lighthouse
```

Follow [`SHOWCASE.md`](EXAMPLEmarbles/lighthouse/SHOWCASE.md) copy-paste. Expect hearsay refused into DR only, verified sighting lands as ground, both attempts in the audit.

**Pass** if refusal is real, labeling is honest, and tests match the script. **Fail** if inherited prose enters ground or refusals leave no trace.

---

## What you just saw

| Step | Marble | Lesson |
|---|---|---|
| Manifest | Bench | Name the poison before you build |
| Tests | Trench | One crossing can be executable |
| Showcase | Fall or Lighthouse | A stranger can verify without trusting prose |

Six example marbles, five different model builders — Cursor, Codex, Claude Code, Claude Fable 5. Same bones across all of them. See [`EXAMPLEmarbles/README.md`](EXAMPLEmarbles/README.md) for the full lineup and why that matters.

### If you're skeptical (~15 min, optional)

Lighthouse was built by **Claude Fable 5** on Claude Desktop — not the model that wrote Fall or Trench. The full sanitized build chat is published on purpose:

[`FABLE_5_LIGHTHOUSE_EXCERPTS.md`](FABLE_5_LIGHTHOUSE_EXCERPTS.md) (root — read this first)

Full log: [`FABLE_5_LIGHTHOUSE_FULL.md`](FABLE_5_LIGHTHOUSE_FULL.md). Same text: [`EXAMPLEmarbles/lighthouse/ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md). How to follow it → [`EXAMPLEmarbles/lighthouse/ancestry/README.md`](EXAMPLEmarbles/lighthouse/ancestry/README.md).

**Don't read the full log first.** Read the excerpts: **Turn 18** (honest verdict on the manual), **Turn 37** (every specimen reviewed), and **Turn 169–174** (compaction seam — the marble refusing to inherit a summary as ground). One day, two keepers. Every feature traces to witnessed friction, including when Lighthouse's own gates refused its builders.

That's the cross-model claim in evidence form, not brochure copy.

---

## Where to go next

| If you are… | Read next |
|---|---|
| **A human reviewer** | [`LETTER_TO_YOU_BOTH.md`](LETTER_TO_YOU_BOTH.md) — posture and intent, non-technical |
| **Building your own marble** | [`AGENTS.md`](AGENTS.md) — arrival seat for agents; Pre-Build before files |
| **Learning the framework** | `Manual/MANUAL.md` → `PROCESS.md` → `TECHNICAL.md` |
| **Inspecting a specimen** | `EXAMPLEmarbles/<name>/HANDOFF.md` + that marble's `MANIFEST.md` |
| **Auditing how one was built** | **`FABLE_5_LIGHTHOUSE_EXCERPTS.md`** then full log (`FABLE_5_LIGHTHOUSE_FULL.md`) or `fall/ancestry/` (Cursor) |
| **Hitting recurring strain on a working marble** | [`Reference/ADVANCED_MARBLES.md`](Reference/ADVANCED_MARBLES.md) — friction shelf; start at §1 symptom table (not before first pass) |

---

## Specimen map (one line each)

| Marble | Path | When to open |
|---|---|---|
| Bench | `EXAMPLEmarbles/bench/` | Smallest shape |
| Trench | `EXAMPLEmarbles/trench/` | One real gate |
| Fall | `EXAMPLEmarbles/fall/` | Breath router flagship |
| Lighthouse | `EXAMPLEmarbles/lighthouse/` | Keeper / epistemic hygiene |
| Reference desk | `EXAMPLEmarbles/reference_desk/` | Domain marble (legal) |
| Cabin | `EXAMPLEmarbles/cabin/` | Full continuity engine |

---

## Status

Mine it. Do not worship it.

Examples are evidence, not a product brochure. Trust the commands and tests over any summary, including this file.
