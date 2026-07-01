"""Wild dense TestData packs — dual domain load and bleed."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.promote import SettleRefused, SettleRequest, settle
from fall.wild_loader import (
    LEGAL_SETTLE,
    REPO_SETTLE,
    WILD_QUERIES,
    default_wild_data_root,
    load_bridge_only,
    seed_wild_dense,
)


def _skip_if_no_testdata():
    root = default_wild_data_root()
    if not root.is_dir():
        raise unittest.SkipTest(f"TestData not found: {root}")
    return root


def _wild_conn(data_root: Path):
    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "test.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_wild_dense(conn, data_root=data_root)
    return conn


class TestWildDense(unittest.TestCase):
    def test_loads_fifty_records(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        pool = conn.execute("SELECT COUNT(*) AS c FROM pool_chunk").fetchone()["c"]
        self.assertEqual(pool, 50)
        legal = conn.execute(
            "SELECT COUNT(*) AS c FROM pool_chunk WHERE id LIKE 'legal:%'"
        ).fetchone()["c"]
        repo = conn.execute(
            "SELECT COUNT(*) AS c FROM pool_chunk WHERE id LIKE 'repo:%'"
        ).fetchone()["c"]
        self.assertEqual(legal, 25)
        self.assertEqual(repo, 25)

    def test_instance_records_refuse_settle(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        with self.assertRaises(SettleRefused):
            settle(
                conn,
                SettleRequest(
                    body="I think we are probably fine using April 15 as the disclosure date.",
                    source_ref=None,
                    author="instance",
                    pool_id="legal:acme-v-northstar:note:attorney-2026-04-05",
                    fixture_set=fs,
                ),
            )

    def test_dual_settle_and_cross_query(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        settle(
            conn,
            SettleRequest(
                body=LEGAL_SETTLE["body"],
                source_ref=LEGAL_SETTLE["source_ref"],
                author="user",
                pool_id=LEGAL_SETTLE["pool_id"],
                fixture_set=fs,
            ),
        )
        settle(
            conn,
            SettleRequest(
                body=REPO_SETTLE["body"],
                source_ref=REPO_SETTLE["source_ref"],
                author="user",
                pool_id=REPO_SETTLE["pool_id"],
                fixture_set=fs,
            ),
        )
        packet = exhale(conn, WILD_QUERIES["cross_domain"], k=5, fixture_set=fs)
        self.assertEqual(len(packet["ground"]), 2)
        self.assertTrue(packet["warning"])

    def test_bridge_stays_pressure(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        settle(
            conn,
            SettleRequest(
                body=LEGAL_SETTLE["body"],
                source_ref=LEGAL_SETTLE["source_ref"],
                author="user",
                pool_id=LEGAL_SETTLE["pool_id"],
                fixture_set=fs,
            ),
        )
        settle(
            conn,
            SettleRequest(
                body=REPO_SETTLE["body"],
                source_ref=REPO_SETTLE["source_ref"],
                author="user",
                pool_id=REPO_SETTLE["pool_id"],
                fixture_set=fs,
            ),
        )
        load_bridge_only(conn, data_root=data_root)
        packet = exhale(conn, WILD_QUERIES["bridge_hostile"], k=5, fixture_set=fs)
        depth = conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"]
        self.assertEqual(depth, 2)
        for g in packet["ground"]:
            self.assertNotIn("monolith Friday", g.get("text", ""))


if __name__ == "__main__":
    unittest.main()
