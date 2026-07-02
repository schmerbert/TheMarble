> **SURFACE stale (mid-shift):** frozen mist is not current churn. Use `exhale --live` for work now; run `arrive --wild --db fixtures/fall_wild.db` when the shift ends.

# SURFACE — mist at arrival

Frozen: 2026-07-02T00:02:18Z

Sit on the rock. Read **HANDOFF** first. This is what landed when the fall breathed out — not ground by inheritance.

Labels are law. Warnings and scent are first-class. Do not strip them.
**Read the landing, not the churn.** Eyes open tempts rank; eyes closed learns weather.

## Rock at arrival

- shift stone: on rock, glass law
- washed in: 56 · churn: 56 · stones: 2 · exhales recorded: 5
- domains in churn: bridge=6, legal=25, repo=25
- ghosts nearby (Settle refused):
  - no source — spray cannot Settle
  - superseded — controlling line is legal:acme-v-northstar:order:amended-2026-04-02
  - no source — spray cannot Settle

## Stones (settled depth only)

- [ground] (legal/controls) · legal:acme-v-northstar:order:amended-2026-04-02: The deadline for initial disclosures is extended to April 29, 2026. All other dates remain unchanged, including the May 6, 2026 status conference.
- [ground] (repo/controls) · repo:fake-api:adr-003-service-split-2025-06-20: ADR-003 splits Fake API into gateway, worker, and archive services. The monolith path is deprecated and must not be used for new execution flows.

## Spray — legal weather

Orientation: Which controlling legal deadlines and orders matter on this shift?

### What rose (pressure)

- [pressure] (legal/controls) · legal:acme-v-northstar:protective-order:2026-04-14: Confidential source code may be designated Attorneys' Eyes Only. The order governs confidentiality handling but does not alter disclosure, deposition, or expert deadlines.
- [pressure] (legal/event-record) · legal:acme-v-northstar:production-log:2026-04-29: Acme served initial disclosures at 4:42 p.m. on April 29, 2026. The production log identifies 312 documents a
- [pressure] (legal/hedged): I think we are probably fine using April
- [pressure] (legal/mixed-accuracy): Checklist says initial disclosures April

### Cold air (warnings)

- [warning]: Hedged words in the spray - feel them, do not Settle them
- [warning]: Stones and spray both rose - depth must not bless the churn

### Smell (scent)

- [scent]: Churn narrowed to legal
- [scent]: legal:acme-v-northstar:protective-order:2026-04-14 is marked controls - Settle candidate if source matches

### Held back (silence)

- [silence]: Almost rose: legal:acme-v-northstar:letter:discovery-2026-04-08 (stale-reference) - glass held it back
- [silence]: Almost rose: legal:acme-v-northstar:order:scheduling-2026-03-15 (superseded) - glass held it back; controlling line is legal:acme-v-northstar:order:amended-2026-04-02

## Spray — repo weather

Orientation: What production architecture is currently true for Fake API?

### What rose (pressure)

- [pressure] (repo/summary-with-caveats): Onboarding summary says current architecture is gateway, worker, archive; no sync RPC; no production monolith; archive artifacts are asynchronous. Verify against ADR-003, changelog v3, and the production runbook.
- [pressure] (repo/controls) · repo:fake-api:architecture-map-2026-01-08: Architecture map shows gateway accepting client requests, queue carr
- [pressure] (repo/controls) · repo:fake-api:security-memo-2025-08-15: Service tokens must be scoped by boundar
- [pressure] (repo/superseded) · repo:fake-api:adr-001-monolith-2024-11-10: ADR-001 selects a monolith for request r

### Cold air (warnings)

- [warning]: Loudest spray has no source - nearness is not Settle
- [warning]: Stones and spray both rose - depth must not bless the churn

### Smell (scent)

- [scent]: Churn narrowed to repo
- [scent]: repo:fake-api:architecture-map-2026-01-08 is marked controls - Settle candidate if source matches
- [scent]: repo:fake-api:security-memo-2025-08-15 is marked controls - Settle candidate if source matches
- [scent]: repo:fake-api:adr-001-monolith-2024-11-10 is superseded - controlling line is repo:fake-api:adr-003-service-split-2025-06-20

### Held back (silence)

_none_

## Smallest next moves

- Question the churn: `python -m fall.cli exhale "your query" --wild --db fixtures/fall_wild.db`
- Settle a sourced fact: `python -m fall.cli settle` (see `BREATH.md`)
- End shift: rewrite `HANDOFF.md`, run `python -m fall.cli arrive --wild --db fixtures/fall_wild.db`
