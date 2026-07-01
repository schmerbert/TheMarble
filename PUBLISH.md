# Public release notes

**This repo is the public release.** Clone it, verify it, fork it — no export step required.

If you also keep a **private working copy** (local tool config, unsanitized ancestry
sources, session databases), maintain that separately. The working copy may use a
`publish_clean.ps1` script to build a fresh export like this one — that script lives
in the working repo, not here.

## What ships in this repo

| Included | Why |
|---|---|
| `START_HERE.md`, `README.md`, `AGENTS.md`, `LETTER_TO_YOU_BOTH.md`, `FABLE_5_LIGHTHOUSE_CONV.md` | Arrival, posture, and perspective lens |
| `Manual/`, `Reference/` | Core manual pack |
| `EXAMPLEmarbles/` | All six specimen marbles |
| `TestData/` | Optional external test packs for Fall |
| `verify_examples.ps1` | Maintainer test sweep |
| Sanitized `ancestry/` (Fall + Lighthouse) | Build provenance — **not** `*.source.jsonl` |
| Fall fixture DBs (`fall_wild.db`, etc.) | SHOWCASE depends on them |
| Per-marble `.gitignore` files | Keep clones clean |

| Not in this repo (by design) | Why |
|---|---|
| `**/conversation.source.jsonl` | Unsanitized ancestry archives — gitignored if present locally |
| `**/data/light.db` | Lighthouse session LOG (local only) |
| `.claude/`, `.cursor/`, `.agents/` | Local tool config and machine paths |

## What we keep on purpose (not secrets)

- **User voice** in `LETTER_TO_YOU_BOTH.md`, journals, standing orders — chosen public texture
- **Sanitized build chats** in `ancestry/conversation.jsonl` — paths redacted, see each ancestry `README.md`
- **Public-figure design discussion** (e.g. PewDiePie as audience compass in Fall ancestry) — design intent, not PII
- **`noreply@anthropic.com`** in Co-Authored-By lines inside ancestry — tool metadata, not your email

## Verify before you trust

```powershell
.\verify_examples.ps1
```

Runs Fall, Lighthouse, Trench, and Cabin hostile suites against this tree.

## Re-sanitizing ancestry

If you refresh a conversation export from Cursor or Claude Desktop in a working copy:

```bash
cd EXAMPLEmarbles/fall/ancestry && python sanitize_ancestry.py
cd EXAMPLEmarbles/lighthouse/ancestry && python sanitize_ancestry.py
```

Keep `conversation.source.jsonl` local only — never in a public export.

## Working repo vs this public repo

| | Working repo (`marble_starter`) | This repo (`TheMarble`) |
|---|---|---|
| Purpose | Build, iterate, local tools | Download, verify, fork |
| Git history | Your commits, your email | One clean public commit |
| Ancestry source | May exist locally (gitignored) | Never copied |
| Lighthouse LOG | May exist locally | Never copied |
