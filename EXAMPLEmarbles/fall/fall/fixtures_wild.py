"""Ensure shipped wild demo db exists — cold zip must not depend on external TestData."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.promote import SettleRefused, SettleRequest, settle
from fall.surface import arrival_breath
from fall.wild_loader import (
    CANONICAL_HOSTILE_QUERY,
    HOSTILE_SETTLE_ATTEMPTS,
    LEGAL_SETTLE,
    REPO_SETTLE,
    bundled_wild_data_root,
    default_wild_data_root,
    load_bridge_only,
    seed_wild_dense,
)

FALL_ROOT = Path(__file__).resolve().parents[1]
WILD_DB = FALL_ROOT / "fixtures" / "fall_wild.db"
SCHEMA = FALL_ROOT / "schema.sql"
SURFACE = FALL_ROOT / "SURFACE.md"


def wild_data_available() -> bool:
    root = default_wild_data_root()
    legal = root / "type_a_synthetic_legal_matter_pack" / "legal_records.jsonl"
    return legal.is_file()


def build_wild_demo_db(
    db_path: Path | None = None,
    *,
    surface_path: Path | None = None,
    verbose: bool = False,
) -> Path:
    """Rebuild fall_wild.db from bundled JSONL — same path as wild_run.py."""
    if not wild_data_available():
        raise FileNotFoundError(
            f"wild dense packs missing; expected under {bundled_wild_data_root()}"
        )

    db_path = db_path or WILD_DB
    surface_path = surface_path or SURFACE
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = connect(db_path)
    init_db(conn, SCHEMA)
    data_root = default_wild_data_root()
    seed_wild_dense(conn, data_root=data_root)
    fs = WILD_DENSE_FIXTURE_SET

    for hostile in HOSTILE_SETTLE_ATTEMPTS:
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
            raise RuntimeError(f"hostile settle should refuse: {hostile['label']}")
        except SettleRefused:
            pass

    settle(
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
    settle(
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

    load_bridge_only(conn, data_root=data_root)
    packet = exhale(conn, CANONICAL_HOSTILE_QUERY, k=5, fixture_set=fs)
    if any("monolith Friday" in (g.get("text") or "") for g in packet.get("ground") or []):
        raise RuntimeError("canonical hostile query promoted bridge to ground")

    arrival_breath(conn, fixture_set=fs, surface_path=surface_path)
    conn.commit()
    conn.close()

    if verbose:
        print(f"built {db_path}")
    return db_path


def ensure_wild_demo_db(*, rebuild: bool = False) -> Path:
    """Return path to fall_wild.db, building from bundled JSONL if missing."""
    if WILD_DB.exists() and not rebuild:
        return WILD_DB
    return build_wild_demo_db()
