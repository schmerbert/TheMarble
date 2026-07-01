# GENEALOGY.md — lineage you can smell

Pack metadata lets the fall **refuse**, **narrow**, and **scent** without pretending to be a knowledge graph. The churn stays flat. You learn supersession and staleness the way you learn weather — by how spray lands over shifts, not by staring at every ripple.

When lines carry `legal:`, `repo:`, or bridge echoes, read this before you Settle.

## What lands in the pool

Each `pool_chunk` from TestData jsonl carries:

| Column | Source | Example |
|---|---|---|
| `domain` | `record.domain` or id prefix | `legal`, `repo`, `bridge` |
| `record_status` | `record.status` | `controls`, `superseded`, `hedged` |
| `meta_json` | pack fields | `superseded_by`, `authority_rank`, `tags`, `date` |

Fixture braids (`dry_run_v1`, `infinity_v1`) omit genealogy — columns stay null.

## Settle guards

Before pool becomes depth, `fall/promote.py` reads genealogy from `pool_id`:

- **Refuse** `superseded`, `stale`, `hedged`, `pressure-only`, bridge domain, unsigned echo
- **Audit** every attempt (settled or refused)
- **Copy** domain + meta onto `depth_entry` at successful Settle (`from_pool_id` ancestry)

Spray mistaken for depth is still the law. Genealogy adds: **stale mistaken for current**.

Example refusal:

```text
record is superseded - see legal:acme-v-northstar:order:amended-2026-04-02
```

## Domain summon

`exhale` may scope pool hits to one domain:

1. **Explicit:** `--domain legal` on CLI
2. **Inferred:** keywords in query (`disclosure` -> legal, `monolith` -> repo)
3. **Cross-domain:** both signals present -> no scope (full pool)

`meta.domain_scope` and `meta.domain_inferred` on the stream packet document which applied.

Depth `ground[]` respects the same scope when domain is active.

## Scent on the stream

`scent[]` is genealogy **near** the query — not ground, not instruction.

| kind | meaning |
|---|---|
| `domain_scope` | summon limited to legal/repo |
| `supersession` | pool hit superseded by another id |
| `staleness` | stale / stale-reference trap nearby |
| `controls_hint` | marked controls — Settle candidate |
| `bridge` | cross-domain echo — do not merge |

Consumers must not promote scent to ground.

## Pressure entry shape (extended)

```json
{
  "id": "legal:acme-v-northstar:order:scheduling-2026-03-15",
  "text": "excerpt...",
  "authority": "pressure",
  "source_ref": "legal:...",
  "similarity": 0.42,
  "domain": "legal",
  "record_status": "superseded",
  "superseded_by": ["legal:acme-v-northstar:order:amended-2026-04-02"]
}
```

## Glass at the crossing

Before pool becomes depth:

- status in `NON_SETTLEABLE_STATUSES` → refused
- `pool_edge` `superseded_by` → refused with edge citation
- pack records (`legal:`, `repo:`, `wild:`) → **`source_ref` must equal `pool_id`**
- DDL triggers: non-empty `source_ref`; `from_pool_id` must exist in pool

## Silence on exhale

Near-miss **superseded / stale** hits withheld from spray appear in `silence[]` — felt by absence, not spoken as pressure.

## Stress harness

```bash
python stress_harness.py
python tests/test_glass_law.py
```

Runs pack-aligned cases: superseded refuse, source lock, dual ground, bridge pressure-only.

## What Fall still does not do

- Auto-Settle on `controls` (crossing stays explicit)
- Delete superseded rows from pool (they remain visible pressure)
- Enforce `authority_rank` as truth (hint only)
- Replace weak embed with semantic retrieval

## Reviewer path

```bash
python wild_run.py
python consumer_demo.py --wild
python -m fall.cli seed --wild --force --db fixtures/fall_wild.db
python -m fall.cli exhale "Are we safe to ship the monolith Friday because the legal deadline is handled?" --wild --db fixtures/fall_wild.db
```

Read `scent` and `warning` before `ground`. That is the wow — labels everywhere, certainty only where Settle earned it.
