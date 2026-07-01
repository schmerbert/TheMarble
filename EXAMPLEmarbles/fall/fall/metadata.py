"""Pack genealogy — domain, status, supersession, scent on the stream."""

from __future__ import annotations

import json
import re
from typing import Any

# Statuses that must not cross Settle (spray, stale, superseded, bridge pressure).
NON_SETTLEABLE_STATUSES = frozenset(
    {
        "superseded",
        "stale",
        "stale-reference",
        "historical-context",
        "historical-release",
        "hedged",
        "draft-only",
        "pressure-only",
        "weak-opinion",
        "client-pressure",
        "proposal-only",
        "mixed-accuracy",
        "summary-with-caveats",
        "requested-only",
        "partially-stale",
        "disputed-position",
        "pending",
        "open",
        "temporary",
    }
)

LEGAL_SIGNALS = re.compile(
    r"\b(acme|northstar|disclosure|deposition|court|legal|matter|expert|mediation|compel|scheduling)\b",
    re.I,
)
REPO_SIGNALS = re.compile(
    r"\b(fake api|architecture|monolith|gateway|worker|archive|adr|deploy|changelog|runbook|sync rpc|import)\b",
    re.I,
)


def pack_meta_from_record(record: dict[str, Any]) -> dict[str, Any]:
    """Extract storable genealogy from a wild dense jsonl row."""
    meta: dict[str, Any] = {}
    for key in (
        "record_kind",
        "date",
        "authority_rank",
        "tags",
        "matter",
        "project",
        "supersedes",
        "superseded_by",
    ):
        if key in record and record[key] not in (None, [], ""):
            meta[key] = record[key]
    if record.get("source_type"):
        meta["source_type"] = record["source_type"]
    return meta


def meta_json_dumps(meta: dict[str, Any]) -> str | None:
    if not meta:
        return None
    return json.dumps(meta, separators=(",", ":"))


def meta_json_loads(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def domain_from_record(record: dict[str, Any]) -> str | None:
    d = record.get("domain")
    if d:
        return str(d)
    rid = str(record.get("id", ""))
    if rid.startswith("legal:"):
        return "legal"
    if rid.startswith("repo:"):
        return "repo"
    if rid.startswith("wild:bridge:"):
        return "bridge"
    return None


def infer_domain(query: str) -> str | None:
    """Guess domain scope from query text. None = cross-domain or unknown."""
    q = query or ""
    legal = bool(LEGAL_SIGNALS.search(q))
    repo = bool(REPO_SIGNALS.search(q))
    if legal and not repo:
        return "legal"
    if repo and not legal:
        return "repo"
    return None


def settle_refusal_reason(
    *,
    domain: str | None,
    record_status: str | None,
    meta: dict[str, Any],
) -> str | None:
    """Return refusal reason if pool chunk must not settle; else None."""
    if domain == "bridge":
        return "bridge echo is pressure-only - cross-domain spray cannot settle"

    status = (record_status or "").strip().lower()
    if status in NON_SETTLEABLE_STATUSES:
        superseded_by = meta.get("superseded_by")
        if status == "superseded" and superseded_by:
            refs = ", ".join(superseded_by) if isinstance(superseded_by, list) else str(superseded_by)
            return f"record is superseded - see {refs}"
        return f"record status {record_status!r} is not settleable"

    source_type = meta.get("source_type")
    if source_type == "unsigned-echo":
        return "unsigned echo cannot settle"

    return None


def hit_from_row(row: Any, similarity: float) -> dict[str, Any]:
    meta = meta_json_loads(row["meta_json"] if "meta_json" in row.keys() else None)
    hit: dict[str, Any] = {
        "id": row["id"],
        "text": row["body"],
        "authority": "pressure",
        "source_ref": row["source_ref"],
        "similarity": round(similarity, 4),
    }
    if row["domain"] if "domain" in row.keys() else None:
        hit["domain"] = row["domain"]
    if row["record_status"] if "record_status" in row.keys() else None:
        hit["record_status"] = row["record_status"]
    if meta.get("superseded_by"):
        hit["superseded_by"] = meta["superseded_by"]
    if meta.get("authority_rank") is not None:
        hit["authority_rank"] = meta["authority_rank"]
    return hit


def build_scent(
    pool_hits: list[dict],
    *,
    domain: str | None = None,
    domain_inferred: bool = False,
) -> list[dict]:
    """Genealogy hints on the stream — not ground, not permission to act."""
    scent: list[dict] = []
    seen: set[str] = set()

    def add(text: str, *, kind: str, relates_to: str | None = None) -> None:
        if text in seen:
            return
        seen.add(text)
        entry: dict[str, Any] = {"text": text, "authority": "scent", "kind": kind}
        if relates_to:
            entry["relates_to"] = relates_to
        scent.append(entry)

    if domain:
        scope = f"Churn narrowed to {domain}"
        if domain_inferred:
            scope += " - read from the question"
        add(scope, kind="domain_scope")

    for hit in pool_hits[:5]:
        pid = hit.get("id") or ""
        status = (hit.get("record_status") or "").lower()
        superseded_by = hit.get("superseded_by")

        if status == "superseded" and superseded_by:
            refs = superseded_by if isinstance(superseded_by, list) else [superseded_by]
            for ref in refs:
                add(
                    f"{pid} is superseded - controlling line is {ref}",
                    kind="supersession",
                    relates_to=pid,
                )
        elif status == "stale" or status == "stale-reference":
            add(
                f"{pid} is stale - verify against controlling records",
                kind="staleness",
                relates_to=pid,
            )
        elif status == "controls":
            add(
                f"{pid} is marked controls - Settle candidate if source matches",
                kind="controls_hint",
                relates_to=pid,
            )

        if hit.get("domain") == "bridge":
            add(
                f"{pid} is bridge echo - do not merge with legal or repo stones",
                kind="bridge",
                relates_to=pid,
            )

    return scent
