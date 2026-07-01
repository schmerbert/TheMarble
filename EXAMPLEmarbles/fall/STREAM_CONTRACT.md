# STREAM_CONTRACT.md — v1

Fall does not act on other marbles. It **exhales** labeled packets they may drink.

## Shape

```json
{
  "stream_version": "fall/stream/v1",
  "stream_id": "uuid",
  "source": "fall",
  "fixture_set": "dry_run_v1 | null",
  "query": "string",
  "ground": [],
  "pressure": [],
  "warning": [],
  "scent": [],
  "silence": [],
  "meta": {
    "wash_in_count": 0,
    "pool_hits": 0,
    "exhale_bytes": 0
  }
}
```

## Entry shape (ground / pressure)

```json
{
  "id": "pool-003",
  "text": "excerpt",
  "authority": "pressure",
  "source_ref": "fixture:...",
  "similarity": 0.82,
  "domain": "legal",
  "record_status": "superseded",
  "superseded_by": ["legal:...:amended-2026-04-02"]
}
```

Genealogy fields are optional (null on fixture braids without pack metadata).

## Scent shape (spirit_v2)

```json
{
  "text": "pool hit legal:... is superseded by legal:...:amended-2026-04-02",
  "authority": "scent",
  "kind": "supersession",
  "relates_to": "legal:..."
}
```

Scent is not ground. Do not promote.

## Meta extensions (spirit_v2)

```json
"meta": {
  "wash_in_count": 0,
  "pool_hits": 0,
  "domain_scope": "legal",
  "domain_inferred": true,
  "exhale_bytes": 0
}
```

## Trust rules for consumers

1. **Never** promote `pressure` to local ground without your own crossing.
2. `ground` in stream came from Fall **depth** only — still verify `source_ref` if stakes are high.
3. `fixture_set` non-null → rehearsal; do not merge into live state.
4. `warning`, `scent`, and `silence` are first-class; do not strip them to shorten.
5. Fall has no outbox — stream is not instruction to act.

## Example consumers (spirit)

- `consumer_demo.py` — prints what it would trust
- Tower might map `pressure` → Radar, never Strip Board
- Bench might append stream to log/, Settle separately
- Cabin might inhale stream into Wild only

## Versioning

Bump `stream_version` when entry shape or trust rules change. Do not silently break downstream readers.
