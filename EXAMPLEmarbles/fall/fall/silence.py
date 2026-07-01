"""Silence on exhale — known material withheld from pressure."""

from __future__ import annotations

from typing import Any

WITHHELD_STATUSES = frozenset(
    {
        "superseded",
        "stale",
        "stale-reference",
        "pressure-only",
    }
)


def build_exhale_silence(
    candidate_hits: list[dict],
    pressure_hits: list[dict],
    *,
    min_similarity: float = 0.18,
) -> list[dict]:
    """
    Record near-miss pool hits omitted from pressure — especially superseded/stale traps.
    Silence is not ground; it documents what the glass held back.
    """
    pressure_ids = {p.get("id") for p in pressure_hits}
    silence: list[dict] = []
    seen: set[str] = set()

    for hit in candidate_hits:
        pid = hit.get("id")
        if not pid or pid in pressure_ids:
            continue
        status = (hit.get("record_status") or "").lower()
        sim = float(hit.get("similarity") or 0)
        if status not in WITHHELD_STATUSES or sim < min_similarity:
            continue
        key = f"{pid}:{status}"
        if key in seen:
            continue
        seen.add(key)
        text = (
            f"Almost rose: {pid} ({hit.get('record_status')}) - glass held it back"
        )
        superseded_by = hit.get("superseded_by")
        if superseded_by:
            refs = superseded_by if isinstance(superseded_by, list) else [superseded_by]
            text += f"; controlling line is {', '.join(refs)}"
        entry: dict[str, Any] = {
            "text": text,
            "authority": "silence",
            "kind": "withheld_genealogy",
            "relates_to": pid,
        }
        silence.append(entry)

    return silence
