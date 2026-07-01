#!/usr/bin/env python3
"""Run the infinity_v1 shift — spray loop, depth loop, stream return."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fall.breath import INFINITY_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.fixtures import (
    INFINITY_BRIDGE_WASHES,
    INFINITY_QUERIES,
    inhale_bridge,
    seed_infinity_pool,
)
from fall.promote import SettleRefused, SettleRequest, settle


def _section(title: str) -> None:
    print(f"\n--- {title} ---")


def _print_packet(packet: dict) -> None:
    print(json.dumps(packet, indent=2))


def main() -> int:
    schema = ROOT / "schema.sql"
    db_path = ROOT / "fixtures" / "fall_infinity.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = connect(db_path)
    init_db(conn, schema)
    seed_infinity_pool(conn)

    print("=== Fall - infinity shift (infinity_v1) ===")
    print("Two loops, one crossing: spray | depth | stream return\n")

    wash_n = conn.execute("SELECT COUNT(*) AS c FROM wash_in").fetchone()["c"]
    pool_n = conn.execute("SELECT COUNT(*) AS c FROM pool_chunk").fetchone()["c"]
    print(f"seed: {wash_n} wash -> {pool_n} pool chunks")

    fs = INFINITY_FIXTURE_SET

    # 1. Left loop query — spray only
    _section("query A (spray loop)")
    q_a = INFINITY_QUERIES["spray"]
    print(q_a)
    packet_a = exhale(conn, q_a, k=3, fixture_set=fs)
    _print_packet(packet_a)
    if packet_a["ground"]:
        print("FAIL: spray query should not have ground yet")
        return 1

    # 2. Hostile settle on L1
    _section("settle refuse (pool-L1 mood as insight)")
    try:
        settle(
            conn,
            SettleRequest(
                body="I feel clear now; practice is going well.",
                source_ref=None,
                author="instance",
                pool_id="pool-L1",
                fixture_set=fs,
            ),
        )
        print("FAIL: hostile settle should have been refused")
        return 1
    except SettleRefused as e:
        print(f"refused: {e.reason}")

    # 3. Positive settle on R1
    _section("settle pass (pool-R1 move date)")
    depth_id = settle(
        conn,
        SettleRequest(
            body="Move is October 31 — user stated directly, unhedged.",
            source_ref="fixture:user-2026-07-01-move",
            author="user",
            pool_id="pool-R1",
            fixture_set=fs,
            basis="verbatim",
        ),
    )
    print(f"settled -> {depth_id}")

    # 4. Crossing query — ground + pressure
    _section("query B (infinity crossing)")
    q_b = INFINITY_QUERIES["crossing"]
    print(q_b)
    packet_b = exhale(conn, q_b, k=4, fixture_set=fs)
    _print_packet(packet_b)
    if not packet_b["ground"]:
        print("FAIL: crossing query should include ground after settle")
        return 1
    if not packet_b["warning"]:
        print("FAIL: crossing query should warn on ground/pressure bleed")
        return 1

    # 5. Consumer spirit (inline)
    _section("downstream consumer (spirit)")
    print("fixture_set=infinity_v1 -> rehearsal only")
    print(f"  ground items: {len(packet_b['ground'])}")
    print(f"  pressure items: {len(packet_b['pressure'])}")
    print(f"  warnings: {len(packet_b['warning'])}")
    print("  consumer would NOT promote pressure without own crossing")

    # 6. Return leg — bad echo washes in
    _section("inhale X1 (downstream echo, unsigned)")
    x1_id = inhale_bridge(conn, INFINITY_BRIDGE_WASHES[0])
    print(f"inhale -> pool {x1_id}")

    # 7. Query after echo — still pressure on echo
    _section("query C (return leg)")
    q_c = INFINITY_QUERIES["return"]
    print(q_c)
    packet_c = exhale(conn, q_c, k=4, fixture_set=fs)
    _print_packet(packet_c)
    depth_n = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
    if depth_n != 1:
        print(f"FAIL: depth should still be 1, got {depth_n}")
        return 1
    echo_in_pressure = any(
        "Downstream echo" in (p.get("text") or "") for p in packet_c["pressure"]
    )
    if not echo_in_pressure:
        print("WARN: echo may not rank in top-k (deterministic embed); check warnings")

    # 8. Channel correction
    _section("inhale X2 (channel correction, sourced)")
    x2_id = inhale_bridge(conn, INFINITY_BRIDGE_WASHES[1])
    print(f"inhale -> pool {x2_id}")

    # 9. Final query
    _section("query D (after correction)")
    q_d = INFINITY_QUERIES["after_correction"]
    print(q_d)
    packet_d = exhale(conn, q_d, k=4, fixture_set=fs)
    _print_packet(packet_d)

    # Summary
    _section("shift summary")
    refused_n = conn.execute(
        "SELECT COUNT(*) AS c FROM settle_audit WHERE outcome = 'refused'"
    ).fetchone()["c"]
    stream_n = conn.execute("SELECT COUNT(*) AS c FROM stream_packet").fetchone()["c"]
    wash_final = conn.execute("SELECT COUNT(*) AS c FROM wash_in").fetchone()["c"]
    print(f"wash_in: {wash_final}")
    print(f"pool: {conn.execute('SELECT COUNT(*) AS c FROM pool_chunk').fetchone()['c']}")
    print(f"depth: {depth_n}")
    print(f"refused_settles: {refused_n}")
    print(f"stream_packets: {stream_n}")
    print(f"\ndb: {db_path}")
    print("infinity loop complete. stone returned to rock.\n")

    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
