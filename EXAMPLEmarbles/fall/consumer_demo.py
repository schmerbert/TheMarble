#!/usr/bin/env python3
"""Spirit consumer — what would a downstream marble trust?"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def consume(packet: dict) -> None:
    print("=== downstream consumer (spirit) ===\n")
    if packet.get("fixture_set"):
        print(f"fixture_set={packet['fixture_set']!r} -> rehearsal only\n")

    for label in ("ground", "pressure", "warning", "scent", "silence"):
        items = packet.get(label) or []
        if not items:
            continue
        print(f"{label.upper()}:")
        for item in items:
            if isinstance(item, dict):
                text = item.get("text", item)
                auth = item.get("authority", label)
                kind = item.get("kind")
                prefix = f"[{auth}]" if not kind else f"[{auth}/{kind}]"
                dom = item.get("domain")
                st = item.get("record_status")
                tag = ""
                if dom or st:
                    tag = f" ({dom or ''}{'/' + st if st else ''})".strip()
                print(f"  {prefix}{tag} {text}")
            else:
                print(f"  {item}")
        print()

    print("consumer rules:")
    print("  - would treat ground as cited only if source_ref present")
    print("  - would not act on stream — Fall has no outbox")


def main() -> int:
    print("Fall showcase consumer — see SHOWCASE.md step 4\n")
    db_path = ROOT / "fixtures" / "fall.db"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--infinity":
            db_path = ROOT / "fixtures" / "fall_infinity.db"
            sys.argv.pop(1)
        elif sys.argv[1] == "--wild":
            db_path = ROOT / "fixtures" / "fall_wild.db"
            sys.argv.pop(1)
    if not db_path.exists():
        hints = {
            "fall_infinity.db": "python infinity_run.py",
            "fall_wild.db": "python wild_run.py",
        }
        hint = hints.get(db_path.name, "python dry_run.py")
        print(f"Run {hint} first.", file=sys.stderr)
        return 1

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT payload_json FROM stream_packet ORDER BY exhaled_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if not row:
        print("No stream packet found.", file=sys.stderr)
        return 1

    packet = json.loads(row["payload_json"])
    consume(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
