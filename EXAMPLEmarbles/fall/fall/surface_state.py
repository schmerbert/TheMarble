"""SURFACE freshness — when arrival mist goes stale."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fall.db import migrate_schema

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SURFACE = ROOT / "SURFACE.md"


def mark_surface_dirty(
    conn: sqlite3.Connection,
    *,
    surface_path: Path | None = None,
) -> None:
    migrate_schema(conn)
    conn.execute("UPDATE handoff SET surface_dirty = 1 WHERE id = 1")
    write_surface_stale_marker(surface_path or DEFAULT_SURFACE)


def clear_surface_fresh(conn: sqlite3.Connection, frozen_at: str) -> None:
    migrate_schema(conn)
    conn.execute(
        "UPDATE handoff SET surface_dirty = 0, surface_frozen_at = ? WHERE id = 1",
        (frozen_at,),
    )


def write_surface_stale_marker(surface_path: Path) -> None:
    if not surface_path.exists():
        return
    text = surface_path.read_text(encoding="utf-8")
    if text.startswith("> **SURFACE stale"):
        return
    marker = (
        "> **SURFACE stale (mid-shift):** frozen mist is not current churn. "
        "Use `exhale --live` for work now; run `arrive --wild --db fixtures/fall_wild.db` when the shift ends.\n\n"
    )
    surface_path.write_text(marker + text, encoding="utf-8")


def surface_stale_banner(conn: sqlite3.Connection) -> str | None:
    migrate_schema(conn)
    row = conn.execute(
        "SELECT surface_frozen_at, surface_dirty FROM handoff WHERE id = 1"
    ).fetchone()
    if not row:
        return None
    if row["surface_dirty"]:
        return (
            "SURFACE stale (mid-shift): frozen mist outdated. "
            "exhale --live for work; arrive when shift ends."
        )
    frozen = row["surface_frozen_at"]
    if not frozen:
        return None
    latest = conn.execute(
        """
        SELECT MAX(ts) AS ts FROM (
          SELECT settled_at AS ts FROM depth_entry
          UNION ALL
          SELECT exhaled_at AS ts FROM stream_packet
        )
        """
    ).fetchone()["ts"]
    if latest and latest > frozen:
        return (
            f"SURFACE stale (mid-shift): db changed after frozen ({frozen}). "
            "exhale --live for work; arrive when shift ends."
        )
    return None
