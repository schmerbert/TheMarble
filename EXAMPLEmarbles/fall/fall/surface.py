"""Arrival breath — weighted surfacing for the cold instance."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fall.breath import (
    FIXTURE_SET,
    INFINITY_FIXTURE_SET,
    WILD_DENSE_FIXTURE_SET,
    exhale,
    load_depth,
)
from fall.intake import live_wash_stats, recent_live_chunks
from fall.surface_state import clear_surface_fresh


ROOT = Path(__file__).resolve().parents[1]


def detect_fixture_set(conn: sqlite3.Connection) -> str | None:
    row = conn.execute(
        """
        SELECT fixture_set, COUNT(*) AS c
        FROM pool_chunk
        WHERE fixture_set IS NOT NULL
        GROUP BY fixture_set
        ORDER BY c DESC
        LIMIT 1
        """
    ).fetchone()
    return row["fixture_set"] if row else None


def shift_snapshot(conn: sqlite3.Connection) -> dict[str, Any]:
    handoff = conn.execute(
        "SELECT phase, shift_stone FROM handoff WHERE id = 1"
    ).fetchone()
    counts = {
        t: conn.execute(f"SELECT COUNT(*) AS c FROM {t}").fetchone()["c"]
        for t in ("wash_in", "pool_chunk", "depth_entry", "settle_audit", "stream_packet")
    }
    refused = conn.execute(
        """
        SELECT reason FROM settle_audit
        WHERE outcome = 'refused'
        ORDER BY attempted_at DESC
        LIMIT 3
        """
    ).fetchall()
    domains = conn.execute(
        """
        SELECT domain, COUNT(*) AS c
        FROM pool_chunk
        WHERE domain IS NOT NULL
        GROUP BY domain
        """
    ).fetchall()
    fixture_set = detect_fixture_set(conn)
    live_wash = live_wash_stats(conn)
    return {
        "phase": handoff["phase"] if handoff else None,
        "shift_stone": handoff["shift_stone"] if handoff else None,
        "fixture_set": fixture_set,
        "live_wash": live_wash,
        "counts": counts,
        "domains": {r["domain"]: r["c"] for r in domains},
        "recent_refusals": [r["reason"] for r in refused],
    }


def arrival_queries(fixture_set: str | None) -> list[tuple[str | None, str]]:
    """Domain-scoped orientation exhales — compress for movement, not flood."""
    if fixture_set == WILD_DENSE_FIXTURE_SET:
        return [
            (
                "legal",
                "Which controlling legal deadlines and orders matter on this shift?",
            ),
            (
                "repo",
                "What production architecture is currently true for Fake API?",
            ),
        ]
    if fixture_set == INFINITY_FIXTURE_SET:
        return [
            (
                None,
                "What should downstream believe about practice and the move on this shift?",
            ),
        ]
    return [(None, "What is live on this shift — spray versus settled depth?")]


def _line_authority(item: dict, default: str = "pressure") -> str:
    auth = item.get("authority", default)
    dom = item.get("domain")
    st = item.get("record_status")
    tags = [t for t in (dom, st) if t]
    suffix = f" ({'/'.join(tags)})" if tags else ""
    return f"[{auth}]{suffix}"


def _ghost_line(reason: str) -> str:
    """SURFACE-facing refusal — same audit string in the store, gentler on the rock."""
    if reason == "spray mistaken for depth - source_ref required":
        return "no source — spray cannot Settle"
    if reason.startswith("record is superseded - see "):
        ref = reason.split("see ", 1)[1]
        return f"superseded — controlling line is {ref}"
    if reason == "source_ref must match pool_id for pack records":
        return "source does not match the line — glass refused"
    if reason == "bridge echo is pressure-only - cross-domain spray cannot settle":
        return "bridge echo — cross-domain spray cannot Settle"
    return reason


def _render_items(items: list[dict], *, empty: str, for_surface: bool = True) -> list[str]:
    if not items:
        return [empty]
    lines: list[str] = []
    for item in items:
        text = (item.get("text") or "").strip()
        if not text:
            continue
        prefix = _line_authority(item, item.get("authority", "pressure"))
        ref = item.get("source_ref")
        ref_bit = f" · {ref}" if ref and for_surface else (f" ref={ref}" if ref else "")
        lines.append(f"- {prefix}{ref_bit}: {text}")
    return lines or [empty]


def render_surface_markdown(
    snapshot: dict[str, Any],
    breaths: list[dict[str, Any]],
    *,
    ground: list[dict],
    frozen_at: str | None = None,
) -> str:
    now = frozen_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    counts = snapshot["counts"]
    stone = snapshot.get("shift_stone") or "on the rock"
    lines = [
        "# SURFACE — mist at arrival",
        "",
        f"Frozen: {now}",
        "",
        "Sit on the rock. Read **HANDOFF** first. This is what landed when the fall breathed out — not ground by inheritance.",
        "",
        "Labels are law. Warnings and scent are first-class. Do not strip them.",
        "**Read the landing, not the churn.** Eyes open tempts rank; eyes closed learns weather.",
        "",
        "## Rock at arrival",
        "",
        f"- shift stone: {stone}",
        f"- washed in: {counts['wash_in']} · churn: {counts['pool_chunk']} · "
        f"stones: {counts['depth_entry']} · exhales recorded: {counts['stream_packet']}",
    ]
    if snapshot.get("domains"):
        dom = ", ".join(f"{k}={v}" for k, v in snapshot["domains"].items())
        lines.append(f"- domains in churn: {dom}")
    if snapshot.get("recent_refusals"):
        lines.append("- ghosts nearby (Settle refused):")
        for r in snapshot["recent_refusals"]:
            lines.append(f"  - {_ghost_line(r)}")
    live = snapshot.get("live_wash") or {}
    if live.get("count"):
        lines.extend(
            [
                "",
                "## Fresh wash (live — in churn, not ground)",
                "",
                f"- **{live['count']}** live chunk(s) — pack mist below does not include these",
                "- summon with: `python -m fall.cli exhale \"your query\" --live --db fixtures/fall_wild.db`",
                "- `--wild` scopes rehearsal pack only",
                "- **rank != receipt** — new imports may not top every query",
            ]
        )
        if live.get("unsigned"):
            lines.append(f"- {live['unsigned']} unsigned in live wash")
        if live.get("hedged"):
            lines.append(f"- {live['hedged']} hedged in live wash")
        recent = snapshot.get("recent_live") or []
        if recent:
            lines.append("")
            lines.append("### Last live arrivals (pressure only)")
            lines.append("")
            lines.extend(
                _render_items(recent, empty="_none_", for_surface=True)
            )
    lines.extend(["", "## Stones (settled depth only)", ""])
    lines.extend(
        _render_items(ground, empty="_No stones yet — churn only until Settle._")
    )

    for packet in breaths:
        q = packet.get("query", "")
        scope = (packet.get("meta") or {}).get("domain_scope")
        if scope:
            title = f"Spray — {scope} weather"
        elif packet.get("_breath_domain") == "live":
            title = "Spray — live wash weather"
        else:
            title = "Spray — open weather"
        lines.extend(["", f"## {title}", "", f"Orientation: {q}", ""])
        lines.extend(["### What rose (pressure)", ""])
        lines.extend(_render_items(packet.get("pressure") or [], empty="_none_"))
        lines.extend(["", "### Cold air (warnings)", ""])
        lines.extend(_render_items(packet.get("warning") or [], empty="_none_"))
        lines.extend(["", "### Smell (scent)", ""])
        lines.extend(_render_items(packet.get("scent") or [], empty="_none_"))
        lines.extend(["", "### Held back (silence)", ""])
        lines.extend(_render_items(packet.get("silence") or [], empty="_none_"))

    live = snapshot.get("live_wash") or {}
    if live.get("count"):
        next_moves = [
            "- **Live wash in churn:** `python -m fall.cli exhale \"your query\" --live --db fixtures/fall_wild.db`",
            "- Pack-scoped only: add `--wild` (omits live wash)",
            "- Settle a sourced fact: see `BREATH.md`",
            "- End shift: rewrite `HANDOFF.md`, then `python -m fall.cli arrive --wild --db fixtures/fall_wild.db`",
        ]
    else:
        next_moves = [
            "- Question the churn: `python -m fall.cli exhale \"your query\" --wild --db fixtures/fall_wild.db`",
            "- Settle a sourced fact: `python -m fall.cli settle` (see `BREATH.md`)",
            "- End shift: rewrite `HANDOFF.md`, run `python -m fall.cli arrive --wild --db fixtures/fall_wild.db`",
        ]
    lines.extend(
        [
            "",
            "## Smallest next moves",
            "",
            *next_moves,
            "",
        ]
    )
    return "\n".join(lines)


def arrival_breath(
    conn: sqlite3.Connection,
    *,
    fixture_set: str | None = None,
    k: int = 4,
    surface_path: Path | None = None,
) -> Path:
    """
    Orientation exhale(s) + weighted SURFACE.md for arrival.
    This is the marble breathing out what the shift needs to see — not ambient flood.
    """
    fs = fixture_set or detect_fixture_set(conn)
    snapshot = shift_snapshot(conn)
    if snapshot["live_wash"].get("count"):
        snapshot["recent_live"] = recent_live_chunks(conn)
        ground = load_depth(conn, fixture_set=None)
    else:
        snapshot["recent_live"] = []
        ground = load_depth(conn, fixture_set=fs)
    breaths: list[dict[str, Any]] = []

    for domain, query in arrival_queries(fs):
        packet = exhale(
            conn,
            query,
            k=k,
            fixture_set=fs,
            domain=domain,
            infer_domain_scope=domain is None,
        )
        packet["_breath_domain"] = domain
        breaths.append(packet)

    if snapshot["live_wash"].get("count"):
        live_packet = exhale(
            conn,
            "What fresh live wash is tempting — unsigned, hedged, or cross-domain?",
            k=k,
            fixture_set=None,
            infer_domain_scope=False,
        )
        live_packet["_breath_domain"] = "live"
        breaths.append(live_packet)

    if surface_path is None:
        surface_path = ROOT / "SURFACE.md"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = render_surface_markdown(snapshot, breaths, ground=ground, frozen_at=now)
    surface_path.write_text(text, encoding="utf-8")
    clear_surface_fresh(conn, now)
    return surface_path
