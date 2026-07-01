"""SQLite store for Fall."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fall.edges import ensure_edges_table

# Columns added in spirit_v2 (genealogy pass). Safe to run on existing DBs.
_POOL_GENEALOGY_COLUMNS = (
    ("domain", "TEXT"),
    ("record_status", "TEXT"),
    ("meta_json", "TEXT"),
)

_HANDOFF_SURFACE_COLUMNS = (
    ("surface_frozen_at", "TEXT"),
    ("surface_dirty", "INTEGER NOT NULL DEFAULT 0"),
)


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def migrate_schema(conn: sqlite3.Connection) -> None:
    """Add genealogy columns and pool_edge to existing databases without wiping data."""
    for table in ("pool_chunk", "depth_entry"):
        existing = _table_columns(conn, table)
        for name, col_type in _POOL_GENEALOGY_COLUMNS:
            if name not in existing:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {col_type}")
    ensure_edges_table(conn)
    existing_handoff = _table_columns(conn, "handoff")
    for name, col_type in _HANDOFF_SURFACE_COLUMNS:
        if name not in existing_handoff:
            conn.execute(f"ALTER TABLE handoff ADD COLUMN {name} {col_type}")
    conn.commit()


def init_db(conn: sqlite3.Connection, schema_path: Path) -> None:
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    migrate_schema(conn)
    conn.commit()
