# Trench Context Return

| Field | Value |
|---|---|
| **Carrier** | Trowel Call at arrival; Plumb Line on summon |
| **Payload** | Context Register ground, Field Notebook pressure, Damage Record warnings, Site Bench corrections |
| **Cadence** | Session start through seat; summoned search during work; session end through handoff |
| **Strength** | Concrete for Context Register and Damage Record; soft for Field Notebook; urgent for Site Bench correction |
| **Landing** | First read, then inline when summoned |
| **Trust** | Context Register = ground; Field Notebook = pressure; Damage Record = warning; Site Bench = warning/path |
| **Decay** | Handoff expires when rewritten; Field Notebook pressure decays unless re-observed; Site Bench items expire when acted on |
| **Override** | Fresh user instruction, current file contents, and field audit/test output override inherited pressure |

## Nesting dolls

- Outermost: `HANDOFF.md`, the Trowel Call.
- Middle: `MANIFEST.md`, `context-register/`, `damage-record/`, and `SITE_BENCH.md`.
- Innermost: `field-notebook/`, raw sessions, drafts, failed writes, and observations.

Do not compress raw notes into ground. Extract, cite, Lift, or record Broken Chain.
