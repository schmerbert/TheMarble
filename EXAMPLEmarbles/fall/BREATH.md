# BREATH.md — Fall

How material moves on a shift. Per-message ambient injection is forbidden. **Arrival** surfaces through mist — `SURFACE.md` — not through flooding every line you read.

## Live wash (bulk intake)

When material washes in **live** (`fixture_set` null, CLI `--live`):

```text
wash → status (read live_wash lines) → exhale --live for work → arrive when shift ends
```

Not:

```text
wash → arrive expecting your imports in pack mist   # wrong order for live bulk
```

| Flag | Summons |
|---|---|
| `--wild` | rehearsal pack only — **omits** live wash |
| `--live` | full churn including live wash |
| neither | dry_run fixture_set default |

**Rank != receipt.** Embed rank alone may ignore fresh imports on generic queries. **`--live` exhale** uses hybrid summon: up to one **receipt slot per live domain** (newest wash) plus embed-ranked pressure. Receipt is still spray — recency is not Settle.

After bulk wash, `SURFACE.md` lists **Fresh wash (live)** when live chunks exist, plus a live orientation breath.

Stale `SURFACE` during work means **mid-shift** — use `exhale --live`; run `arrive` when the shift ends.

## Inhale

Something washes in: user line, session fragment, rehearsal chunk, outside correction.

Ask: what is this? who authored it? is there a source? does it belong in the churn only?

Never inhale directly to depth.

## Classify

| Signal | Default landing |
|---|---|
| user / instance fragment, no Settle yet | pool |
| unsigned inference, mood, hedged memory | pool |
| Settle passed with source | depth |

## Settle (the only crossing)

Pool to depth only. The law lives in `fall/promote.py` when you need the mechanism.

Passes: user confirmation, verbatim + source, synthesis citing pool id.

Refuses: missing source, spray mistaken for depth, superseded/stale/bridge lineage (see `GENEALOGY.md`).

## Summon

Nearness on the **churn only**. Nearness is not Settle.

You may narrow to one domain (`legal`, `repo`) — explicit flag or inferred from the question. Mixed questions stay flat across the whole pool.

```bash
python -m fall.cli exhale "your query here" --wild --domain legal --db fixtures/fall_wild.db
```

## Exhale

Build a thin `fall/stream/v1` packet — smaller than what washed in.

| Label | From |
|---|---|
| **ground** | depth only — settled stones |
| **pressure** | spray from the churn (capped excerpts; may carry domain and status) |
| **warning** | cold air when nearness could mislead |
| **scent** | smell of lineage — supersession, staleness, scope — not ground |
| **silence** | known but intentionally withheld |

Default pressure cap: 280 chars total excerpts.

### Warnings (productive friction)

Exhale adds warnings when:

- loudest spray has no source and nearness is non-trivial
- spray text is hedged (`didn't we`, `probably`, `I feel`, …)
- loudest spray is superseded or stale — nearness must not bypass lineage
- bridge spray in the mix — do not merge across domains
- stones and spray both rose for the same question — depth must not bless the churn

Warnings and scent are not ground. Downstream must not strip them.

## Cadence

| When | Breath |
|---|---|
| Shift start | `HANDOFF.md`, then **`SURFACE.md`** (or `python -m fall.cli arrive --wild --db fixtures/fall_wild.db`) |
| During shift | inhale / Settle / exhale on demand |
| Shift end | rewrite `HANDOFF.md`, `arrive` for the next worker |
| Demo reset | `python wild_run.py` rebuilds db + `SURFACE.md` |

## Carrier

Handoff card at arrival. **`SURFACE.md`** at arrival — orientation mist. Stream packet at query exhale. No ambient per-message injection.

### Arrival mist

```bash
python -m fall.cli arrive --wild --db fixtures/fall_wild.db
python -m fall.cli breath --wild --db fixtures/fall_wild.db
```

Writes stones plus domain weather (legal + repo for wild packs): spray, warnings, scent, silence.

Read the landing before you trust the loudest line.

## Override

Fresh user intent silences stale spray. Rehearsal packs are rehearsal only when labeled.
