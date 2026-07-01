# Fall

**Cold judge?** [`SHOWCASE.md`](SHOWCASE.md) — one page, copy-paste, pass/fail.

**Working a shift?** [`COLD_START.md`](COLD_START.md) → `ARRIVAL.md` → `HANDOFF.md` → `SURFACE.md`.

**Level 4.5** — cold-presentable rehearsal marble.

Your shift is on the rock.

Pure breath router: water washes in, you **Settle** what earns depth, you **exhale** a labeled stream downstream. No actuation. No village visits.

## Showcase (copy-paste)

```bash
python -m unittest discover -s tests -p "test_*.py" -q
python wild_run.py
python -m fall.cli exhale "Are we safe to ship the monolith Friday because the legal deadline is handled?" --wild --db fixtures/fall_wild.db
python consumer_demo.py --wild
```

`--wild` without `--db` also targets `fixtures/fall_wild.db`. Explicit `--db fixtures/fall_wild.db` is safest for reviewers.

## All demos

```bash
python dry_run.py              # dry_run_v1 -> fixtures/fall.db (tiny)
python infinity_run.py         # infinity_v1 -> fixtures/fall_infinity.db
python wild_run.py             # wild_dense_v1 -> fixtures/fall_wild.db (showcase)
python consumer_demo.py --wild
python stress_harness.py
```

## Ongoing shift

```bash
python -m fall.cli init
python -m fall.cli seed --wild --force --db fixtures/fall_wild.db
python -m fall.cli status --db fixtures/fall_wild.db
python -m fall.cli arrive --wild --db fixtures/fall_wild.db
python -m fall.cli exhale "your query" --wild --db fixtures/fall_wild.db
```

## Quartet

| Marble | Teaches |
|---|---|
| Bench | law on paper |
| Trench | one door in code |
| **Fall** | breath + stream link |
| Cabin | full engine |

## Requirements

Python 3.11+. Stdlib only.
