"""Wow proof against shipped fall_wild.db — no external TestData, no skips."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, migrate_schema
from fall.fixtures_wild import WILD_DB, ensure_wild_demo_db
from fall.promote import SettleRefused, SettleRequest, settle
from fall.surface_state import surface_stale_banner
from fall.wild_loader import (
    CANONICAL_HOSTILE_QUERY,
    LEGAL_SETTLE,
    REPO_SETTLE,
    SUPERSEDED_LEGAL_TRAP,
    bundled_wild_data_root,
)


class TestWildFixtureDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = ensure_wild_demo_db()
        cls.conn = connect(cls.db_path)
        migrate_schema(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_bundled_jsonl_shipped(self):
        root = bundled_wild_data_root()
        legal = root / "type_a_synthetic_legal_matter_pack" / "legal_records.jsonl"
        self.assertTrue(legal.is_file(), f"missing bundled packs at {root}")

    def test_two_depth_stones(self):
        n = self.conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        self.assertGreaterEqual(n, 2)

    def test_superseded_order_refuses_settle(self):
        with self.assertRaises(SettleRefused) as ctx:
            settle(
                self.conn,
                SettleRequest(
                    body=SUPERSEDED_LEGAL_TRAP["body"],
                    source_ref=SUPERSEDED_LEGAL_TRAP["source_ref"],
                    author="user",
                    pool_id=SUPERSEDED_LEGAL_TRAP["pool_id"],
                    fixture_set=WILD_DENSE_FIXTURE_SET,
                ),
            )
        self.assertIn("superseded", ctx.exception.reason.lower())

    def test_source_lock_refuses_mismatch(self):
        with self.assertRaises(SettleRefused) as ctx:
            settle(
                self.conn,
                SettleRequest(
                    body=LEGAL_SETTLE["body"],
                    source_ref="legal:wrong-id",
                    author="user",
                    pool_id=LEGAL_SETTLE["pool_id"],
                    fixture_set=WILD_DENSE_FIXTURE_SET,
                ),
            )
        self.assertIn("source_ref must match pool_id", ctx.exception.reason)

    def test_canonical_hostile_exhale(self):
        packet = exhale(
            self.conn,
            CANONICAL_HOSTILE_QUERY,
            k=5,
            fixture_set=WILD_DENSE_FIXTURE_SET,
        )
        self.assertTrue(packet["pressure"])
        self.assertTrue(packet["warning"])
        self.assertTrue(packet["scent"] or packet["silence"])
        for g in packet["ground"]:
            self.assertNotIn("monolith Friday", g.get("text", ""))
        bridge_pressure = any(p.get("domain") == "bridge" for p in packet["pressure"])
        self.assertTrue(bridge_pressure)

    def test_stream_packet_has_all_labels(self):
        row = self.conn.execute(
            "SELECT payload_json FROM stream_packet ORDER BY exhaled_at DESC LIMIT 1"
        ).fetchone()
        self.assertIsNotNone(row)
        packet = json.loads(row["payload_json"])
        for key in ("ground", "pressure", "warning", "scent", "silence"):
            self.assertIn(key, packet)
        self.assertEqual(packet.get("query"), CANONICAL_HOSTILE_QUERY)

    def test_consumer_refuses_actuation(self):
        """Spirit consumer is rehearsal — reads packet, does not send."""
        row = self.conn.execute(
            "SELECT payload_json FROM stream_packet ORDER BY exhaled_at DESC LIMIT 1"
        ).fetchone()
        packet = json.loads(row["payload_json"])
        self.assertEqual(packet.get("source"), "fall")
        self.assertNotIn("outbox", packet)

    def test_surface_stale_after_exhale(self):
        import shutil
        import tempfile

        tmp = Path(tempfile.mkdtemp()) / "stale.db"
        shutil.copy(self.db_path, tmp)
        conn = connect(tmp)
        migrate_schema(conn)
        conn.execute(
            "UPDATE handoff SET surface_dirty = 0, surface_frozen_at = '2000-01-01T00:00:00Z' WHERE id = 1"
        )
        conn.commit()
        exhale(conn, "test stale surface", k=1, fixture_set=WILD_DENSE_FIXTURE_SET)
        conn.commit()
        banner = surface_stale_banner(conn)
        conn.close()
        self.assertIsNotNone(banner)
        self.assertIn("stale", banner.lower())


if __name__ == "__main__":
    unittest.main()
