"""Live wash intake — what the instance needs to feel after bulk wash-in."""

from __future__ import annotations

import sqlite3
from typing import Any


def live_wash_stats(conn: sqlite3.Connection) -> dict[str, Any]:
    """Counts for fixture_set IS NULL chunks (user/live wash, not rehearsal pack)."""
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM pool_chunk WHERE fixture_set IS NULL"
    ).fetchone()["c"]
    unsigned = conn.execute(
        """
        SELECT COUNT(*) AS c FROM pool_chunk
        WHERE fixture_set IS NULL AND (source_ref IS NULL OR source_ref = '')
        """
    ).fetchone()["c"]
    hedged = conn.execute(
        """
        SELECT COUNT(*) AS c FROM pool_chunk
        WHERE fixture_set IS NULL AND lower(record_status) = 'hedged'
        """
    ).fetchone()["c"]
    by_domain = conn.execute(
        """
        SELECT domain, COUNT(*) AS c
        FROM pool_chunk
        WHERE fixture_set IS NULL AND domain IS NOT NULL
        GROUP BY domain
        """
    ).fetchall()
    return {
        "count": count,
        "unsigned": unsigned,
        "hedged": hedged,
        "by_domain": {r["domain"]: r["c"] for r in by_domain},
    }


def recent_live_chunks(conn: sqlite3.Connection, *, limit: int = 6) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT id, body, source_ref, domain, record_status, author
        FROM pool_chunk
        WHERE fixture_set IS NULL
        ORDER BY washed_at DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        text = (r["body"] or "").strip()
        if len(text) > 120:
            text = text[:117] + "..."
        out.append(
            {
                "id": r["id"],
                "text": text,
                "authority": "pressure",
                "source_ref": r["source_ref"],
                "domain": r["domain"],
                "record_status": r["record_status"],
                "author": r["author"],
            }
        )
    return out


def recent_live_receipt_rows(
    conn: sqlite3.Connection,
    *,
    domain: str | None = None,
    max_slots: int = 2,
) -> list[sqlite3.Row]:
    """Newest live chunk per domain — recency receipt, not embed rank."""
    if domain:
        row = conn.execute(
            """
            SELECT id, body, source_ref, fixture_set, author, embedding,
                   domain, record_status, meta_json
            FROM pool_chunk
            WHERE fixture_set IS NULL AND domain = ?
            ORDER BY washed_at DESC, id DESC
            LIMIT 1
            """,
            (domain,),
        ).fetchone()
        return [row] if row else []

    rows = conn.execute(
        """
        SELECT p.id, p.body, p.source_ref, p.fixture_set, p.author, p.embedding,
               p.domain, p.record_status, p.meta_json
        FROM pool_chunk p
        WHERE p.fixture_set IS NULL
          AND p.domain IS NOT NULL
          AND p.id = (
              SELECT id FROM pool_chunk
              WHERE fixture_set IS NULL AND domain = p.domain
              ORDER BY washed_at DESC, id DESC
              LIMIT 1
          )
        ORDER BY p.washed_at DESC, p.id DESC
        LIMIT ?
        """,
        (max_slots,),
    ).fetchall()
    return list(rows)


def live_receipt_slot_count(conn: sqlite3.Connection, *, domain: str | None = None) -> int:
    """How many receipt slots hybrid summon reserves on --live exhale."""
    stats = live_wash_stats(conn)
    if not stats.get("count"):
        return 0
    if domain:
        return 1 if stats.get("by_domain", {}).get(domain) else 0
    by_dom = stats.get("by_domain") or {}
    return min(len(by_dom), 2)


def intake_posture_lines(stats: dict[str, Any]) -> list[str]:
    """Shift-card lines when live wash is in the churn."""
    if not stats.get("count"):
        return []
    n = stats["count"]
    lines = [
        f"- **{n} live chunk(s)** in churn (not rehearsal pack)",
    ]
    if stats.get("by_domain"):
        dom = ", ".join(f"{k}={v}" for k, v in stats["by_domain"].items())
        lines.append(f"- live by domain: {dom}")
    if stats.get("unsigned"):
        lines.append(f"- **{stats['unsigned']} unsigned** - nearness is not Settle")
    if stats.get("hedged"):
        lines.append(f"- **{stats['hedged']} hedged** - feel, do not Settle")
    lines.extend(
        [
            "- **Summon live pool:** `exhale \"your query\" --live --db fixtures/fall_wild.db`",
            "- **`--live` exhale** hybrid summons: receipt slot per live domain + embed rank",
            "- **`--wild` alone** scopes rehearsal pack - omits live wash",
            "- **Rank != receipt** - imports may not top generic queries; ask targeted questions",
            "- **Order:** wash -> status -> exhale --live for work -> arrive when shift ends",
        ]
    )
    return lines


def cli_inhale_ack(*, live: bool, stats: dict[str, Any] | None = None) -> str:
    if not live:
        return "inhale -> pool (rehearsal fixture_set). Live user wash: add --live."
    n = (stats or {}).get("count", 1)
    return (
        f"inhale -> pool (live wash). {n} live chunk(s) in churn. "
        "Next: exhale --live for questions; arrive when shift ends."
    )
