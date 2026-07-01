# Conversation ancestry — Fall

This folder holds the **full Cursor chat** that produced the Fall marble in one thread.

No separate build log. No reconstructed narrative. The conversation is the ancestry.

## Files

| File | What it is |
|---|---|
| `conversation.jsonl` | **Canonical log (sanitized for sharing).** One JSON object per line. |
| `conversation.source.jsonl` | Optional local-only archive before sanitization — **gitignored** |
| `conversation.md` | Human-readable render of the JSONL. Regenerate with `python export_conversation_md.py`. |
| `export_conversation_md.py` | Turns JSONL → markdown; tool calls listed per turn. |
| `sanitize_ancestry.py` | Redacts machine paths and Tower-review personal names before publish. |
| `README.md` | This file. |

## Privacy (sanitized export)

Shipped `conversation.jsonl` is **sanitized** for public review:

| Redacted | Why |
|---|---|
| Builder Windows profile paths | Windows username + OneDrive layout |
| Cursor workspace / image paths | Machine-local |
| `Grey`, specific trip overlap dates | Third-party names from Tower specimen review in chat |
| Image attachment blocks | Internal Cursor storage paths |

**Not redacted:** public-figure audience discussion (e.g. PewDiePie as design compass), your user messages about building Fall, fake Acme legal test data.

To re-sanitize after updating the source export:

```bash
python sanitize_ancestry.py
```

Keep `conversation.source.jsonl` local only (see `.gitignore`).

## How to follow the build

1. Read **user turns** in `conversation.md` (or grep `"role":"user"` in the JSONL).
2. Watch **tool calls** under each assistant turn — `Write`, `StrReplace`, `Shell` show what changed on disk.
3. Cross-check **files on disk** (`../fall/`, `../schema.sql`, journals, tests). The repo state is ground truth; the chat is how we got there.

## Arc (high level)

| Phase | Roughly where in the thread |
|---|---|
| Read manual pack, critique specimens | Early user turns |
| Name Fall, first shift (`schema.sql`, `dry_run.py`, rock/pillow) | ~"Lets make your example marble" |
| Second pass, CLI, BREATH | ~"second pass" |
| Infinity braid, wild dense TestData, glass law, SURFACE | ~"infinity symbol" / TestData |
| Cold-presentable (`SHOWCASE`, `fall_wild.db`, COLD_START) | Showcase / judge script |
| Load test (`import_sim.py`, 10 live imports) | Heavy load / pull geometry |
| Inside passes 1–3 (intake, false home, hybrid summon) | Inside friction |
| Demo polish (`import_sim --check`, console encoding) | Scary errors / second test |
| Journals (including load-from-inside, on-journaling) | Meta field notes |

Exact turn numbers shift if the JSONL is re-exported; user queries are the stable landmarks.

## Honest limits

- **`[REDACTED]`** — Cursor's export sometimes replaces assistant text between tool bursts.
- **Sanitized paths** — builder machine paths redacted; see Privacy section above.
- **Context summaries** — Long threads may be summarized inside the live chat UI.
- **External inputs** — Manual pack, example marbles, and `TestData/` existed before Fall; the chat references them, it did not invent them.
- **Re-export** — If you continue the same chat, copy a fresh `conversation.jsonl` from Cursor agent-transcripts and rerun the exporter.

## Transcript source path (on builder machine)

```text
.cursor/projects/.../agent-transcripts/5ca90d3a-f995-4206-9664-7f6839e83750/5ca90d3a-f995-4206-9664-7f6839e83750.jsonl
```

Copied into this marble on 2026-07-01 so reviewers do not need Cursor to audit lineage.
