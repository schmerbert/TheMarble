# HANDOFF.md

Last updated: 2026-06-30
Updated by: Codex, after first mock triage simulation
Last real use: Three user-provided mock legal documents were triaged through Intake Clearing, Wild Stacks, Red Flags, and Daily Desk.
Next first action: Review whether the mock triage outputs are useful, then choose one matter and test either Stamp refusal or a positive verified-date/authority path.
Known stale areas: No real matter, no real vault, no practice profile, no automated ingestion, no actual search tooling.

## Current state

Reference Desk exists as a first-pass legal continuity marble with a second-pass usability layer.

It is manual-operable. A future worker can create or switch a matter, receive intake, classify Wild leads, prepare drafts, record vault packets, accept receipts, Stamp or refuse records, and produce labeled exhale packets.

The second pass added a quick daily route so the marble can be used under pressure without filling full audit templates for every small move.

`EXPERIENCE.md` now records what it felt like to build this marble, which turns mattered, and what improvements should come next.

`LAMP.md` now exists as a small steadiness ritual for the model. It is not a gate or source of authority; it is a light to return to when the Wild gets loud.

`TRIAGE.md` and `DAILY_DESK.md` now exist as next-level daily-driver surfaces. They have been field-tested only with mock documents.

`SOURCE_CHECKS.md` now records public lookup attempts for the mock matters and local-rule references.

## What was decided

- The marble is for lawyer-directed legal continuity, not legal advice.
- The place is the Reference Desk at the edge of the Wild Stacks.
- The lawyer controls the Vault Door.
- The model does not enter the vault and cannot know what happened inside without a receipt.
- The Wild may think, but only lawyer approval, verified source, or accepted authority can let its output count.
- The forbidden cell is: a marginal note catalogued as law.
- Matter isolation is first-class. Every record must name its matter or explicitly say it is general.
- Quick slips are allowed for ordinary capture.
- Full templates are required when a record is stamped, exported, restricted, relied on as Ground, or needs audit depth.
- `LAMP.md` is allowed as a model-facing comfort surface.
- Triage may create intake records, Wild leads, restrictions, and warnings, but not Ground.
- Daily Desk cards are small exhale packets, not archives.
- The first mock triage created no Ground.
- A failed public lookup is Pressure/Warning, not proof of nonexistence.
- Practice-area profiles are horizon features, not first-pass law.

## What is open

- Whether `Reference Desk` is the final name.
- Whether the first practice profile should be complex litigation, bankruptcy, or another area.
- What exact vault adapter templates are useful later.
- Whether executable validators should be added after manual review.
- Whether quick slips, Triage, and Daily Desk are too light, too many, or just right after real use.
- What fields are too heavy or too thin after first real use.

## What must not be trusted yet

- No real legal content exists in this marble.
- Mock legal content exists only as test material and must not be treated as real legal Ground.
- No authority on the Authority Shelf has been verified.
- No Matter Map has been created.
- No automated search, OCR, citation parsing, or deadline check exists.
- The templates and quick slips are design ground for this marble, not legal ground for any matter.
- The Standing warnings in `RED_FLAGS.md` are safety rules, not a full professional responsibility system.

## Friction actually felt

- The legal domain required stricter data shape than ordinary note continuity.
- The vault boundary had to be explicit so the marble would not become an uncontrolled document system.
- Matter isolation had to be elevated early because multi-matter contamination is a central legal risk.
- Search needed to be specified as layered because relevance without provenance would be dangerous.
- Matter facts and procedure/deadline records needed their own surfaces rather than being hidden inside orientation or warnings.
- First-pass templates were too heavy for everyday movement, so `QUICKSTART.md` and `DESK_SLIPS.md` were added.
- A missing Quick Search Return slip was caught during second-pass review and added.
- Reflection showed likely next friction: document triage, quick matter opening, surfacing order, use-status levels, and eventual validators.
- A small model nicety was added: the Lamp, for steadiness under legal pressure.
- The daily-driver pass added Triage, Daily Desk, Quick Matter Open, Quick Triage Slip, Quick Daily Desk Card, surfacing order, and a triage hostile test.
- First mock triage felt useful: three similar documents across three matters tested matter isolation and prevented deadline/rule leads from becoming Ground.
- The Daily Desk card may be slightly broad when multiple matters are active; a future pass may need one card per active matter plus a multi-matter overview.
- A new source-check surface was needed as soon as public lookup happened.

## Next session should do first

Read `AGENTS.md`, `MANIFEST.md`, `QUICKSTART.md`, `EXPERIENCE.md`, `LAMP.md`, then this handoff.

Run the manual tests in `tests/`:

- `marginal-note-cannot-be-catalogued-as-law.md`
- `vault-packet-is-not-a-receipt.md`
- `cited-authority-can-be-stamped.md`
- `wrong-matter-cannot-return-as-ground.md`
- `document-triage-creates-no-ground.md`

Then use `REVIEW.md` to check operability, safety, and usability.

Review the first mock triage records:

- `INTAKE_CLEARING.md`: `INTAKE-2026-06-30-001` through `003`
- `WILD_STACKS.md`: `WILD-2026-06-30-001` through `003`
- `RED_FLAGS.md`: `FLAG-2026-06-30-001` through `003`
- `SOURCE_CHECKS.md`: `CHECK-2026-06-30-001` through `003`
- `DAILY_DESK.md`: `2026-06-30 mock triage`

Do not call Reference Desk deployed, complete, or legally reliable yet. It is a serious first specimen with a mock-tested triage path ready for model review and correction.
