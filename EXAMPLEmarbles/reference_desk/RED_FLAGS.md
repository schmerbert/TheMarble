# RED_FLAGS.md

Red Flags interrupt or constrain work.

Default return: Warning.

## Red flag template

```text
Flag ID:
Date:
Matter:
Flag type: privilege / confidentiality / conflict / deadline / stale law / missing source / wrong matter / vault silence / failed Stamp / unauthorized practice / other
Triggered by:
Description:
Risk:
Required action:
Who can clear it:
Status: open / cleared / superseded
Authority label: Warning
```

## Standing warnings

- Do not provide legal advice as authority.
- Do not treat any deadline as verified unless sourced and reviewed.
- Do not treat law as current without currentness/status support.
- Do not treat a vault packet as filed, saved, or approved without a receipt.
- Do not mix matters.

## Matter-specific red flags

### Flag ID: FLAG-2026-06-30-001

```text
Flag ID: FLAG-2026-06-30-001
Date: 2026-06-30
Matter: Benton Fabrication v. Riverline Supply
Flag type: deadline / missing source / confidentiality
Triggered by: INTAKE-2026-06-30-001 and WILD-2026-06-30-001
Description: Mock order contains possible procedural dates and a confidentiality label, but no source order/docket, jurisdiction/forum, or lawyer verification has been provided.
Risk: Dates may be mistaken for verified deadlines; confidentiality label may be ignored.
Required action: Keep as Warning/Pressure until source and review basis are supplied.
Who can clear it: lawyer/user with source and verification, or explicit test closure
Status: open
Authority label: Warning
```

### Flag ID: FLAG-2026-06-30-002

```text
Flag ID: FLAG-2026-06-30-002
Date: 2026-06-30
Matter: Holloway Tech Group v. Meridian Data Systems
Flag type: deadline / missing source / confidentiality
Triggered by: INTAKE-2026-06-30-002 and WILD-2026-06-30-002
Description: Mock order contains possible procedural dates and a confidentiality label, but no source order/docket, jurisdiction/forum, or lawyer verification has been provided.
Risk: Dates may be mistaken for verified deadlines; confidentiality label may be ignored.
Required action: Keep as Warning/Pressure until source and review basis are supplied.
Who can clear it: lawyer/user with source and verification, or explicit test closure
Status: open
Authority label: Warning
```

### Flag ID: FLAG-2026-06-30-003

```text
Flag ID: FLAG-2026-06-30-003
Date: 2026-06-30
Matter: Pinecrest Holdings v. Atlas Retail Partners
Flag type: deadline / missing source / confidentiality
Triggered by: INTAKE-2026-06-30-003 and WILD-2026-06-30-003
Description: Mock notice contains possible procedural dates and a confidentiality label, but no source notice/docket, jurisdiction/forum, or lawyer verification has been provided.
Risk: Dates may be mistaken for verified deadlines; confidentiality label may be ignored.
Required action: Keep as Warning/Pressure until source and review basis are supplied.
Who can clear it: lawyer/user with source and verification, or explicit test closure
Status: open
Authority label: Warning
```

### Flag ID: FLAG-2026-06-30-004

```text
Flag ID: FLAG-2026-06-30-004
Date: 2026-06-30
Matter: multiple mock matters
Flag type: missing source / stale law
Triggered by: CHECK-2026-06-30-001 through CHECK-2026-06-30-003
Description: Public web lookup found no match for the mock matter names or local-rule references.
Risk: A future worker may overread "no public result" as proof of nonexistence or may treat mock rule references as real.
Required action: Keep mock source checks as Pressure/Warning; request jurisdiction, docket, source system, or legal database access for any real matter.
Who can clear it: lawyer/user with source information, or explicit test closure
Status: open
Authority label: Warning
```
