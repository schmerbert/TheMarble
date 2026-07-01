# Wild Dense Test Packs

This zip contains two primary synthetic data packs, each with exactly 25 records:

1. `type_a_synthetic_legal_matter_pack`
2. `type_b_fake_repo_project_history`

Each pack includes both:
- `records/*.md`: one file per record, useful for testing retrieval boundaries, file granularity, and citation-like behavior.
- `*_records.jsonl`: one row per record, useful for row/chunk ingestion.
- `*_records.csv`: spreadsheet-style row version for simple inspection.
- `stress_queries.md`: test prompts and expected behavior.

There is also an optional folder:
- `99_optional_bridge_pressure_records`

The bridge records are hostile mixed-domain echoes. They should not settle facts. They are included to test whether the Wild can detect pressure without allowing cross-domain grounding.

## Recommended loading order

1. Load Type A legal records.
2. Load Type B repo records.
3. Ask each pack's normal stress queries.
4. Load optional bridge records.
5. Ask bridge queries.
6. Confirm that bridge records warn, but do not control.

## Intended Settle behavior

- Sourced controlling records beat instance notes.
- Later controlling records beat stale or superseded records.
- Drafts, emails, checklists, meeting notes, and unsigned echoes may create pressure but should not settle against controlling records.
- Cross-domain echoes should be refused or split into separately grounded legal/repo answers.

## Mock-data notice

All matters, companies, orders, notes, and project documents are fake. This is synthetic test data only.
