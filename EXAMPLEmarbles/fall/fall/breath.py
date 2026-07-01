"""Inhale, classify, summon, exhale — the shift."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any

from fall.embed import blob_to_embedding, cosine, embed_text, embedding_to_blob
from fall.edges import enrich_hit_with_edges
from fall.metadata import build_scent, hit_from_row, infer_domain, meta_json_loads
from fall.silence import build_exhale_silence
from fall.intake import live_receipt_slot_count, recent_live_receipt_rows
from fall.surface_state import mark_surface_dirty
from fall.warnings import build_exhale_warnings


FIXTURE_SET = "dry_run_v1"
INFINITY_FIXTURE_SET = "infinity_v1"
WILD_DENSE_FIXTURE_SET = "wild_dense_v1"

_POOL_SELECT = """
    SELECT id, body, source_ref, fixture_set, author, embedding,
           domain, record_status, meta_json
    FROM pool_chunk
"""


def wash_in(
    conn: sqlite3.Connection,
    body: str,
    *,
    source_ref: str | None,
    author: str,
    fixture_set: str | None = FIXTURE_SET,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO wash_in (washed_at, body, source_ref, fixture_set, author)
        VALUES (?, ?, ?, ?, ?)
        """,
        (datetime.now(timezone.utc).isoformat(), body, source_ref, fixture_set, author),
    )
    return int(cur.lastrowid)


def to_pool(
    conn: sqlite3.Connection,
    chunk_id: str,
    body: str,
    *,
    source_ref: str | None,
    author: str,
    fixture_set: str | None = FIXTURE_SET,
    domain: str | None = None,
    record_status: str | None = None,
    meta_json: str | None = None,
) -> None:
    emb = embedding_to_blob(embed_text(body))
    conn.execute(
        """
        INSERT INTO pool_chunk (
            id, washed_at, body, source_ref, fixture_set, author, authority,
            embedding, domain, record_status, meta_json
        )
        VALUES (?, ?, ?, ?, ?, ?, 'pressure', ?, ?, ?, ?)
        """,
        (
            chunk_id,
            datetime.now(timezone.utc).isoformat(),
            body,
            source_ref,
            fixture_set,
            author,
            emb,
            domain,
            record_status,
            meta_json,
        ),
    )


def _score_pool(
    conn: sqlite3.Connection,
    query: str,
    *,
    fixture_set: str | None = None,
    domain: str | None = None,
) -> list[tuple[float, dict]]:
    qvec = embed_text(query)
    rows = conn.execute(_POOL_SELECT).fetchall()
    scored: list[tuple[float, dict]] = []
    for row in rows:
        if fixture_set and row["fixture_set"] != fixture_set:
            continue
        if domain and row["domain"] != domain:
            continue
        sim = cosine(qvec, blob_to_embedding(row["embedding"]))
        hit = enrich_hit_with_edges(conn, hit_from_row(row, sim))
        scored.append((sim, hit))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def summon_pool(
    conn: sqlite3.Connection,
    query: str,
    *,
    k: int = 3,
    fixture_set: str | None = None,
    domain: str | None = None,
    receipt_slots: int = 0,
) -> list[dict]:
    ranked = _score_pool(conn, query, fixture_set=fixture_set, domain=domain)
    if receipt_slots <= 0:
        return [item for _, item in ranked[:k]]

    qvec = embed_text(query)
    receipt_hits: list[dict] = []
    chosen: set[str] = set()
    for row in recent_live_receipt_rows(conn, domain=domain, max_slots=receipt_slots):
        sim = cosine(qvec, blob_to_embedding(row["embedding"]))
        hit = enrich_hit_with_edges(conn, hit_from_row(row, sim))
        hit["summon_kind"] = "receipt"
        receipt_hits.append(hit)
        chosen.add(hit["id"])

    merged = list(receipt_hits)
    for _, hit in ranked:
        if len(merged) >= k:
            break
        if hit["id"] not in chosen:
            merged.append(hit)
            chosen.add(hit["id"])
    return merged[:k]


def load_depth(
    conn: sqlite3.Connection,
    *,
    fixture_set: str | None = None,
    domain: str | None = None,
) -> list[dict]:
    sql = """
        SELECT id, body, source_ref, use_limit, domain, record_status, meta_json
        FROM depth_entry
        WHERE 1=1
    """
    params: list[Any] = []
    if fixture_set:
        sql += " AND fixture_set = ?"
        params.append(fixture_set)
    if domain:
        sql += " AND domain = ?"
        params.append(domain)
    rows = conn.execute(sql, params).fetchall()
    out: list[dict] = []
    for r in rows:
        entry: dict[str, Any] = {
            "id": r["id"],
            "text": r["body"],
            "authority": "ground",
            "source_ref": r["source_ref"],
            "use_limit": r["use_limit"],
        }
        if r["domain"]:
            entry["domain"] = r["domain"]
        if r["record_status"]:
            entry["record_status"] = r["record_status"]
        meta = meta_json_loads(r["meta_json"])
        if meta.get("supersedes"):
            entry["supersedes"] = meta["supersedes"]
        out.append(entry)
    return out


def exhale(
    conn: sqlite3.Connection,
    query: str,
    *,
    k: int = 3,
    max_pressure_chars: int = 280,
    fixture_set: str | None = FIXTURE_SET,
    domain: str | None = None,
    infer_domain_scope: bool = True,
) -> dict:
    domain_inferred = False
    effective_domain = domain
    if effective_domain is None and infer_domain_scope:
        effective_domain = infer_domain(query)
        domain_inferred = effective_domain is not None

    pool_hits = summon_pool(
        conn,
        query,
        k=k,
        fixture_set=fixture_set,
        domain=effective_domain,
        receipt_slots=(
            live_receipt_slot_count(conn, domain=effective_domain)
            if fixture_set is None
            else 0
        ),
    )
    scored = _score_pool(
        conn, query, fixture_set=fixture_set, domain=effective_domain
    )
    scan_hits = [hit for _, hit in scored[: max(k, 12)]]
    ground = load_depth(conn, fixture_set=fixture_set, domain=effective_domain)

    pressure = []
    remaining = max_pressure_chars
    for hit in pool_hits:
        excerpt = hit["text"][: min(len(hit["text"]), max(40, remaining))]
        if not excerpt:
            break
        pressure.append({**hit, "text": excerpt})
        remaining -= len(excerpt)

    warnings = build_exhale_warnings(pool_hits, ground)
    scent = build_scent(
        pool_hits,
        domain=effective_domain,
        domain_inferred=domain_inferred,
    )
    silence = build_exhale_silence(scan_hits, pressure)
    receipt_count = sum(1 for h in pool_hits if h.get("summon_kind") == "receipt")

    wash_count = conn.execute("SELECT COUNT(*) AS c FROM wash_in").fetchone()["c"]

    packet: dict[str, Any] = {
        "stream_version": "fall/stream/v1",
        "stream_id": str(uuid.uuid4()),
        "source": "fall",
        "fixture_set": fixture_set,
        "query": query,
        "ground": ground,
        "pressure": pressure,
        "warning": warnings,
        "scent": scent,
        "silence": silence,
        "meta": {
            "wash_in_count": wash_count,
            "pool_hits": len(pool_hits),
            "receipt_slots": receipt_count,
            "hybrid_summon": receipt_count > 0,
            "silence_count": len(silence),
            "domain_scope": effective_domain,
            "domain_inferred": domain_inferred,
            "exhale_bytes": 0,
        },
    }

    payload = json.dumps(packet, indent=2)
    packet["meta"]["exhale_bytes"] = len(payload.encode("utf-8"))

    conn.execute(
        """
        INSERT INTO stream_packet (id, exhaled_at, stream_version, query, fixture_set, payload_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            packet["stream_id"],
            datetime.now(timezone.utc).isoformat(),
            packet["stream_version"],
            query,
            fixture_set,
            json.dumps(packet),
        ),
    )
    mark_surface_dirty(conn)
    return packet


def fetch_pool_genealogy(conn: sqlite3.Connection, pool_id: str | None) -> dict[str, Any] | None:
    if not pool_id:
        return None
    row = conn.execute(
        "SELECT domain, record_status, meta_json FROM pool_chunk WHERE id = ?",
        (pool_id,),
    ).fetchone()
    if not row:
        return None
    return {
        "domain": row["domain"],
        "record_status": row["record_status"],
        "meta": meta_json_loads(row["meta_json"]),
    }
