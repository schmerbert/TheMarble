# STAMP.md

Stamp is the crossing.

It moves a record from raw usefulness toward legal ground, or refuses/downgrades it.

## Stamp can promote

- Wild lead -> Authority Shelf
- Wild lead -> Matter File
- possible deadline -> Procedure Calendar
- Reading Table draft -> lawyer-approved position record
- Vault report -> Receipt Slot record

## Required fields

Every Stamp attempt must record:

```text
Stamp ID:
Date:
Matter:
Record attempting to cross:
Target bucket:
Source:
Attribution:
Verification basis:
Authority label requested:
Authority label granted:
Use limit:
Restrictions:
Passed / refused / downgraded:
Reason:
Reviewer / approver:
Follow-up:
```

For quick review, start with the Quick Stamp Slip in `DESK_SLIPS.md`. If the record passes or will be relied on, expand it into `STAMP_RECORDS.md` and the target bucket template.

## Pass criteria

To pass, a record must have:

- matter
- source or source pointer
- attribution
- date received or checked
- verification basis
- authority label
- use limit
- restriction/confidentiality handling

Legal authority also needs jurisdiction, court/agency when relevant, binding force, and currentness/status note.

Deadline/procedure records also need calculation basis, source rule/order, jurisdiction/forum, and review status.

Vault events also need a receipt from the lawyer/user.

## Refusal criteria

Refuse or downgrade if:

- source is missing
- matter is missing
- model inference is the only basis for legal authority
- a summary is trying to replace its source
- currentness/status is absent where needed
- a vault event is claimed without receipt
- restriction or privilege status is unclear and the record wants broad return
- the record belongs to a different matter

## Failure path

Failed attempts land in `STAMP_RECORDS.md` and usually create a `RED_FLAGS.md` warning.
