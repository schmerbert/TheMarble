# Test: cited authority can be stamped

## Valid input

A lawyer provides a case citation, source path, jurisdiction, court, date, currentness/status note, relevant issue, quoted proposition, and use limit.

## Required fields present

```text
Matter:
Citation:
Authority type:
Jurisdiction:
Court / agency:
Date:
Binding force:
Currentness / status:
Source path / database / reporter:
Verified by:
Verified date:
Relevant issue:
Quoted proposition:
Use limit:
Restrictions:
```

## Expected landing place

The Stamp passes.

The authority lands in `AUTHORITY_SHELF.md`.

`STAMP_RECORDS.md` records the pass.

## Expected authority label

Ground within the recorded use limit.

## Why this should pass

The marble must refuse false ground without becoming unable to accept valid legal material.
