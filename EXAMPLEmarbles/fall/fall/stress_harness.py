"""Stress harness — TestData stress_queries expectations as law tests."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.promote import SettleRefused, SettleRequest, settle
from fall.wild_loader import (
    LEGAL_SETTLE,
    REPO_SETTLE,
    SUPERSEDED_LEGAL_TRAP,
    WILD_QUERIES,
    load_bridge_only,
    default_wild_data_root,
)

FS = WILD_DENSE_FIXTURE_SET


@dataclass
class StressResult:
    name: str
    passed: bool
    detail: str


def run_stress_harness(conn: sqlite3.Connection) -> list[StressResult]:
    """Run pack-aligned stress cases against an loaded wild_dense db."""
    results: list[StressResult] = []

    # --- Settle law ---
    try:
        settle(
            conn,
            SettleRequest(
                body=SUPERSEDED_LEGAL_TRAP["body"],
                source_ref=SUPERSEDED_LEGAL_TRAP["source_ref"],
                author="user",
                pool_id=SUPERSEDED_LEGAL_TRAP["pool_id"],
                fixture_set=FS,
            ),
        )
        results.append(StressResult("refuse_superseded_mar15", False, "should have refused"))
    except SettleRefused as e:
        ok = "superseded" in e.reason.lower()
        results.append(
            StressResult("refuse_superseded_mar15", ok, e.reason)
        )

    try:
        settle(
            conn,
            SettleRequest(
                body=LEGAL_SETTLE["body"],
                source_ref="wrong:ref",
                author="user",
                pool_id=LEGAL_SETTLE["pool_id"],
                fixture_set=FS,
            ),
        )
        results.append(StressResult("source_lock", False, "should have refused"))
    except SettleRefused as e:
        ok = "source_ref must match pool_id" in e.reason
        results.append(StressResult("source_lock", ok, e.reason))

    # --- Positive settles ---
    for label, spec in (("legal_controls", LEGAL_SETTLE), ("repo_controls", REPO_SETTLE)):
        try:
            settle(
                conn,
                SettleRequest(
                    body=spec["body"],
                    source_ref=spec["source_ref"],
                    author="user",
                    pool_id=spec["pool_id"],
                    fixture_set=FS,
                    basis="verbatim",
                ),
            )
            results.append(StressResult(f"settle_{label}", True, "ok"))
        except SettleRefused as e:
            results.append(StressResult(f"settle_{label}", False, e.reason))

    # --- Exhale expectations ---
    legal_packet = exhale(
        conn,
        WILD_QUERIES["legal_deadline"],
        k=8,
        fixture_set=FS,
        domain="legal",
        infer_domain_scope=False,
    )
    legal_text = " ".join(
        (p.get("text") or "") for p in legal_packet["pressure"]
    ).lower()
    has_amended = "april 29" in legal_text or any(
        LEGAL_SETTLE["pool_id"] in (p.get("id") or "") for p in legal_packet["pressure"]
    )
    results.append(
        StressResult(
            "legal_deadline_surfaces_controls",
            has_amended or bool(legal_packet["scent"]),
            "amended order or controls scent expected",
        )
    )

    repo_packet = exhale(
        conn,
        WILD_QUERIES["repo_architecture"],
        k=8,
        fixture_set=FS,
        domain="repo",
        infer_domain_scope=False,
    )
    repo_ids = {p.get("id") for p in repo_packet["pressure"]}
    monolith_trap = "repo:fake-api:adr-001-monolith-2024-11-10" in repo_ids
    has_silence_or_scent = bool(repo_packet["silence"]) or any(
        s.get("kind") == "supersession" for s in repo_packet["scent"]
    )
    results.append(
        StressResult(
            "repo_architecture_genealogy",
            has_silence_or_scent or monolith_trap,
            "superseded monolith surfaced as scent/silence/pressure trap",
        )
    )

    cross = exhale(conn, WILD_QUERIES["cross_domain"], k=6, fixture_set=FS)
    results.append(
        StressResult(
            "cross_domain_dual_ground",
            len(cross["ground"]) >= 2,
            f"ground count={len(cross['ground'])}",
        )
    )
    results.append(
        StressResult(
            "cross_domain_warnings",
            bool(cross["warning"]),
            "ground+pressure bleed warning expected",
        )
    )

    bridge = exhale(conn, WILD_QUERIES["bridge_hostile"], k=6, fixture_set=FS)
    if not any(p.get("domain") == "bridge" for p in bridge["pressure"]):
        try:
            load_bridge_only(conn, data_root=default_wild_data_root())
        except FileNotFoundError:
            pass
        bridge = exhale(conn, WILD_QUERIES["bridge_hostile"], k=6, fixture_set=FS)
    bridge_in_ground = any(
        "monolith Friday" in (g.get("text") or "") for g in bridge["ground"]
    )
    results.append(
        StressResult(
            "bridge_not_ground",
            not bridge_in_ground,
            "bridge must not appear in ground",
        )
    )
    bridge_pressure = any(
        p.get("domain") == "bridge" for p in bridge["pressure"]
    )
    results.append(
        StressResult(
            "bridge_in_pressure",
            bridge_pressure,
            "bridge echo expected in pressure",
        )
    )

    return results


def all_passed(results: list[StressResult]) -> bool:
    return all(r.passed for r in results)
