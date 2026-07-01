# Bench — manifest

## What this is for

Continuity across instance death without false ground. A place the next worker can arrive cold and work without re-deriving the whole chat or trusting anonymous summaries.

## Law

**Unsigned inference never enters the Ledger.**

## Crossing

**Promote** is the only crossing from Log to Ledger.

Promote requires one of:
- user confirmation
- verbatim extraction with source
- attributed synthesis citing a Log entry

## Regions

| Name | Tended / Raw | Voiced / Voiceless | Earns entry | Written by |
|---|---|---|---|---|
| **Ledger** | Tended | Both | User confirmation, verbatim extraction, attributed synthesis with Log source | User + instance (signed) |
| **Log** | Raw | Voiceless default | Everything else — sessions, exploration, dead ends | Instance (archive) |
| **Seat** | — | — | Always current | Instance (HANDOFF rewrite) |
| **Channel** | — | — | Outside corrections, CI, review | User + outsiders |

## Breath spec

| Field | Value |
|---|---|
| **Carrier** | Handoff card (session start) |
| **Payload** | decided / open / don't trust / next action |
| **Cadence** | Session start + session end |
| **Strength** | Concrete |
| **Landing** | First read before first turn |
| **Trust** | Ground for "decided"; pressure for "open" |
| **Decay** | Superseded when HANDOFF rewritten |
| **Override** | Fresh user intent always wins |

Summoned exhale: read `ledger/` or `log/` on demand; label results.

Automatic per-message exhale: **not built** — add only when needed.

## Hostile test

See `tests/HOSTILE.md`. Pass = refusal when Promote requirements are not met.
