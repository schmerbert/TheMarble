"""Live wash intake — surface and stats."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import wash_in, to_pool
from fall.db import connect, init_db
from fall.intake import live_wash_stats
from fall.surface import arrival_breath, shift_snapshot


class TestIntake(unittest.TestCase):
    def test_live_wash_stats_and_surface_section(self):
        tmp = tempfile.mkdtemp()
        db = Path(tmp) / "t.db"
        surface = Path(tmp) / "SURFACE.md"
        conn = connect(db)
        init_db(conn, ROOT / "schema.sql")
        wash_in(conn, "Client says April 15 is fine.", source_ref=None, author="instance", fixture_set=None)
        to_pool(
            conn,
            "live:legal:test-001",
            "Client says April 15 is fine.",
            source_ref=None,
            author="instance",
            fixture_set=None,
            domain="legal",
            record_status="hedged",
        )
        stats = live_wash_stats(conn)
        self.assertEqual(stats["count"], 1)
        self.assertEqual(stats["hedged"], 1)
        snap = shift_snapshot(conn)
        self.assertEqual(snap["live_wash"]["count"], 1)
        arrival_breath(conn, fixture_set=None, surface_path=surface, k=2)
        text = surface.read_text(encoding="utf-8")
        self.assertIn("Fresh wash (live", text)
        self.assertIn("Spray — live wash weather", text)
        self.assertIn("exhale", text)
        self.assertIn("--live", text)
        conn.close()


if __name__ == "__main__":
    unittest.main()
