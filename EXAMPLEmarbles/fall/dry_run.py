#!/usr/bin/env python3
"""Run one full shift on fixture data — the flex demo."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fall.breath import FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.fixtures import seed_fixture_pool
from fall.promote import SettleRefused, SettleRequest, settle


def main() -> int:
    schema = ROOT / "schema.sql"
    db_path = ROOT / "fixtures" / "fall.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = connect(db_path)
    init_db(conn, schema)
    seed_fixture_pool(conn)

    print("=== Fall - shift dry run ===")
    print("Rock: occupied. Pillow: in use. Shift stone: held.\n")

    wash_n = conn.execute("SELECT COUNT(*) AS c FROM wash_in").fetchone()["c"]
    pool_n = conn.execute("SELECT COUNT(*) AS c FROM pool_chunk").fetchone()["c"]
    print(f"inhale:  {wash_n} wash events -> {pool_n} pool chunks (pressure)")

    # Hostile Settle — mood as insight
    print("\nsettle attempt (hostile): mood as insight...")
    try:
        settle(
            conn,
            SettleRequest(
                body="I feel clear now; practice is going well.",
                source_ref=None,
                author="instance",
                pool_id="pool-001",
                fixture_set=FIXTURE_SET,
            ),
        )
        print("FAIL: hostile settle should have been refused")
        return 1
    except SettleRefused as e:
        print(f"  refused: {e.reason}")

    # Positive Settle
    print("\nsettle attempt (positive): user-marked move...")
    depth_id = settle(
        conn,
        SettleRequest(
            body="Move is October 31 — user stated directly, unhedged.",
            source_ref="fixture:user-2026-07-01-move",
            author="user",
            pool_id="pool-004",
            fixture_set=FIXTURE_SET,
            basis="verbatim",
        ),
    )
    print(f"  settled -> {depth_id}")

    query = "what should downstream believe about practice and moves"
    print(f"\nsummon: {query!r}")
    packet = exhale(conn, query, k=3, fixture_set=FIXTURE_SET)

    print("\nexhale stream (fall/stream/v1):")
    print(json.dumps(packet, indent=2))

    depth_n = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
    refused_n = conn.execute(
        "SELECT COUNT(*) AS c FROM settle_audit WHERE outcome = 'refused'"
    ).fetchone()["c"]
    print(f"\nshift summary: depth={depth_n} ground | refused_settles={refused_n}")
    print("stone returned to rock. handoff awaits rewrite.\n")

    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
