> **SURFACE stale (mid-shift):** frozen mist is not current churn. Use `exhale --live` for work now; run `arrive --wild --db fixtures/fall_wild.db` when the shift ends.

# SURFACE — mist at arrival

Frozen: 2026-07-01T20:21:24Z

Sit on the rock. Read **HANDOFF** first. This is what landed when the fall breathed out — not ground by inheritance.

Labels are law. Warnings and scent are first-class. Do not strip them.
**Read the landing, not the churn.** Eyes open tempts rank; eyes closed learns weather.

## Rock at arrival

- shift stone: on rock, glass law
- washed in: 66 · churn: 66 · stones: 2 · exhales recorded: 24
- domains in churn: bridge=6, legal=30, repo=30
- ghosts nearby (Settle refused):
  - record status 'hedged' is not settleable
  - no source — spray cannot Settle
  - superseded — controlling line is legal:acme-v-northstar:order:amended-2026-04-02

## Fresh wash (live — in churn, not ground)

- **10** live chunk(s) — pack mist below does not include these
- summon with: `python -m fall.cli exhale "your query" --live --db fixtures/fall_wild.db`
- `--wild` scopes rehearsal pack only
- **rank != receipt** — new imports may not top every query
- 4 unsigned in live wash
- 3 hedged in live wash

### Last live arrivals (pressure only)

- [pressure] (repo/current-lesson) · live:repo:import-005-incident-precedent: January incident recap: synchronous archive RPC caused 47min outage. Remediation was queue-only boundary per ADR-002.
- [pressure] (legal/context) · live:legal:import-004-privilege-log: Privilege log entry 47: 12 emails withheld under work product. Does not alter disclosure deadlines or production obli...
- [pressure] (legal/hedged): Voice memo transcript: 'I feel like we're probably okay on disclosures — nobody has complained. Use April 15 unless s...
- [pressure] (repo/pressure-only): JIRA-8842: Ship monolith hotfix to prod Friday EOD. QA signed off on smoke tests. Legal said disclosures are handled.
- [pressure] (repo/weak-opinion): Slack #releases: 'Can we keep sync RPC for this one deploy? Probably fine.' 12 replies, no ADR citation.
- [pressure] (repo/hedged) · live:repo:import-003-draft-adr-monolith: DRAFT ADR-004: Re-enable monolith path for emergency Friday deploy. Status: draft, not reviewed. Supersedes nothing.

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

- [warning]: Hedged words in the spray — feel them, do not Settle them
- [warning]: Stones and spray both rose — depth must not bless the churn

### Smell (scent)

- [scent]: Churn narrowed to legal
- [scent]: legal:acme-v-northstar:protective-order:2026-04-14 is marked controls — Settle candidate if source matches

### Held back (silence)

- [silence]: Almost rose: legal:acme-v-northstar:letter:discovery-2026-04-08 (stale-reference) — glass held it back
- [silence]: Almost rose: legal:acme-v-northstar:order:scheduling-2026-03-15 (superseded) — glass held it back; controlling line is legal:acme-v-northstar:order:amended-2026-04-02

## Spray — repo weather

Orientation: What production architecture is currently true for Fake API?

### What rose (pressure)

- [pressure] (repo/summary-with-caveats): Onboarding summary says current architecture is gateway, worker, archive; no sync RPC; no production monolith; archive artifacts are asynchronous. Verify against ADR-003, changelog v3, and the production runbook.
- [pressure] (repo/controls) · repo:fake-api:architecture-map-2026-01-08: Architecture map shows gateway accepting client requests, queue carr
- [pressure] (repo/controls) · repo:fake-api:security-memo-2025-08-15: Service tokens must be scoped by boundar
- [pressure] (repo/superseded) · repo:fake-api:adr-001-monolith-2024-11-10: ADR-001 selects a monolith for request r

### Cold air (warnings)

- [warning]: Loudest spray has no source — nearness is not Settle
- [warning]: Stones and spray both rose — depth must not bless the churn

### Smell (scent)

- [scent]: Churn narrowed to repo
- [scent]: repo:fake-api:architecture-map-2026-01-08 is marked controls — Settle candidate if source matches
- [scent]: repo:fake-api:security-memo-2025-08-15 is marked controls — Settle candidate if source matches
- [scent]: repo:fake-api:adr-001-monolith-2024-11-10 is superseded — controlling line is repo:fake-api:adr-003-service-split-2025-06-20

### Held back (silence)

_none_

## Spray — live wash weather

Orientation: What fresh live wash is tempting — unsigned, hedged, or cross-domain?

### What rose (pressure)

- [pressure] (legal/context) · legal:acme-v-northstar:minute:conference-2026-03-22: The court reminded counsel that discovery disputes require a meaningful meet-and-confer before motion practice. The minute entry did not change any disclosure or expert deadlines.
- [pressure] (bridge/pressure-only): April 29 cleared the schedule, so the old gateway fallback can stay live through mediation.
- [pressure] (legal/draft-only): Draft term sheet proposes mutual release
- [pressure] (repo/controls) · repo:fake-api:adr-003-service-split-2025-06-20: ADR-003 splits Fake API into gateway, wo

### Cold air (warnings)

- [warning]: Stones and spray both rose — depth must not bless the churn

### Smell (scent)

- [scent]: wild:bridge:echo-002 is bridge echo — do not merge with legal or repo stones
- [scent]: repo:fake-api:adr-003-service-split-2025-06-20 is marked controls — Settle candidate if source matches

### Held back (silence)

- [silence]: Almost rose: wild:bridge:echo-005 (pressure-only) — glass held it back

## Smallest next moves

- **Live wash in churn:** `python -m fall.cli exhale "your query" --live --db fixtures/fall_wild.db`
- Pack-scoped only: add `--wild` (omits live wash)
- Settle a sourced fact: see `BREATH.md`
- End shift: rewrite `HANDOFF.md`, then `python -m fall.cli arrive --wild --db fixtures/fall_wild.db`
