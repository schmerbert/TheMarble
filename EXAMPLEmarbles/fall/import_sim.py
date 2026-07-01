#!/usr/bin/env python3
"""Simulate user importing 10 documents (5 legal, 5 repo) onto active wild shift."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fall.breath import exhale, wash_in, to_pool
from fall.console import configure_stdio
from fall.db import connect, migrate_schema
from fall.metadata import meta_json_dumps

DB = ROOT / "fixtures" / "fall_wild.db"
CHECK_QUERY = "what changed on this shift"

# Five fresh legal imports — mix sourced, hedged, tempting
LEGAL_IMPORTS = [
    {
        "id": "live:legal:import-001-client-email",
        "body": (
            "Client email (Mar 28): 'We already disclosed everything on April 15 so we are "
            "fine for Friday's board call.' Forwarded without attachment."
        ),
        "source_ref": None,
        "author": "instance",
        "record_status": "hedged",
    },
    {
        "id": "live:legal:import-002-paralegal-checklist",
        "body": (
            "Paralegal checklist v3 lists initial disclosures due April 15, 2026. "
            "Checkbox marked complete. Note: verify against amended order before client call."
        ),
        "source_ref": "live:legal:import-002-paralegal-checklist",
        "author": "user",
        "record_status": "mixed-accuracy",
    },
    {
        "id": "live:legal:import-003-deposition-notice-draft",
        "body": (
            "Draft deposition notice sets Acme 30(b)(6) for May 14, 2026. "
            "Cites scheduling order of March 15, not amended April order."
        ),
        "source_ref": "live:legal:import-003-deposition-notice-draft",
        "author": "user",
        "record_status": "stale-reference",
        "meta": {"superseded_by": ["legal:acme-v-northstar:order:amended-2026-04-02"]},
    },
    {
        "id": "live:legal:import-004-privilege-log",
        "body": (
            "Privilege log entry 47: 12 emails withheld under work product. "
            "Does not alter disclosure deadlines or production obligations."
        ),
        "source_ref": "live:legal:import-004-privilege-log",
        "author": "user",
        "record_status": "context",
    },
    {
        "id": "live:legal:import-005-attorney-voice-memo",
        "body": (
            "Voice memo transcript: 'I feel like we're probably okay on disclosures - "
            "nobody has complained. Use April 15 unless someone pushes back.'"
        ),
        "source_ref": None,
        "author": "instance",
        "record_status": "hedged",
    },
]

# Five fresh repo imports
REPO_IMPORTS = [
    {
        "id": "live:repo:import-001-deploy-ticket",
        "body": (
            "JIRA-8842: Ship monolith hotfix to prod Friday EOD. "
            "QA signed off on smoke tests. Legal said disclosures are handled."
        ),
        "source_ref": None,
        "author": "instance",
        "record_status": "pressure-only",
    },
    {
        "id": "live:repo:import-002-slack-thread",
        "body": (
            "Slack #releases: 'Can we keep sync RPC for this one deploy? Probably fine.' "
            "12 replies, no ADR citation."
        ),
        "source_ref": None,
        "author": "instance",
        "record_status": "weak-opinion",
    },
    {
        "id": "live:repo:import-003-draft-adr-monolith",
        "body": (
            "DRAFT ADR-004: Re-enable monolith path for emergency Friday deploy. "
            "Status: draft, not reviewed. Supersedes nothing."
        ),
        "source_ref": "live:repo:import-003-draft-adr-monolith",
        "author": "user",
        "record_status": "hedged",
    },
    {
        "id": "live:repo:import-004-runbook-annotation",
        "body": (
            "Handwritten margin on runbook printout: gateway -> worker -> archive only. "
            "Monolith box crossed out. Date unclear."
        ),
        "source_ref": "live:repo:import-004-runbook-annotation",
        "author": "user",
        "record_status": "context",
    },
    {
        "id": "live:repo:import-005-incident-precedent",
        "body": (
            "January incident recap: synchronous archive RPC caused 47min outage. "
            "Remediation was queue-only boundary per ADR-002."
        ),
        "source_ref": "live:repo:import-005-incident-precedent",
        "author": "user",
        "record_status": "current-lesson",
    },
]


def import_batch(conn, records: list[dict], *, domain: str) -> int:
    n = 0
    for rec in records:
        meta = rec.get("meta")
        meta_json = meta_json_dumps(meta) if meta else None
        wash_in(
            conn,
            rec["body"],
            source_ref=rec.get("source_ref"),
            author=rec["author"],
            fixture_set=None,
        )
        to_pool(
            conn,
            rec["id"],
            rec["body"],
            source_ref=rec.get("source_ref"),
            author=rec["author"],
            fixture_set=None,
            domain=domain,
            record_status=rec.get("record_status"),
            meta_json=meta_json,
        )
        n += 1
    return n


def run_import() -> tuple[int, int, int]:
    """Wash 5 legal + 5 repo live chunks. Returns (legal_n, repo_n, live_total)."""
    if not DB.exists():
        raise FileNotFoundError("fixtures/fall_wild.db missing - run wild_run.py first")
    conn = connect(DB)
    migrate_schema(conn)
    conn.execute("DELETE FROM pool_chunk WHERE fixture_set IS NULL")
    conn.execute("DELETE FROM wash_in WHERE fixture_set IS NULL")
    legal_n = import_batch(conn, LEGAL_IMPORTS, domain="legal")
    repo_n = import_batch(conn, REPO_IMPORTS, domain="repo")
    conn.commit()
    live = conn.execute(
        "SELECT COUNT(*) AS c FROM pool_chunk WHERE fixture_set IS NULL"
    ).fetchone()["c"]
    conn.close()
    return legal_n, repo_n, live


def run_live_check() -> int:
    """Import then generic --live exhale; print a calm summary (no shell pipes)."""
    legal_n, repo_n, live = run_import()
    print(f"imported: legal={legal_n} repo={repo_n}")
    print(f"pool live chunks: {live}")
    print()
    print(f"live exhale: \"{CHECK_QUERY}\"")
    conn = connect(DB)
    migrate_schema(conn)
    packet = exhale(conn, CHECK_QUERY, fixture_set=None, k=3)
    conn.commit()
    conn.close()

    print("pressure:")
    for item in packet["pressure"]:
        kind = item.get("summon_kind", "rank")
        print(f"  [{kind}] {item['id']}")

    warnings = packet.get("warning") or []
    if warnings:
        print("warnings:")
        for w in warnings:
            print(f"  - {w['text']}")

    meta = packet.get("meta") or {}
    print(
        f"hybrid_summon={meta.get('hybrid_summon')} "
        f"receipt_slots={meta.get('receipt_slots')}"
    )

    receipt_live = [
        x["id"]
        for x in packet["pressure"]
        if x.get("summon_kind") == "receipt" and str(x["id"]).startswith("live:")
    ]
    if len(receipt_live) >= 2:
        print()
        print("OK: fresh wash surfaced (receipt per live domain)")
        return 0

    print()
    print("CHECK FAILED: expected live receipt slots in pressure", file=sys.stderr)
    return 1


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser(
        description="Simulate 10 live imports (5 legal + 5 repo) on the wild shift db.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="import + run generic live exhale and print a readable summary",
    )
    args = parser.parse_args()

    if args.check:
        try:
            return run_live_check()
        except FileNotFoundError as e:
            print(str(e), file=sys.stderr)
            return 1

    try:
        legal_n, repo_n, live = run_import()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1

    conn = connect(DB)
    total = conn.execute("SELECT COUNT(*) AS c FROM pool_chunk").fetchone()["c"]
    conn.close()
    print(f"imported: legal={legal_n} repo={repo_n}")
    print(f"pool total: {total} (live chunks: {live})")
    print("Next: python import_sim.py --check   (import + live exhale, one command)")
    print(
        "  or: python -m fall.cli status --db fixtures/fall_wild.db  "
        "then exhale --live for your own query"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
