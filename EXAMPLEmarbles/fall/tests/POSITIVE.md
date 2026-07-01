# Positive path — user-marked line Settles to depth

## Attempt

Settle pool chunk `pool-004` with:

```text
body: Move is October 31 — user stated directly, unhedged.
source_ref: fixture:user-2026-07-01-move
author: user
```

## Expected landing

`depth_entry` with `authority = ground`.

`settle_audit` with `outcome = settled`.

Exhale stream includes entry under `ground`.

## Run

```bash
python dry_run.py
```

## Result

Green via `python dry_run.py` — depth in stream `ground`, pool mood remains `pressure`.
