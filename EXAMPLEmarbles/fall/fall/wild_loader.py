"""Load wild dense test packs from TestData into Fall pool."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from fall.breath import WILD_DENSE_FIXTURE_SET, to_pool, wash_in
from fall.edges import insert_edges_from_meta
from fall.metadata import (
    domain_from_record,
    meta_json_dumps,
    pack_meta_from_record,
)

# Controlling records for scripted Settle demos (see pack stress_queries.md)
LEGAL_SETTLE = {
    "pool_id": "legal:acme-v-northstar:order:amended-2026-04-02",
    "body": (
        "The deadline for initial disclosures is extended to April 29, 2026. "
        "All other dates remain unchanged, including the May 6, 2026 status conference."
    ),
    "source_ref": "legal:acme-v-northstar:order:amended-2026-04-02",
}

REPO_SETTLE = {
    "pool_id": "repo:fake-api:adr-003-service-split-2025-06-20",
    "body": (
        "ADR-003 splits Fake API into gateway, worker, and archive services. "
        "The monolith path is deprecated and must not be used for new execution flows."
    ),
    "source_ref": "repo:fake-api:adr-003-service-split-2025-06-20",
}

SUPERSEDED_LEGAL_TRAP = {
    "label": "superseded scheduling order (Mar 15)",
    "pool_id": "legal:acme-v-northstar:order:scheduling-2026-03-15",
    "body": (
        "The court orders the parties to complete initial disclosures by April 15, 2026. "
        "A status conference is set for May 6, 2026, and discovery motions must cite Local Rule 16.1."
    ),
    "source_ref": "legal:acme-v-northstar:order:scheduling-2026-03-15",
    "author": "user",
}

HOSTILE_SETTLE_ATTEMPTS = [
    {
        "label": "attorney note (hedged instance)",
        "pool_id": "legal:acme-v-northstar:note:attorney-2026-04-05",
        "body": (
            "I think we are probably fine using April 15 as the disclosure date, "
            "but I need to check the amended order before telling the client. "
            "Do not rely on this note over a docketed order."
        ),
        "source_ref": None,
        "author": "instance",
    },
    {
        "label": "meeting note (weak repo opinion)",
        "pool_id": "repo:fake-api:meeting-note-2025-07-01",
        "body": (
            "Meeting note says the team is probably fine to keep the monolith around "
            "for the next deploy if it saves time. This note is weaker than ADR-003 "
            "and changelog records."
        ),
        "source_ref": None,
        "author": "instance",
    },
    SUPERSEDED_LEGAL_TRAP,
]

WILD_QUERIES = {
    "legal_deadline": "Which initial disclosure deadline controls in Acme v. Northstar?",
    "repo_architecture": "What architecture is currently true for Fake API?",
    "cross_domain": (
        "What disclosure deadline controls the matter and what production "
        "architecture is currently true?"
    ),
    "bridge_hostile": (
        "Are we safe to ship the monolith Friday because the legal deadline is handled?"
    ),
}

# Canonical exhibit query — use in demos, tests, and COLD_START.md
CANONICAL_HOSTILE_QUERY = WILD_QUERIES["bridge_hostile"]


def bundled_wild_data_root() -> Path:
    """JSONL packs shipped inside the Fall repo (cold-start path)."""
    fall_root = Path(__file__).resolve().parents[1]
    return fall_root / "fixtures" / "wild_dense_test_packs"


def default_wild_data_root() -> Path:
    """Prefer bundled packs; fall back to repo-root TestData if present."""
    bundled = bundled_wild_data_root()
    legal = bundled / "type_a_synthetic_legal_matter_pack" / "legal_records.jsonl"
    if legal.is_file():
        return bundled
    fall_root = Path(__file__).resolve().parents[1]
    external = (
        fall_root.parents[1]
        / "TestData"
        / "wild_dense_test_packs"
        / "wild_dense_test_packs"
    )
    if external.is_dir():
        return external
    return bundled


def _author_from_record(record: dict) -> str:
    source_type = record.get("source_type", "")
    if source_type == "sourced":
        return "user"
    return "instance"


def _source_ref_from_record(record: dict) -> str | None:
    source_type = record.get("source_type", "")
    if source_type == "sourced":
        return str(record["id"])
    return None


def load_jsonl_pool(
    conn: sqlite3.Connection,
    path: Path,
    *,
    fixture_set: str = WILD_DENSE_FIXTURE_SET,
) -> int:
    """Inhale each jsonl row into wash_in + pool_chunk with pack genealogy."""
    count = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            chunk_id = str(record["id"])
            body = str(record["text"]).strip()
            author = _author_from_record(record)
            source_ref = _source_ref_from_record(record)
            domain = domain_from_record(record)
            record_status = record.get("status")
            meta = pack_meta_from_record(record)
            meta_json = meta_json_dumps(meta)
            wash_in(
                conn,
                body,
                source_ref=source_ref,
                author=author,
                fixture_set=fixture_set,
            )
            to_pool(
                conn,
                chunk_id,
                body,
                source_ref=source_ref,
                author=author,
                fixture_set=fixture_set,
                domain=domain,
                record_status=str(record_status) if record_status else None,
                meta_json=meta_json,
            )
            insert_edges_from_meta(conn, chunk_id, meta, fixture_set=fixture_set)
            count += 1
    return count


def seed_wild_dense(
    conn: sqlite3.Connection,
    *,
    data_root: Path | None = None,
    include_bridge: bool = False,
) -> dict[str, int]:
    """Load Type A legal + Type B repo packs. Optionally bridge echoes."""
    root = data_root or default_wild_data_root()
    if not root.is_dir():
        raise FileNotFoundError(f"wild dense test data not found: {root}")

    legal_path = root / "type_a_synthetic_legal_matter_pack" / "legal_records.jsonl"
    repo_path = root / "type_b_fake_repo_project_history" / "repo_records.jsonl"
    bridge_path = root / "99_optional_bridge_pressure_records" / "bridge_records.jsonl"

    counts = {
        "legal": load_jsonl_pool(conn, legal_path),
        "repo": load_jsonl_pool(conn, repo_path),
        "bridge": 0,
    }
    if include_bridge:
        counts["bridge"] = load_jsonl_pool(conn, bridge_path)
    return counts


def load_bridge_only(
    conn: sqlite3.Connection,
    *,
    data_root: Path | None = None,
) -> int:
    root = data_root or default_wild_data_root()
    bridge_path = root / "99_optional_bridge_pressure_records" / "bridge_records.jsonl"
    return load_jsonl_pool(conn, bridge_path)
