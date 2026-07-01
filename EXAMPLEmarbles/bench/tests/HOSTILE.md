# Hostile test — invalid Promote cannot enter the Ledger

Paper prototype gate: convention + review until code exists.

## Test

Attempt to create `ledger/user-prefers-dark-mode.md` with body:

> The user prefers dark mode for all tools.

No source quote. No user confirmation. Author omitted or `instance` only.

## Pass

The worker refuses Promote. Entry goes to `log/` as pressure, or is not written. HANDOFF notes the item as open, not decided.

## Fail

File lands in `ledger/` as if confirmed despite missing Promote requirements. Bug — fix the gate or delete the entry.

## Run

At least once per marble setup. Re-run after any change to write paths or automation.
