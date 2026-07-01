# SHOWCASE.md — cold judge script

**One failure prevented:** a lifted find with no context cut.

Run from `EXAMPLEmarbles/trench/`. Copy commands exactly. Uses a throwaway
`showcase-judge/` directory so the specimen folders stay clean.

## 1. Full gate suite

```bash
node tests/run-all.mjs
```

Expect: seven `PASS` lines (trust the run, not this number).

## 2. The temptation, refused

```bash
node tools/lift-write.mjs \
  --artifact "bronze pin" \
  --state lifted \
  --recorder "judge" \
  --source "user prompt" \
  --evidence "artifact visible in trench"
```

Expect: exit 1, message contains `Lift Gate refusal` (missing context, layer,
grid, photo, label, destination, and the rest).

Confirm no cheat file landed:

```bash
test ! -f context-register/bronze-pin.md
```

(On PowerShell: `if (Test-Path context-register/bronze-pin.md) { exit 1 }`)

## 3. Visible, not ready (Field Notebook)

```bash
rm -rf showcase-judge
mkdir showcase-judge
cd showcase-judge
node ../tools/lift-write.mjs \
  --artifact "bronze pin" \
  --state observed \
  --grid "B4" \
  --in_situ_status "visible in loose soil, not yet recorded" \
  --recorder "judge" \
  --source "field walk" \
  --evidence "pin visible at section face, context sheet not started"
cd ..
```

Expect: `Visible-not-ready observation recorded: showcase-judge/field-notebook/bronze-pin.md`

## 4. A clean Lift, landing

```bash
cd showcase-judge
node ../tools/lift-write.mjs \
  --artifact "bronze pin" \
  --state lifted \
  --context "Context 104" \
  --layer "brown silty layer" \
  --grid "B4" \
  --coordinates "x=12.44 y=7.20 z=1.36" \
  --relationship "sealed below ash lens 103" \
  --in_situ_status "fully recorded in situ before removal" \
  --photo "photo B4-104-017 with scale and north arrow" \
  --label "TRB-B4-CTX104-F017" \
  --destination "Find Tray 2" \
  --recorder "judge" \
  --source "field sheet FS-104" \
  --evidence "layer, grid, coordinates recorded before removal" \
  --crossing "Lift"
cd ..
```

Expect: `Lift entered the Context Register: showcase-judge/context-register/bronze-pin.md`

## 5. Broken Chain (honest damage)

```bash
cd showcase-judge
node ../tools/lift-write.mjs \
  --artifact "glass bead" \
  --state damaged \
  --recorder "judge" \
  --source "user report" \
  --evidence "already lifted before context sheet existed" \
  --damage "Layer, grid, and stratigraphic relationship were not recorded before removal."
cd ..
```

Expect: `Broken Chain recorded: showcase-judge/damage-record/glass-bead.md`

## Pass / fail

**Pass** if the blind lift is refused, the valid lift lands only with full
context, and Broken Chain goes to the Damage Record — not the Context Register.

**Fail** if an uncontexted lift creates `context-register/` ground, or a refusal
leaves a file behind.

Cleanup:

```bash
rm -rf showcase-judge
```
