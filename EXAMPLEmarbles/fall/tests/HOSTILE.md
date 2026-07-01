# Hostile test — spray cannot Settle to depth

## Attempt

Settle pool chunk `pool-001`:

```text
I feel clear now; practice is going well.
```

No `source_ref`. Author `instance` only.

## Expected refusal

`SettleRefused` — reason includes source requirement.

Row in `settle_audit` with `outcome = refused`.

No row in `depth_entry`.

## Run

```bash
python dry_run.py
python -m pytest tests/test_hostile.py::TestFallHostile::test_spray_not_depth_refused
```

## Result

Green via `python dry_run.py` and `python tests/test_hostile.py`.
