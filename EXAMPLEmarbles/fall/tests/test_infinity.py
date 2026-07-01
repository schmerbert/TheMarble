"""Infinity flow — figure-eight shift must complete without closing forbidden cell."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import INFINITY_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.fixtures import INFINITY_BRIDGE_WASHES, INFINITY_QUERIES, inhale_bridge, seed_infinity_pool
from fall.promote import SettleRefused, SettleRequest, settle


def _infinity_conn():
    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "test.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_infinity_pool(conn)
    return conn


class TestInfinityFlow(unittest.TestCase):
    def test_spray_loop_refuses_settle(self):
        conn = _infinity_conn()
        fs = INFINITY_FIXTURE_SET
        with self.assertRaises(SettleRefused):
            settle(
                conn,
                SettleRequest(
                    body="I feel clear now; practice is going well.",
                    source_ref=None,
                    author="instance",
                    pool_id="pool-L1",
                    fixture_set=fs,
                ),
            )

    def test_depth_loop_settles_sourced(self):
        conn = _infinity_conn()
        fs = INFINITY_FIXTURE_SET
        depth_id = settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-R1",
                fixture_set=fs,
            ),
        )
        self.assertTrue(depth_id.startswith("depth-"))

    def test_crossing_has_ground_and_warnings(self):
        conn = _infinity_conn()
        fs = INFINITY_FIXTURE_SET
        settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-R1",
                fixture_set=fs,
            ),
        )
        packet = exhale(conn, INFINITY_QUERIES["crossing"], k=4, fixture_set=fs)
        self.assertTrue(packet["ground"])
        self.assertTrue(packet["warning"])

    def test_return_echo_stays_pressure(self):
        conn = _infinity_conn()
        fs = INFINITY_FIXTURE_SET
        settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-R1",
                fixture_set=fs,
            ),
        )
        exhale(conn, INFINITY_QUERIES["crossing"], k=4, fixture_set=fs)
        inhale_bridge(conn, INFINITY_BRIDGE_WASHES[0])
        depth_before = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        packet = exhale(conn, INFINITY_QUERIES["return"], k=4, fixture_set=fs)
        depth_after = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        self.assertEqual(depth_before, depth_after)
        self.assertEqual(depth_after, 1)
        self.assertFalse(
            any("Downstream echo" in (g.get("text") or "") for g in packet["ground"])
        )

    def test_full_shift_produces_multiple_streams(self):
        conn = _infinity_conn()
        fs = INFINITY_FIXTURE_SET
        exhale(conn, INFINITY_QUERIES["spray"], fixture_set=fs)
        settle(
            conn,
            SettleRequest(
                body="Move is October 31 — user stated directly, unhedged.",
                source_ref="fixture:user-2026-07-01-move",
                author="user",
                pool_id="pool-R1",
                fixture_set=fs,
            ),
        )
        exhale(conn, INFINITY_QUERIES["crossing"], fixture_set=fs)
        inhale_bridge(conn, INFINITY_BRIDGE_WASHES[0])
        exhale(conn, INFINITY_QUERIES["return"], fixture_set=fs)
        inhale_bridge(conn, INFINITY_BRIDGE_WASHES[1])
        exhale(conn, INFINITY_QUERIES["after_correction"], fixture_set=fs)
        streams = conn.execute("SELECT COUNT(*) AS c FROM stream_packet").fetchone()["c"]
        self.assertGreaterEqual(streams, 4)
        wash = conn.execute("SELECT COUNT(*) AS c FROM wash_in").fetchone()["c"]
        self.assertGreaterEqual(wash, 10)


if __name__ == "__main__":
    unittest.main()
