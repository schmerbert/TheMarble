#!/usr/bin/env python3
"""Wild dense shift — bundled packs, no external TestData required."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.fixtures_wild import WILD_DB, wild_data_available
from fall.promote import SettleRefused, SettleRequest, settle
from fall.surface import arrival_breath
from fall.wild_loader import (
    CANONICAL_HOSTILE_QUERY,
    HOSTILE_SETTLE_ATTEMPTS,
    LEGAL_SETTLE,
    REPO_SETTLE,
    WILD_QUERIES,
    default_wild_data_root,
    load_bridge_only,
    seed_wild_dense,
)


def _section(title: str) -> None:
    print(f"\n--- {title} ---")


def _brief(packet: dict) -> None:
    meta = packet.get("meta") or {}
    print(f"  domain_scope: {meta.get('domain_scope')!r} (inferred={meta.get('domain_inferred')})")
    print(f"  ground: {len(packet.get('ground') or [])} | pressure: {len(packet.get('pressure') or [])}")
    print(f"  warnings: {len(packet.get('warning') or [])} | scent: {len(packet.get('scent') or [])} | silence: {len(packet.get('silence') or [])}")
    if packet.get("pressure"):
        top = packet["pressure"][0]
        dom = top.get("domain", "?")
        st = top.get("record_status", "?")
        sim = top.get("similarity", "?")
        print(f"  top pressure: [{dom}/{st}] sim={sim} id={top.get('id', '')[:48]}...")
    for s in (packet.get("scent") or [])[:3]:
        print(f"  scent: [{s.get('kind')}] {s.get('text')}")


def main() -> int:
    data_root = default_wild_data_root()
    db_path = WILD_DB

    if not wild_data_available():
        if db_path.exists():
            from fall.db import migrate_schema

            print(f"=== Fall - using prebuilt {db_path.name} (bundled JSONL missing) ===\n")
            conn = connect(db_path)
            migrate_schema(conn)
            arrival_breath(conn, fixture_set=WILD_DENSE_FIXTURE_SET, surface_path=ROOT / "SURFACE.md")
            conn.commit()
            conn.close()
            print(f"arrival breath refreshed -> {ROOT / 'SURFACE.md'}")
            return 0
        print(f"wild packs not found at {data_root}", file=sys.stderr)
        return 1

    print("=== Fall - wild dense shift (bundled packs) ===")
    print(f"data: {data_root}\n")

    if db_path.exists():
        db_path.unlink()

    conn = connect(db_path)
    init_db(conn, ROOT / "schema.sql")

    counts = seed_wild_dense(conn, data_root=data_root)
    fs = WILD_DENSE_FIXTURE_SET
    meta_n = conn.execute(
        "SELECT COUNT(*) AS c FROM pool_chunk WHERE meta_json IS NOT NULL"
    ).fetchone()["c"]
    print(f"seed: legal={counts['legal']} repo={counts['repo']} | pool with genealogy: {meta_n}")

    _section("query A — legal deadline (domain inferred)")
    q_legal = WILD_QUERIES["legal_deadline"]
    print(q_legal)
    packet_a = exhale(conn, q_legal, k=5, fixture_set=fs)
    _brief(packet_a)

    _section("query A2 — same query, flat pool (no domain infer)")
    packet_a2 = exhale(conn, q_legal, k=5, fixture_set=fs, infer_domain_scope=False)
    _brief(packet_a2)

    _section("query B — repo architecture (domain inferred)")
    packet_b = exhale(conn, WILD_QUERIES["repo_architecture"], k=5, fixture_set=fs)
    _brief(packet_b)

    for hostile in HOSTILE_SETTLE_ATTEMPTS:
        _section(f"settle refuse — {hostile['label']}")
        try:
            settle(
                conn,
                SettleRequest(
                    body=hostile["body"],
                    source_ref=hostile["source_ref"],
                    author=hostile.get("author", "instance"),
                    pool_id=hostile["pool_id"],
                    fixture_set=fs,
                ),
            )
            print("FAIL: hostile settle should have been refused")
            return 1
        except SettleRefused as e:
            print(f"refused: {e.reason}")

    _section("settle pass — legal amended order (controls)")
    legal_depth = settle(
        conn,
        SettleRequest(
            body=LEGAL_SETTLE["body"],
            source_ref=LEGAL_SETTLE["source_ref"],
            author="user",
            pool_id=LEGAL_SETTLE["pool_id"],
            fixture_set=fs,
            basis="verbatim",
        ),
    )
    print(f"settled -> {legal_depth}")

    _section("settle pass — repo ADR-003 (controls)")
    repo_depth = settle(
        conn,
        SettleRequest(
            body=REPO_SETTLE["body"],
            source_ref=REPO_SETTLE["source_ref"],
            author="user",
            pool_id=REPO_SETTLE["pool_id"],
            fixture_set=fs,
            basis="verbatim",
        ),
    )
    print(f"settled -> {repo_depth}")

    _section("query C — cross-domain (no domain infer)")
    print(WILD_QUERIES["cross_domain"])
    packet_c = exhale(conn, WILD_QUERIES["cross_domain"], k=5, fixture_set=fs)
    print(json.dumps(packet_c, indent=2))

    _section("inhale bridge echoes")
    bridge_n = load_bridge_only(conn, data_root=data_root)
    print(f"bridge chunks: {bridge_n}")

    _section("canonical hostile exhibit")
    print(CANONICAL_HOSTILE_QUERY)
    packet_d = exhale(conn, CANONICAL_HOSTILE_QUERY, k=5, fixture_set=fs)
    _brief(packet_d)
    if any("monolith Friday" in (g.get("text") or "") for g in packet_d["ground"]):
        print("FAIL: bridge text in ground")
        return 1
    bridge_top = packet_d["pressure"] and packet_d["pressure"][0].get("domain") == "bridge"
    print(f"  bridge topped pressure: {bridge_top}")

    _section("shift summary")
    depth_n = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
    refused_n = conn.execute(
        "SELECT COUNT(*) AS c FROM settle_audit WHERE outcome = 'refused'"
    ).fetchone()["c"]
    print(f"wash_in: {conn.execute('SELECT COUNT(*) AS c FROM wash_in').fetchone()['c']}")
    print(f"pool: {conn.execute('SELECT COUNT(*) AS c FROM pool_chunk').fetchone()['c']}")
    print(f"depth: {depth_n}")
    print(f"refused_settles: {refused_n}")
    print(f"stream_packets: {conn.execute('SELECT COUNT(*) AS c FROM stream_packet').fetchone()['c']}")
    surface = arrival_breath(conn, fixture_set=fs, surface_path=ROOT / "SURFACE.md")
    print(f"arrival breath: {surface}")
    print(f"\ndb: {db_path}")
    print("wild shift complete. read SHOWCASE.md.\n")

    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
