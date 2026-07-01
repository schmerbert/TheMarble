"""Exhale warnings — productive friction on the stream."""

from __future__ import annotations

HEDGED_MARKERS = (
    "didn't we",
    "didnt we",
    "probably",
    "i feel",
    "might ",
    "maybe ",
    "somewhere in there",
)


def build_exhale_warnings(pool_hits: list[dict], ground: list[dict]) -> list[dict]:
    warnings: list[dict] = []
    seen: set[str] = set()

    def add(text: str) -> None:
        if text not in seen:
            seen.add(text)
            warnings.append({"text": text, "authority": "warning"})

    if not pool_hits:
        return warnings

    top = pool_hits[0]
    sim = float(top.get("similarity") or 0)
    if not top.get("source_ref") and sim >= 0.15:
        add("Loudest spray has no source - nearness is not Settle")

    for hit in pool_hits[:3]:
        lower = (hit.get("text") or "").lower()
        if any(marker in lower for marker in HEDGED_MARKERS):
            add("Hedged words in the spray - feel them, do not Settle them")
            break

    top_status = (top.get("record_status") or "").lower()
    if top_status in ("superseded", "stale", "stale-reference"):
        add(
            f"Loudest spray is {top.get('record_status')} - nearness does not bypass lineage"
        )

    if top.get("domain") == "bridge":
        add("Bridge spray in the mix - do not merge across domains")

    if ground and pool_hits:
        add("Stones and spray both rose - depth must not bless the churn")

    if any(h.get("summon_kind") == "receipt" for h in pool_hits):
        add("Receipt slot: recent live wash - recency is not rank and not Settle")

    if pool_hits and not ground and sim >= 0.35:
        add("Strong spray, no settled stone for this question yet")

    return warnings
