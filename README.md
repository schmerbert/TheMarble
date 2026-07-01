# Marble Manual v3

A manual pack for making marbles.

A marble is a model-facing continuity environment: a small inheritable place for recurring AI work.

This pack is the manual layer — laws, process, specimens, and verification — not a shipped application.

**New here?** [`START_HERE.md`](START_HERE.md) — ten minutes, three steps, one cold judge demo.

**Skeptical? Don't skim this pack and move on.** **Open** [`FABLE_5_LIGHTHOUSE_CONV.md`](FABLE_5_LIGHTHOUSE_CONV.md) — the sanitized build log from Claude Fable 5 (one day, cold arrival, compaction mid-session). The reading guide at the top names five turns; start with **Turn 18** and **Turn 37**. A summary is not evidence. Same text: [`EXAMPLEmarbles/lighthouse/ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md).

**Maintainer notes?** [`PUBLISH.md`](PUBLISH.md) — what ships, what's excluded, how to verify and re-sanitize ancestry.

## Main sentence

A prompt gives the model instructions.

A marble gives the next model working conditions.

## Layout

```text
marble_starter/
  START_HERE.md              stranger path — ten minutes to verify the claim
  FABLE_5_LIGHTHOUSE_CONV.md perspective lens — Fable 5 build log (read guide first)
  AGENTS.md                  arrival seat for models building a marble
  README.md                  this file
  LETTER_TO_YOU_BOTH.md  non-technical note for builders
  Manual/                core manual trilogy
  Reference/             review harness + advanced patterns
  EXAMPLEmarbles/        specimen marbles — see EXAMPLEmarbles/README.md
  TestData/                  optional external test packs
  verify_examples.ps1        maintainer: run all specimen test suites
  PUBLISH.md                 public release notes and privacy checklist
```

## Files

| Path | Role |
|---|---|
| `START_HERE.md` | ten-minute stranger path — verify before you read everything |
| `FABLE_5_LIGHTHOUSE_CONV.md` | Fable 5 build log — reading guide + five turns that reframe the whole pack |
| `AGENTS.md` | arrival seat for models using this manual pack |
| `Manual/MANUAL.md` | conceptual manual and core laws |
| `Manual/PROCESS.md` | build rhythm and pre-build note |
| `Manual/TECHNICAL.md` | metaphor-to-mechanism bridge |
| `Reference/REVIEW_TEMPLATE.md` | review harness |
| `Reference/ADVANCED_MARBLES.md` | horizon patterns (after first marble works) |
| `PUBLISH.md` | public release notes — what ships, verify, re-sanitize ancestry |

## Example marbles

Full lineup, one-liners, **which model built each**, and why cross-model success matters → [`EXAMPLEmarbles/README.md`](EXAMPLEmarbles/README.md).

Six marbles, five builders (Cursor, Codex, Claude Code, Claude Fable 5) — each landed an operable first pass with the same bones: forbidden cell, crossing, hostile test, handoff. The cross-model proof is not prose in this README: **open** [`lighthouse/ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md) and read it.

| Marble | Path | Built with | Notes |
|---|---|---|---|
| Bench | `EXAMPLEmarbles/bench/` | Cursor | law on paper |
| Trench | `EXAMPLEmarbles/trench/` | Codex | one door in code — `SHOWCASE.md` |
| Fall | `EXAMPLEmarbles/fall/` | Cursor | breath router — `SHOWCASE.md` |
| Reference desk | `EXAMPLEmarbles/reference_desk/` | Codex | legal continuity specimen |
| Cabin | `EXAMPLEmarbles/cabin/` | Claude Code | full engine — 31 hostile tests |
| Lighthouse | `EXAMPLEmarbles/lighthouse/` | Claude Fable 5 | **open** [`ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md) — then `SHOWCASE.md` |

## Use

Give this folder to a fresh model and ask it to build a marble for a recurring kind of work.

The model should not build immediately. It should first write a Pre-Build Note, find the cost, name the forbidden cell, choose a place, and only then build the smallest manual-operable first pass.

## Status

Mine it. Do not worship it.

Examples are evidence, not a product brochure. Trust the commands and tests over any summary, including this file.
