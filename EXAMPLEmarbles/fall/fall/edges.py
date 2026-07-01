"""Queryable genealogy edges — glass law for supersession."""

from __future__ import annotations

import sqlite3
from typing import Any


def ensure_edges_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pool_edge (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          from_id TEXT NOT NULL,
          to_id TEXT NOT NULL,
          kind TEXT NOT NULL CHECK (kind IN ('supersedes', 'superseded_by')),
          fixture_set TEXT,
          UNIQUE(from_id, to_id, kind)
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_pool_edge_from ON pool_edge(from_id, kind)"
    )


def _insert_edge(
    conn: sqlite3.Connection,
    from_id: str,
    to_id: str,
    kind: str,
    *,
    fixture_set: str | None,
) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO pool_edge (from_id, to_id, kind, fixture_set)
        VALUES (?, ?, ?, ?)
        """,
        (from_id, to_id, kind, fixture_set),
    )


def insert_edges_from_meta(
    conn: sqlite3.Connection,
    chunk_id: str,
    meta: dict[str, Any],
    *,
    fixture_set: str | None,
) -> int:
    """Load supersedes / superseded_by edges from pack meta. Returns count added."""
    n = 0
    for target in meta.get("supersedes") or []:
        _insert_edge(conn, chunk_id, str(target), "supersedes", fixture_set=fixture_set)
        _insert_edge(conn, str(target), chunk_id, "superseded_by", fixture_set=fixture_set)
        n += 1
    for target in meta.get("superseded_by") or []:
        _insert_edge(conn, chunk_id, str(target), "superseded_by", fixture_set=fixture_set)
        _insert_edge(conn, str(target), chunk_id, "supersedes", fixture_set=fixture_set)
        n += 1
    return n


def superseded_by_targets(conn: sqlite3.Connection, pool_id: str) -> list[str]:
    rows = conn.execute(
        """
        SELECT to_id FROM pool_edge
        WHERE from_id = ? AND kind = 'superseded_by'
        ORDER BY to_id
        """,
        (pool_id,),
    ).fetchall()
    return [r["to_id"] for r in rows]


def edge_settle_refusal(conn: sqlite3.Connection, pool_id: str | None) -> str | None:
    if not pool_id:
        return None
    targets = superseded_by_targets(conn, pool_id)
    if targets:
        return f"record is superseded by edge - see {', '.join(targets)}"
    return None


def enrich_hit_with_edges(conn: sqlite3.Connection, hit: dict[str, Any]) -> dict[str, Any]:
    pid = hit.get("id")
    if not pid or hit.get("superseded_by"):
        return hit
    targets = superseded_by_targets(conn, pid)
    if targets:
        hit = {**hit, "superseded_by": targets}
    return hit
