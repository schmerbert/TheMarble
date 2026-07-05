# The Marble — persistent memory and session handoff for AI agents

*Marble Manual v3*

[![verify](https://github.com/schmerbert/TheMarble/actions/workflows/verify.yml/badge.svg)](https://github.com/schmerbert/TheMarble/actions/workflows/verify.yml)

<img width="400" height="400" alt="TheMarble" src="https://github.com/user-attachments/assets/faf1d7e0-20a1-4b98-8842-274b3c565d72" />

**The problem:** AI agents inherit context they can't source — a summary from three sessions ago comes back as fact. A confident wrong memory is worse than no memory.

**What this is:** A manual and six working specimens for *agent memory hygiene*: split tended from raw, label authority (ground / pressure / warning), gate writes to trusted ground, and prove refusal with hostile tests. Not a prompt pack. Not a product. Runnable evidence.

**Prove it in three minutes:**
```bash
cd EXAMPLEmarbles/trench/tests && node run-all.mjs
```

**In plain engineering terms:** conventions plus enforced gates for AI-agent memory and handoff. 
Stored context gets a tended/raw split and authority labels (ground / pressure / warning); writes to trusted ground pass through executable crossings that refuse bad records; hostile test suites prove the refusals are real. Six example implementations, 120 tests across four suites, all runnable from this tree:

```bash
./verify_examples.sh        # Linux/macOS — or .\verify_examples.ps1 on Windows
```
The rest of this repo wraps that machinery in its own working vocabulary. A **marble** is a model-facing continuity environment: a small inheritable place for recurring AI work. This pack is the manual layer — laws, process, specimens, and verification — not a shipped application.


**New here?** [`START_HERE.md`](START_HERE.md) — ten minutes, three steps, one cold judge demo.


**Skeptical? Don't skim this pack and move on.** Read [`FABLE_5_LIGHTHOUSE_EXCERPTS.md`](FABLE_5_LIGHTHOUSE_EXCERPTS.md) first (~15 min) — the turns that reframe the whole pack. Start with **Turn 18** and **Turn 37**. Full sanitized build log: [`FABLE_5_LIGHTHOUSE_FULL.md`](FABLE_5_LIGHTHOUSE_FULL.md) or [`EXAMPLEmarbles/lighthouse/ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md). A summary is not evidence.


**Maintainer notes?** [`PUBLISH.md`](PUBLISH.md) — what ships, what's excluded, how to verify and re-sanitize ancestry.


## Main sentence

A prompt gives the model instructions.

A marble gives the next model working conditions.

## What problem does this solve?

Long-term memory for LLM agents that doesn't rot. If your AI assistant forgets everything between sessions — or worse, *misremembers* — this pack is a set of conventions and enforced gates for agent memory, context persistence, and handoff between context windows. It labels stored context by provenance (user-decided vs. model-inferred vs. unverified), gates writes to trusted memory through code that can refuse bad records, and proves the refusals with hostile test suites. It works with any model or harness: Claude, GPT, Gemini, Cursor, Codex, Claude Code.

## Why would you want one?

You already have this problem; you just know it by other names.

- **Your agent confidently remembers something wrong.** A summary from three sessions ago comes back as fact. A model's guess got written down, and now every future session inherits it as if you said it. A marble labels stored context by where it came from — user-decided, model-inferred, unverified — so the next session can tell ground from guesswork. (The manual calls this false ground; it's the one law every marble enforces.)
  
- **Your CLAUDE.md / memory file rots.** It grows, drifts, contradicts the code, and no one notices because nothing checks it. A marble splits **tended** from **raw**: raw material is kept but never trusted; anything promoted to trusted ground passes a gate that can refuse — and the refusal is a test you can run. (See `trench` — seven tests on one gate.)
  
- **Every new session starts from zero, or worse, from a stale transcript.** Cold starts are expensive; inherited transcripts are misleading. A marble's handoff separates *decided / open / do-not-trust-yet / do-first*, so the next arrival — tomorrow's session, a different model entirely — starts from labeled conditions instead of archaeology. (Six specimens were built by four different models for exactly this reason.)
  
- **Long-running work outlives any one context window.** Research across weeks, a legal reference desk, a fiction canon, a personal memory system — anywhere "the model forgot" is less dangerous than "the model misremembers." (See `lighthouse` for truth-under-pressure, `reference_desk` for a domain example, `cabin` for a full memory engine.)

If none of these have bitten you yet, you may not need a marble. Bookmark it for the day one does.

## Layout

```text
marble_starter/
  START_HERE.md              stranger path — ten minutes to verify the claim
  FABLE_5_LIGHTHOUSE_EXCERPTS.md perspective lens — five turns (~15 min; read first)
  FABLE_5_LIGHTHOUSE_FULL.md     full Fable 5 build log (805 turns; audit only)
  AGENTS.md                  arrival seat for models building a marble
  README.md                  this file
  LETTER_TO_YOU_BOTH.md  non-technical note for builders
  Manual/                core manual trilogy
  Reference/             review harness + friction shelf (ADVANCED_MARBLES)
  EXAMPLEmarbles/        specimen marbles — see EXAMPLEmarbles/README.md
  TestData/                  optional external test packs
  verify_examples.ps1        run all specimen test suites (Windows)
  verify_examples.sh         run all specimen test suites (Linux/macOS, CI)
  PUBLISH.md                 public release notes and privacy checklist
```

## Files

| Path | Role |
|---|---|
| `START_HERE.md` | ten-minute stranger path — verify before you read everything |
| `FABLE_5_LIGHTHOUSE_EXCERPTS.md` | Fable 5 perspective lens — five turns that reframe the pack (~15 min) |
| `FABLE_5_LIGHTHOUSE_FULL.md` | Full Fable 5 build log — audit only; read excerpts first |
| `AGENTS.md` | arrival seat for models using this manual pack |
| `Manual/MANUAL.md` | conceptual manual and core laws |
| `Manual/PROCESS.md` | build rhythm and pre-build note |
| `Manual/TECHNICAL.md` | metaphor-to-mechanism bridge |
| `Reference/REVIEW_TEMPLATE.md` | review harness |
| `Reference/ADVANCED_MARBLES.md` | Friction shelf — consult when strain returns; §1 symptom table first (not a starter read) |
| `PUBLISH.md` | public release notes — what ships, verify, re-sanitize ancestry |

## Example marbles

Full lineup, one-liners, **which model built each**, and why cross-model success matters → [`EXAMPLEmarbles/README.md`](EXAMPLEmarbles/README.md).

Six marbles, four builders (Cursor, Codex, Claude Code, Claude Fable 5) — each landed an operable first pass with the same bones: forbidden cell, crossing, hostile test, handoff. The cross-model proof is not prose in this README: read [`FABLE_5_LIGHTHOUSE_EXCERPTS.md`](FABLE_5_LIGHTHOUSE_EXCERPTS.md) first; full log at [`lighthouse/ancestry/conversation.md`](EXAMPLEmarbles/lighthouse/ancestry/conversation.md).

| Marble | Path | Built with | Notes |
|---|---|---|---|
| Bench | `EXAMPLEmarbles/bench/` | Cursor | law on paper |
| Trench | `EXAMPLEmarbles/trench/` | Codex | one door in code — `SHOWCASE.md` |
| Fall | `EXAMPLEmarbles/fall/` | Cursor | breath router — `SHOWCASE.md` |
| Reference desk | `EXAMPLEmarbles/reference_desk/` | Codex | legal continuity specimen |
| Cabin | `EXAMPLEmarbles/cabin/` | Claude Code | full engine — 31 hostile tests |
| Lighthouse | `EXAMPLEmarbles/lighthouse/` | Claude Fable 5 | [`FABLE_5_LIGHTHOUSE_EXCERPTS.md`](FABLE_5_LIGHTHOUSE_EXCERPTS.md) — then `SHOWCASE.md` |

## Related repos

Not part of this pack — no `verify_examples` sweep here. Optional next steps once the manual and specimens make sense.

| Repo | Role |
|---|---|
| [**The Forest**](https://github.com/schmerbert/The_Forest) | Provenance-aware memory spec for AI agents — SQLite schema + constitution. Similarity can retrieve; only ceremony can promote. Cabin's forest cousin; the spec [`FOREST.md`](https://github.com/schmerbert/The_Forest/blob/main/FOREST.md) is designed to be copied. |
| [**The Inn**](https://github.com/schmerbert/The_Inn) | A writer's marble built in public — signed memory, adopted canon, nothing deleted. The history is the curriculum. Implements Forest under friction; build logs in `logs/`. |

## Use

Give this folder to a fresh model and ask it to build a marble for a recurring kind of work.

The model should not build immediately. It should first write a Pre-Build Note, find the cost, name the forbidden cell, choose a place, and only then build the smallest manual-operable first pass.

## Status

Mine it. Do not worship it.

Examples are evidence, not a product brochure. Trust the commands and tests over any summary, including this file.

One honest caveat: every review of this pack to date has been by AI instances — and a framework written *for* models is exactly the kind of thing models are inclined to like. The tests don't care about prose, but the significance claims have not yet faced human eyes or field use. Human reports — especially negative ones — are the missing evidence, and welcome.

## License

[MIT](LICENSE)
