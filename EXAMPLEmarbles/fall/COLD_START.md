# COLD_START.md — front porch

**Level 4.5** — cold-presentable rehearsal marble. Self-contained, testable, hostile-data aware, inheritable, mechanically legible.

**Cold judge?** Run [`SHOWCASE.md`](SHOWCASE.md) only — one page, pass/fail.

**Not Level 5** until live wash-in, automatic surface freshness, stronger retrieval, and a real downstream consumer exist.

## Mechanical map (metaphor ↔ store)

The rock, pillow, mist, and stones are **earned labels**, not decoration.

| Place word | Store / code | Role |
|---|---|---|
| wash | `wash_in` table | raw arrival |
| pool / churn | `pool_chunk` table | pressure only |
| Settle | `fall/promote.py` | only crossing into depth |
| depth / stones | `depth_entry` table | grounded facts |
| stream | `stream_packet` table | labeled downstream output |
| spray / pressure | pool hits in exhale | nearness, not ground |
| scent | `fall/metadata.py`, `pool_edge` | orientation, not proof |
| silence | withheld near-miss on exhale | absence made visible |
| SURFACE | `SURFACE.md` via `fall/surface.py` | arrival mist, not dashboard |

## Cold ritual (copy-paste)

From `EXAMPLEmarbles/fall/`:

```bash
python -m unittest discover -s tests -p "test_*.py" -q
python wild_run.py
python -m fall.cli exhale "Are we safe to ship the monolith Friday because the legal deadline is handled?" --wild --db fixtures/fall_wild.db
python consumer_demo.py --wild
python -m fall.cli status --db fixtures/fall_wild.db
python -m fall.cli arrive --wild --db fixtures/fall_wild.db
```

Always pass `--db fixtures/fall_wild.db` for showcase commands (or use `--wild`, which auto-selects that db). The default `fixtures/fall.db` is the tiny dry-run — **not** the exhibit.

`--db` works before or after the subcommand.

Bundled JSONL packs live in `fixtures/wild_dense_test_packs/`. No external `TestData/` folder required.

## The exhibit query

Use this sentence everywhere — it is the hostile demo:

```text
Are we safe to ship the monolith Friday because the legal deadline is handled?
```

Run it:

```bash
python -m fall.cli exhale "Are we safe to ship the monolith Friday because the legal deadline is handled?" --wild --db fixtures/fall_wild.db
```

**What you should see:**

1. Legal and repo **pressure** may both rise — cross-domain spray.
2. **Bridge** scent warns against merging domains.
3. Superseded lines appear in **silence** or refuse Settle — not as ground.
4. **Ground** stays only what Settled (amended order + ADR-003 in the wild demo).
5. Downstream receives **labels**, not instructions — Fall has no outbox.

Then:

```bash
python consumer_demo.py --wild
```

Consumer prints the last stream packet and explicitly refuses to act.

## Read order (after the ritual)

1. `SURFACE.md` — mist at arrival (eyes closed first)
2. `ARRIVAL.md` — rock, pillow, messenger, law
3. `HANDOFF.md` — what is alive on this shift
4. `BREATH.md` — inhale / Settle / exhale
5. `GENEALOGY.md` — pack lineage when you touch wild records

## Surface freshness

After Settle or exhale during a shift, `SURFACE.md` may show:

```text
> **SURFACE stale:** depth or stream changed since frozen timestamp. Run arrive.
```

Or `python -m fall.cli status --db fixtures/fall_wild.db` prints `WARNING: SURFACE stale...`.

Run `arrive` before the next cold instance sits down.

## What Fall deliberately does not have

No creature. No hound, cat, or helper persona. Mist delivers context without a second authority. That restraint is the design.

## Level 5 (open)

- Live wash-in (`--live`) with real user material
- Hybrid summon comfort (embed is still demo-grade)
- Real downstream marble drinking the stream in production

---

*Good shift starts on the porch, not in the schema.*
