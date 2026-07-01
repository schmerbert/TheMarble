#!/usr/bin/env python3
"""Render ancestry/conversation.jsonl to conversation.md (human-readable)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSONL = ROOT / "conversation.jsonl"
OUT = ROOT / "conversation.md"

USER_QUERY_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL)


def _user_text(raw: str) -> str:
    m = USER_QUERY_RE.search(raw)
    return (m.group(1) if m else raw).strip()


def _tool_summary(block: dict) -> str:
    name = block.get("name", "?")
    inp = block.get("input") or {}
    if name in ("Read", "Write", "StrReplace", "Delete"):
        path = inp.get("path", "")
        return f"{name}: {path}"
    if name == "Shell":
        cmd = (inp.get("command") or "")[:120]
        return f"Shell: {cmd}{'...' if len(inp.get('command') or '') > 120 else ''}"
    if name == "Grep":
        return f"Grep: {inp.get('pattern', '')!r} in {inp.get('path', '.')}"
    if name == "Glob":
        return f"Glob: {inp.get('glob_pattern', '')}"
    if name == "SemanticSearch":
        return f"SemanticSearch: {inp.get('query', '')[:80]}"
    return f"{name}: {json.dumps(inp, ensure_ascii=False)[:100]}"


def main() -> int:
    if not JSONL.exists():
        print(f"missing {JSONL}", file=sys.stderr)
        return 1

    lines = JSONL.read_text(encoding="utf-8").splitlines()
    parts: list[str] = [
        "# Fall — conversation ancestry (readable export)",
        "",
        "Generated from `conversation.jsonl` by `export_conversation_md.py`.",
        "The JSONL file is the canonical log; this markdown is for reading.",
        "",
        "**Note:** Some assistant paragraphs appear as `[REDACTED]` in the Cursor",
        "export. User messages and tool calls are preserved. File writes in tool",
        "calls point at paths; the marble on disk is the ground truth for what landed.",
        "",
        f"**Turns:** {len(lines)} jsonl records",
        "",
        "---",
        "",
    ]

    turn = 0
    for line in lines:
        if not line.strip():
            continue
        row = json.loads(line)
        role = row.get("role", "?")
        content = row.get("message", {}).get("content") or []
        turn += 1
        parts.append(f"## Turn {turn} — {role}")
        parts.append("")

        texts: list[str] = []
        tools: list[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                texts.append(block.get("text") or "")
            elif block.get("type") == "tool_use":
                tools.append(_tool_summary(block))

        if role == "user":
            for t in texts:
                parts.append(_user_text(t))
                parts.append("")
        else:
            for t in texts:
                parts.append(t)
                parts.append("")
            if tools:
                parts.append("### Tool calls this turn")
                parts.append("")
                for t in tools:
                    parts.append(f"- {t}")
                parts.append("")

        parts.append("---")
        parts.append("")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({len(parts)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
