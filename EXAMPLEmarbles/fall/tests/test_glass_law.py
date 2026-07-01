"""Glass law — edges, source lock, silence, stress harness."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.edges import superseded_by_targets
from fall.promote import SettleRefused, SettleRequest, settle
from fall.stress_harness import all_passed, run_stress_harness
from fall.wild_loader import (
    LEGAL_SETTLE,
    SUPERSEDED_LEGAL_TRAP,
    default_wild_data_root,
    seed_wild_dense,
)


def _wild_conn():
    root = default_wild_data_root()
    if not root.is_dir():
        raise unittest.SkipTest("TestData missing")
    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "test.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_wild_dense(conn, data_root=root)
    return conn


class TestGlassLaw(unittest.TestCase):
    def test_edges_loaded(self):
        conn = _wild_conn()
        n = conn.execute("SELECT COUNT(*) AS c FROM pool_edge").fetchone()["c"]
        self.assertGreater(n, 10)
        targets = superseded_by_targets(
            conn, "legal:acme-v-northstar:order:scheduling-2026-03-15"
        )
        self.assertIn("legal:acme-v-northstar:order:amended-2026-04-02", targets)

    def test_source_lock_refuses_mismatch(self):
        conn = _wild_conn()
        with self.assertRaises(SettleRefused) as ctx:
            settle(
                conn,
                SettleRequest(
                    body=LEGAL_SETTLE["body"],
                    source_ref="legal:wrong-id",
                    author="user",
                    pool_id=LEGAL_SETTLE["pool_id"],
                    fixture_set=WILD_DENSE_FIXTURE_SET,
                ),
            )
        self.assertIn("source_ref must match pool_id", ctx.exception.reason)

    def test_exhale_silence_on_superseded_nearmiss(self):
        conn = _wild_conn()
        packet = exhale(
            conn,
            "initial disclosures scheduling order April",
            k=3,
            fixture_set=WILD_DENSE_FIXTURE_SET,
            domain="legal",
            infer_domain_scope=False,
        )
        self.assertTrue(packet["silence"] or packet["scent"])

    def test_ddl_rejects_depth_without_pool(self):
        conn = _wild_conn()
        with self.assertRaises(Exception):
            conn.execute(
                """
                INSERT INTO depth_entry (
                    id, settled_at, body, source_ref, author, authority, from_pool_id
                ) VALUES ('depth-bad', 'now', 'x', 'ref', 'user', 'ground', 'nonexistent-id')
                """
            )

    def test_stress_harness_all_pass(self):
        conn = _wild_conn()
        results = run_stress_harness(conn)
        if not all_passed(results):
            fails = [r for r in results if not r.passed]
            self.fail("; ".join(f"{r.name}: {r.detail}" for r in fails))


if __name__ == "__main__":
    unittest.main()
