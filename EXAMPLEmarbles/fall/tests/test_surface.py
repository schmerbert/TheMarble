"""Arrival breath surfaces weighted exhale to SURFACE.md."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET
from fall.db import connect, init_db
from fall.promote import SettleRequest, settle
from fall.surface import arrival_breath, arrival_queries, render_surface_markdown, shift_snapshot
from fall.wild_loader import LEGAL_SETTLE, REPO_SETTLE, default_wild_data_root, seed_wild_dense


def _skip_data():
    root = default_wild_data_root()
    if not root.is_dir():
        raise unittest.SkipTest("TestData missing")
    return root


class TestSurface(unittest.TestCase):
    def test_arrival_queries_wild_has_two_domains(self):
        qs = arrival_queries(WILD_DENSE_FIXTURE_SET)
        self.assertEqual(len(qs), 2)
        self.assertEqual(qs[0][0], "legal")
        self.assertEqual(qs[1][0], "repo")

    def test_arrival_breath_writes_surface(self):
        data_root = _skip_data()
        tmp = tempfile.mkdtemp()
        db = Path(tmp) / "test.db"
        surface = Path(tmp) / "SURFACE.md"
        conn = connect(db)
        init_db(conn, ROOT / "schema.sql")
        seed_wild_dense(conn, data_root=data_root)
        settle(
            conn,
            SettleRequest(
                body=LEGAL_SETTLE["body"],
                source_ref=LEGAL_SETTLE["source_ref"],
                author="user",
                pool_id=LEGAL_SETTLE["pool_id"],
                fixture_set=WILD_DENSE_FIXTURE_SET,
            ),
        )
        path = arrival_breath(conn, fixture_set=WILD_DENSE_FIXTURE_SET, surface_path=surface)
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("SURFACE", text)
        self.assertIn("Stones (settled depth only)", text)
        self.assertIn("April 29", text)
        self.assertIn("Spray — legal weather", text)
        self.assertIn("Spray — repo weather", text)
        self.assertIn("[ground]", text)
        self.assertIn("Cold air", text)
        self.assertIn("Smell (scent)", text)
        snap = shift_snapshot(conn)
        self.assertEqual(snap["counts"]["pool_chunk"], 50)
        self.assertEqual(snap["counts"]["depth_entry"], 1)

    def test_render_marks_authority(self):
        md = render_surface_markdown(
            {"phase": "x", "shift_stone": "y", "fixture_set": "z", "counts": {
                "wash_in": 1, "pool_chunk": 2, "depth_entry": 0, "settle_audit": 0, "stream_packet": 0,
            }, "domains": {}, "recent_refusals": []},
            [{"query": "q", "pressure": [{"text": "p", "authority": "pressure", "domain": "legal",
              "record_status": "superseded", "similarity": 0.5}], "warning": [], "scent": [], "meta": {}}],
            ground=[],
        )
        self.assertIn("[pressure] (legal/superseded)", md)


if __name__ == "__main__":
    unittest.main()
