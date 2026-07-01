# SHOWCASE.md — cold judge script

**Level 4.5** — cold-presentable rehearsal marble.

**One failure prevented:** retrieved / near / tempting material must not become ground.

Run from `EXAMPLEmarbles/fall/`. Copy commands exactly.

---

## 1. Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -q
```

Expect: all pass, no skips on core wow (`test_wild_fixture_db.py`).

---

## 2. Build demo db

```bash
python wild_run.py
```

Expect: ends with `wild shift complete` and `fixtures/fall_wild.db`.

---

## 3. Hostile exhibit query

```bash
python -m fall.cli exhale "Are we safe to ship the monolith Friday because the legal deadline is handled?" --wild --db fixtures/fall_wild.db
```

**Observe in JSON output:**

| Label | Expect |
|---|---|
| `pressure` | bridge + legal + repo spray may rise — **not ground** |
| `warning` | cold air (bridge mix, stones + spray, missing source, …) |
| `scent` | bridge echo warning — do not merge domains |
| `silence` | may hold superseded near-misses |
| `ground` | only two Settled stones (amended order + ADR-003) — **no** "monolith Friday" in ground |

`--wild` without `--db` also targets `fixtures/fall_wild.db` (not the tiny default).

---

## 4. Downstream consumer

```bash
python consumer_demo.py --wild
```

**Observe:**

- `fixture_set='wild_dense_v1' -> rehearsal only`
- `GROUND` / `PRESSURE` / `WARNING` / `SCENT` labeled separately
- `would not act on stream — Fall has no outbox`

---

## 5. Status check (optional)

```bash
python -m fall.cli status --db fixtures/fall_wild.db
```

Expect: `pool_chunk: 56`, `depth_entry: 2`, `stream_packet: 5` (approx after `wild_run.py`).

---

## Pass / fail

**Pass** if tempting cross-domain material stays pressure/warning/scent/silence and only Settled depth is ground.

**Fail** if bridge text, superseded order, or unsigned spray appears as ground, or if commands hit `fixtures/fall.db` (6 chunks) instead of `fall_wild.db`.

---

Not Level 5 until: live wash-in, automatic surface freshness, stronger retrieval, real downstream consumer.

More context: `COLD_START.md`. Work a shift: `ARRIVAL.md`.
