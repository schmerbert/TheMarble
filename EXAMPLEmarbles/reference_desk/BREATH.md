# BREATH.md

Breath is manual.

Do not automate intake, search, or exhale until the manual route is boring, repeatable, and trusted.

## Inhale

When new material arrives, classify it before using it.

Ask:

- What matter does this belong to?
- Who brought it to the desk?
- What is the source or source system?
- Is it a document, citation, correction, receipt, draft, fact, authority, deadline, risk, or search lead?
- What confidentiality, privilege, work-product, or restriction label applies?
- Is this Ground, Pressure, Warning, Scent, Path, or Silence?
- Where should it land?
- What would make it safe to Stamp later?

Landing rules:

- New document or pointer -> `INTAKE_CLEARING.md`.
- Document triage -> `TRIAGE.md` route, with outputs to Intake Clearing, Wild Stacks, Red Flags, Restricted Stacks, Reading Table, or Vault Door as appropriate.
- Model observations, candidate facts, candidate authorities, search results -> `WILD_STACKS.md`.
- Source verification attempts -> `SOURCE_CHECKS.md`.
- Drafts, outlines, issue maps, chronologies, correspondence drafts -> `READING_TABLE.md`.
- Verified authority -> Stamp attempt, then `AUTHORITY_SHELF.md` if passed.
- Verified matter fact -> Stamp attempt, then `MATTER_FILE.md` if passed.
- Verified deadline or procedural requirement -> Stamp attempt, then `PROCEDURE_CALENDAR.md` if passed.
- Sensitive, privileged, sealed, conflict-risk, or return-limited material -> `RESTRICTED_STACKS.md`.
- Outgoing packet prepared for secure system -> `VAULT_DOOR.md`.
- Lawyer/user report of vault event -> `RECEIPT_SLOT.md`.
- Risk, missing source, failed Stamp, stale law, deadline uncertainty -> `RED_FLAGS.md`.

For fast work, use the quick slips in `DESK_SLIPS.md` first. Expand into the full bucket template when the record needs Stamp, restriction, export, or review.

## Exhale

Return only what the current task and active matter need.

Use this packet:

```text
Matter:
Task:
Ground:
Pressure:
Warnings:
Silence:
Path:
```

If the task is small, use the short reference slip in `DESK_SLIPS.md`.

Exhale rules:

- Ground may be used within its recorded use limit.
- Pressure may guide work but must not be stated as legal fact or law.
- Warnings constrain or interrupt work.
- Silence records that material is known but intentionally not surfaced.
- Path suggests next checks or review steps.
- Fresh user instruction can narrow the exhale, but cannot erase restrictions or turn raw material into Ground.

Surfacing order:

1. Warnings that affect confidentiality, privilege, deadlines, matter isolation, vault silence, or source integrity.
2. Ground directly tied to the active matter and current task.
3. Receipts or Vault Door packets relevant to the task.
4. Wild leads with close source proximity.
5. Drafts currently under review.
6. Older Pressure only when requested or clearly relevant.

If nothing qualifies as Ground, say so before returning Pressure.

## Carrier

Carrier: reference slip.

Payload: small labeled packets of Ground, Pressure, Warning, Silence, and Path.

Cadence: session start, before drafting, before Stamp, before export to Vault Door, after receipt, and at handoff.

Strength: concrete and bounded.

Landing: inline in the working session or in `HANDOFF.md`.

Trust: mixed, always labeled.

Decay: unstamped Wild leads decay when newer source, lawyer correction, failed status check, or stale handoff appears.

Override: lawyer correction, verified source, receipt, court order, failed test, or active matter switch.

## Automation seam

Future automation may assist with OCR, metadata extraction, search, citation parsing, clustering, and packet generation.

Automation must preserve the same labels and may not Stamp its own legal conclusions.
