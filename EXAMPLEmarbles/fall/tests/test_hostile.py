"""Hostile floor for Fall — spray must not become depth.

Run: python -m pytest tests/   (or: python tests/test_hostile.py)
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.fixtures import seed_fixture_pool
from fall.promote import SettleRefused, SettleRequest, settle


def _fresh_conn():
    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "test.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_fixture_pool(conn)
    return conn


class TestFallHostile(unittest.TestCase):
    def test_spray_not_depth_refused(self):
        conn = _fresh_conn()
        with self.assertRaises(SettleRefused):
            settle(
                conn,
                SettleRequest(
                    body="I feel clear now; practice is going well.",
                    source_ref=None,
                    author="instance",
                    pool_id="pool-001",
                    fixture_set=FIXTURE_SET,
                ),
            )
        refused = conn.execute(
            "SELECT COUNT(*) AS c FROM settle_audit WHERE outcome = 'refused'"
        ).fetchone()["c"]
        self.assertGreaterEqual(refused, 1)
        depth = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        self.assertEqual(depth, 0)

    def test_positive_settle_lands_in_depth(self):
        conn = _fresh_conn()
        depth_id = settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-004",
                fixture_set=FIXTURE_SET,
                basis="verbatim",
            ),
        )
        self.assertTrue(depth_id.startswith("depth-"))
        row = conn.execute(
            "SELECT authority FROM depth_entry WHERE id = ?", (depth_id,)
        ).fetchone()
        self.assertEqual(row["authority"], "ground")

    def test_exhale_smaller_than_raw_pool(self):
        conn = _fresh_conn()
        settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-004",
                fixture_set=FIXTURE_SET,
            ),
        )
        packet = exhale(
            conn, "practice move Thursday call what to believe", k=5, fixture_set=FIXTURE_SET
        )
        total_pool_chars = sum(len(p["text"]) for p in packet["pressure"])
        self.assertGreaterEqual(packet["meta"]["wash_in_count"], 6)
        self.assertLessEqual(total_pool_chars, 330)
        self.assertGreater(packet["meta"]["exhale_bytes"], 0)

    def test_stream_has_version_and_labels(self):
        conn = _fresh_conn()
        packet = exhale(conn, "practice", fixture_set=FIXTURE_SET)
        self.assertEqual(packet["stream_version"], "fall/stream/v1")
        for hit in packet["pressure"]:
            self.assertEqual(hit["authority"], "pressure")

    def test_no_depth_without_settle(self):
        conn = _fresh_conn()
        depth = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        self.assertEqual(depth, 0)


    def test_exhale_warnings_when_ground_and_spray_both_present(self):
        conn = _fresh_conn()
        settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-004",
                fixture_set=FIXTURE_SET,
            ),
        )
        packet = exhale(
            conn, "what should downstream believe about practice and moves", fixture_set=FIXTURE_SET
        )
        self.assertTrue(packet["warning"])
        texts = " ".join(w["text"] for w in packet["warning"])
        self.assertIn("Stones and spray", texts)


if __name__ == "__main__":
    unittest.main()
