"""Settle — the only pool → depth crossing."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fall.breath import fetch_pool_genealogy
from fall.edges import edge_settle_refusal
from fall.metadata import meta_json_dumps, settle_refusal_reason
from fall.surface_state import mark_surface_dirty


class SettleRefused(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


@dataclass
class SettleRequest:
    body: str
    source_ref: str | None
    author: str | None
    pool_id: str | None = None
    fixture_set: str | None = None
    use_limit: str | None = "within stated source only"
    basis: str = "user_confirmation"  # user_confirmation | verbatim | synthesis


def _requires_source_lock(pool_id: str | None, genealogy: dict[str, Any] | None) -> bool:
    if not pool_id:
        return False
    if pool_id.startswith(("legal:", "repo:", "wild:")):
        return True
    return bool(genealogy and genealogy.get("meta"))


def _audit(
    conn: sqlite3.Connection,
    *,
    pool_id: str | None,
    body: str,
    source_ref: str | None,
    author: str | None,
    outcome: str,
    reason: str,
) -> None:
    conn.execute(
        """
        INSERT INTO settle_audit (attempted_at, pool_id, body, source_ref, author, outcome, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            pool_id,
            body,
            source_ref,
            author,
            outcome,
            reason,
        ),
    )


def settle(conn: sqlite3.Connection, req: SettleRequest) -> str:
    """Attempt Settle. Returns depth_entry id or raises SettleRefused."""
    body = (req.body or "").strip()
    if not body:
        reason = "empty body"
        _audit(conn, pool_id=req.pool_id, body=body, source_ref=req.source_ref,
               author=req.author, outcome="refused", reason=reason)
        raise SettleRefused(reason)

    if not req.source_ref or not str(req.source_ref).strip():
        reason = "spray mistaken for depth - source_ref required"
        _audit(conn, pool_id=req.pool_id, body=body, source_ref=req.source_ref,
               author=req.author, outcome="refused", reason=reason)
        raise SettleRefused(reason)

    if req.author not in ("user", "instance"):
        reason = "author must be user or instance"
        _audit(conn, pool_id=req.pool_id, body=body, source_ref=req.source_ref,
               author=req.author, outcome="refused", reason=reason)
        raise SettleRefused(reason)

    if req.basis == "synthesis" and not req.pool_id:
        reason = "synthesis must cite pool_id"
        _audit(conn, pool_id=req.pool_id, body=body, source_ref=req.source_ref,
               author=req.author, outcome="refused", reason=reason)
        raise SettleRefused(reason)

    genealogy = fetch_pool_genealogy(conn, req.pool_id)
    if genealogy:
        refusal = settle_refusal_reason(
            domain=genealogy.get("domain"),
            record_status=genealogy.get("record_status"),
            meta=genealogy.get("meta") or {},
        )
        if refusal:
            _audit(
                conn,
                pool_id=req.pool_id,
                body=body,
                source_ref=req.source_ref,
                author=req.author,
                outcome="refused",
                reason=refusal,
            )
            raise SettleRefused(refusal)

    edge_refusal = edge_settle_refusal(conn, req.pool_id)
    if edge_refusal:
        _audit(
            conn,
            pool_id=req.pool_id,
            body=body,
            source_ref=req.source_ref,
            author=req.author,
            outcome="refused",
            reason=edge_refusal,
        )
        raise SettleRefused(edge_refusal)

    if _requires_source_lock(req.pool_id, genealogy):
        if req.source_ref.strip() != (req.pool_id or "").strip():
            reason = "source_ref must match pool_id for pack records"
            _audit(
                conn,
                pool_id=req.pool_id,
                body=body,
                source_ref=req.source_ref,
                author=req.author,
                outcome="refused",
                reason=reason,
            )
            raise SettleRefused(reason)

    pool_domain = genealogy.get("domain") if genealogy else None
    pool_status = genealogy.get("record_status") if genealogy else None
    pool_meta_json = None
    if genealogy and genealogy.get("meta"):
        pool_meta_json = meta_json_dumps(genealogy["meta"])

    depth_id = f"depth-{uuid.uuid4().hex[:12]}"
    conn.execute(
        """
        INSERT INTO depth_entry (
            id, settled_at, body, source_ref, fixture_set, author, authority,
            use_limit, from_pool_id, domain, record_status, meta_json
        )
        VALUES (?, ?, ?, ?, ?, ?, 'ground', ?, ?, ?, ?, ?)
        """,
        (
            depth_id,
            datetime.now(timezone.utc).isoformat(),
            body,
            req.source_ref.strip(),
            req.fixture_set,
            req.author,
            req.use_limit,
            req.pool_id,
            pool_domain,
            pool_status or "settled",
            pool_meta_json,
        ),
    )
    _audit(
        conn,
        pool_id=req.pool_id,
        body=body,
        source_ref=req.source_ref,
        author=req.author,
        outcome="settled",
        reason=f"settled via {req.basis}",
    )
    mark_surface_dirty(conn)
    return depth_id
