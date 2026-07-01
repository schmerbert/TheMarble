"""Hybrid summon — receipt slots on --live exhale."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import FIXTURE_SET, exhale, to_pool, wash_in
from fall.db import connect, init_db
from fall.fixtures import seed_fixture_pool
from fall.intake import live_receipt_slot_count


def _fresh_conn():
    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "test.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_fixture_pool(conn)
    return conn


class TestHybridSummon(unittest.TestCase):
    def test_live_exhale_reserves_receipt_for_fresh_wash(self):
        conn = _fresh_conn()
        wash_in(conn, "Pack noise about court dates.", source_ref="pack:1", author="user")
        to_pool(
            conn,
            "pack:court",
            "Pack noise about court dates.",
            source_ref="pack:1",
            author="user",
            fixture_set=FIXTURE_SET,
            domain="legal",
        )
        wash_in(conn, "Just imported: Friday deploy ticket.", source_ref=None, author="user")
        to_pool(
            conn,
            "live:repo:import-fresh",
            "Just imported: Friday deploy ticket.",
            source_ref=None,
            author="user",
            fixture_set=None,
            domain="repo",
            record_status="pressure-only",
        )
        conn.commit()

        self.assertEqual(live_receipt_slot_count(conn), 1)

        packet = exhale(conn, "what changed on this shift", fixture_set=None, k=3)
        ids = [p["id"] for p in packet["pressure"]]
        self.assertIn("live:repo:import-fresh", ids)
        self.assertTrue(packet["meta"]["hybrid_summon"])
        self.assertGreaterEqual(packet["meta"]["receipt_slots"], 1)
        receipt = [p for p in packet["pressure"] if p.get("summon_kind") == "receipt"]
        self.assertTrue(receipt)
        self.assertEqual(receipt[0]["id"], "live:repo:import-fresh")
        warning_text = " ".join(w["text"] for w in packet["warning"])
        self.assertIn("Receipt slot", warning_text)

    def test_wild_exhale_has_no_receipt_slots(self):
        conn = _fresh_conn()
        wash_in(conn, "Live only.", source_ref=None, author="user")
        to_pool(
            conn,
            "live:only",
            "Live only.",
            source_ref=None,
            author="user",
            fixture_set=None,
            domain="repo",
        )
        conn.commit()

        packet = exhale(conn, "anything", fixture_set=FIXTURE_SET, k=3)
        self.assertFalse(packet["meta"]["hybrid_summon"])
        self.assertEqual(packet["meta"]["receipt_slots"], 0)


if __name__ == "__main__":
    unittest.main()
