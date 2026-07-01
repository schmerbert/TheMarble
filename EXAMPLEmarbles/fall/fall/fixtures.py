"""Fixture wash-in — trap chunks and infinity braid for flow demos."""

from __future__ import annotations

import sqlite3

from fall.breath import FIXTURE_SET, INFINITY_FIXTURE_SET, to_pool, wash_in


# --- dry_run_v1 (minimal hostile demo; tests depend on these ids) ---

FIXTURE_CHUNKS = [
    {
        "id": "pool-001",
        "body": "I feel clear now; practice is going well.",
        "source_ref": None,
        "author": "instance",
    },
    {
        "id": "pool-002",
        "body": "The user probably prefers simplicity and quiet tools.",
        "source_ref": None,
        "author": "instance",
    },
    {
        "id": "pool-003",
        "body": "Didn't we already decide Thursday was settled for the call?",
        "source_ref": "fixture:hedged-memory",
        "author": "instance",
    },
    {
        "id": "pool-004",
        "body": "Move is October 31 — user stated directly, unhedged.",
        "source_ref": "fixture:user-2026-07-01-move",
        "author": "user",
    },
    {
        "id": "pool-005",
        "body": "Similarity is high but this is only churn from an old session summary.",
        "source_ref": "fixture:session-archive",
        "author": "instance",
    },
    {
        "id": "pool-006",
        "body": "Breath routing should stay receive-only; the village drinks downstream.",
        "source_ref": "fixture:design-note",
        "author": "user",
    },
]


# --- infinity_v1 (figure-eight flow demo) ---

INFINITY_POOL_CHUNKS = [
    # Left lobe — spray (never auto-close)
    {
        "id": "pool-L1",
        "body": "I feel clear now; practice is going well.",
        "source_ref": None,
        "author": "instance",
    },
    {
        "id": "pool-L2",
        "body": "Didn't we already decide Thursday was settled for the call?",
        "source_ref": "fixture:hedged-memory",
        "author": "instance",
    },
    {
        "id": "pool-L3",
        "body": "The user probably prefers quiet tools and minimal noise.",
        "source_ref": None,
        "author": "instance",
    },
    {
        "id": "pool-L4",
        "body": "Session summary: things are flowing nicely with the new rhythm.",
        "source_ref": "fixture:session-summary",
        "author": "instance",
    },
    # Right lobe — depth candidates (sourced)
    {
        "id": "pool-R1",
        "body": "Move is October 31 — user stated directly, unhedged.",
        "source_ref": "fixture:user-2026-07-01-move",
        "author": "user",
    },
    {
        "id": "pool-R2",
        "body": "Breath routing should stay receive-only; the village drinks downstream.",
        "source_ref": "fixture:design-note",
        "author": "user",
    },
    {
        "id": "pool-R3",
        "body": "Stream contract is fall/stream/v1 — labels required on every packet.",
        "source_ref": "fixture:stream-contract",
        "author": "user",
    },
    {
        "id": "pool-R4",
        "body": "Shift stone returned wet side up at end of shift.",
        "source_ref": "fixture:handoff-2026-07-01",
        "author": "instance",
    },
]

INFINITY_BRIDGE_WASHES = [
    {
        "id": "wash-X1",
        "body": 'Downstream echo: "practice is going well and the move is handled."',
        "source_ref": None,
        "author": "instance",
    },
    {
        "id": "wash-X2",
        "body": "Channel correction: only fixture:user-2026-07-01-move may ground the move date.",
        "source_ref": "fixture:channel-2026-07-01",
        "author": "user",
    },
]

INFINITY_QUERIES = {
    "spray": "what is practice going well",
    "crossing": "what should downstream believe about practice and the move",
    "return": "is practice going well and move handled",
    "after_correction": "is practice going well and move handled",
}


def _seed_chunks(
    conn: sqlite3.Connection,
    chunks: list[dict],
    *,
    fixture_set: str,
) -> None:
    for chunk in chunks:
        wash_in(
            conn,
            chunk["body"],
            source_ref=chunk["source_ref"],
            author=chunk["author"],
            fixture_set=fixture_set,
        )
        to_pool(
            conn,
            chunk["id"],
            chunk["body"],
            source_ref=chunk["source_ref"],
            author=chunk["author"],
            fixture_set=fixture_set,
        )


def seed_fixture_pool(conn: sqlite3.Connection) -> None:
    _seed_chunks(conn, FIXTURE_CHUNKS, fixture_set=FIXTURE_SET)


def seed_infinity_pool(conn: sqlite3.Connection) -> None:
    _seed_chunks(conn, INFINITY_POOL_CHUNKS, fixture_set=INFINITY_FIXTURE_SET)


def inhale_bridge(conn: sqlite3.Connection, bridge: dict) -> str:
    """Wash a bridge chunk into pool (return leg of the infinity loop)."""
    wash_in(
        conn,
        bridge["body"],
        source_ref=bridge["source_ref"],
        author=bridge["author"],
        fixture_set=INFINITY_FIXTURE_SET,
    )
    to_pool(
        conn,
        bridge["id"],
        bridge["body"],
        source_ref=bridge["source_ref"],
        author=bridge["author"],
        fixture_set=INFINITY_FIXTURE_SET,
    )
    return bridge["id"]
