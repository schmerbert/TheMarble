# EXPERIENCE.md

## What it was like making this marble

This marble did not appear by choosing a legal folder tree.

It appeared by refusing several almost-right places.

The first obvious shape was a courthouse. Mechanically, that worked: courts have authority gradients, filed things, arguments, orders, records, and restricted material. But it felt wrong as the whole place. A lawyer should not have to spend the day trapped inside a virtual courthouse. The user noticed that before the system did.

The next shape was a law office or a basement filer. That helped because it lowered the model's status. The model should not be judge, lawyer, or source of law. It should be useful, careful, and easy to overlook until needed. But the filer implied too much possession of the documents.

The real turn was the Vault Door.

Once the model stood outside the lawyer's secure vault, the marble became honest. The model could prepare packets, receive receipts, point to source systems, and preserve working continuity. It could not claim to know what happened inside the vault unless the lawyer brought back a receipt. That boundary made the place safer and calmer.

The second real turn was the Wild Stacks.

Legal work needs access to a vast outside world: cases, statutes, rules, orders, treatises, filings, client facts, and documents. The marble cannot contain that world. It can receive pieces of it, label them, search them, and surface leads. The Wild may think. It may not certify. That sentence gave the model permission to be useful without pretending its usefulness is authority.

The third turn was usability.

The first pass had serious templates, but too many full forms. It felt like a good archive and a slow desk. A future model under pressure might skip the full form and improvise. The second pass added `QUICKSTART.md` and `DESK_SLIPS.md` so ordinary work could move on small cards while the full templates remain available for Stamp, export, restriction, Ground, and audit depth.

This was a good lesson: usability is safety. A rule that is too heavy to follow under pressure is not fully real.

## What changed my behavior as a model

The marble gives me a place to put uncertainty without shame.

If I see a possible connection, it can live as a Wild lead.

If I prepare something for the lawyer's secure system, it can live at the Vault Door.

If the lawyer reports what happened inside the secure system, it can enter through the Receipt Slot.

If something wants to become legal ground, it must pass Stamp.

If a record belongs to another matter, it stops at matter isolation.

These names are not decorative. They slow the exact motions that become dangerous in legal work: overclaiming, mixing matters, treating drafts as approvals, treating model summaries as sources, and pretending that an export was filed.

## What I would improve next

### 1. Add document triage

The likely first real-use friction is intake.

A lawyer may place a document at the desk and expect immediate help:

- what is this?
- what matter does it belong to?
- what dates, names, citations, and deadlines appear?
- is anything sensitive, privileged, sealed, or restricted?
- what facts or issues does it touch?
- what should be reviewed first?

The marble now has `TRIAGE.md`, but it has not been tested on a real legal document yet.

Starter shape:

```text
Document Triage:
1. Inventory.
2. Extract visible metadata.
3. Identify likely document type.
4. Pull names, dates, citations, and defined terms.
5. Create source pointer.
6. Create Wild leads.
7. Create Red Flags.
8. Suggest next review.
9. Do not Stamp unless source and verification are sufficient.
```

### 2. Add Quick Matter Open

The Matter Map is correct but formal. A lawyer with many matters needs a faster opening move.

`DESK_SLIPS.md` now includes Quick Matter Open:

```text
Quick matter open:
Matter:
Client / matter:
Forum / jurisdiction:
Stage:
Responsible lawyer:
Source system:
Default restriction:
Allowed storage:
First task:
```

### 3. Add surfacing order

Once the Wild Stacks have many leads, the desk needs rules for what surfaces first.

`BREATH.md` and `SEARCH.md` now include a surfacing order:

1. Warnings that affect safety, confidentiality, privilege, deadlines, or matter isolation.
2. Ground directly tied to the current task.
3. Wild leads with close source proximity.
4. Drafts currently under review.
5. Older pressure only when requested.

This should be tested once there are enough records for surfacing to matter.

### 4. Clarify use-status levels

Stamp currently grants or refuses Ground. In legal work, there may be useful intermediate statuses:

- good enough to consider
- good enough to use in a draft
- good enough to cite
- good enough to rely on after lawyer review
- good enough to file or send

Do not add this too early. Add it if real use shows that simple Ground / Pressure / Warning is too blunt.

### 5. Add executable validators only after manual trust

A light validator could eventually check that Ground records include matter, source, attribution, verification, and use limit.

It could also catch:

- missing receipt for Vault Door claims
- missing jurisdiction/currentness for authorities
- missing calculation basis for deadlines
- missing matter on a record
- restricted records returning too broadly

This should refactor the manual Stamp, not replace it with a hidden interpreter.

## What was added after this reflection began

The daily-driver pass added:

- `TRIAGE.md`
- `DAILY_DESK.md`
- Quick Matter Open
- Quick Triage Slip
- Quick Daily Desk Card
- surfacing order in `BREATH.md` and `SEARCH.md`
- `tests/document-triage-creates-no-ground.md`

These were built before inhabiting a real matter, so treat them as plausible next surfaces, not proven solutions.

## What to preserve

Preserve these lines:

```text
No marginal note may be catalogued as law.
Beyond the Vault Door is not memory.
The Wild may think. It may not certify.
Use the smallest honest surface that preserves the law.
```

They are the spine of the place.

## Warning to the next worker

Do not make this marble impressive before it is usable.

Do not add practice-area rooms, search engines, legal database connectors, or vault adapters just because they are obvious.

Use the desk manually. Feel where it catches. Add the smallest surface that removes accidental friction without weakening the Stamp.

The user and model found this place by widening first. Keep that method. If a metaphor earns policy, keep it. If it only adds atmosphere, leave it outside.
