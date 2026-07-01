"""Console-safe output on Windows and narrow terminals."""

from __future__ import annotations

import sys


def configure_stdio() -> None:
    """Prefer UTF-8 on Windows so law text and JSON do not mangle on cp1252."""
    if sys.platform != "win32":
        return
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass
