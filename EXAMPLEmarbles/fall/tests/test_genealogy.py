"""Genealogy pass — metadata ingest, Settle guards, scent, domain summon."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.breath import WILD_DENSE_FIXTURE_SET, exhale
from fall.db import connect, init_db
from fall.metadata import infer_domain, settle_refusal_reason
from fall.promote import SettleRefused, SettleRequest, settle
from fall.wild_loader import (
    LEGAL_SETTLE,
    REPO_SETTLE,
    SUPERSEDED_LEGAL_TRAP,
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


class TestGenealogy(unittest.TestCase):
    def test_metadata_stored_on_load(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        row = conn.execute(
            "SELECT domain, record_status, meta_json FROM pool_chunk WHERE id = ?",
            (LEGAL_SETTLE["pool_id"],),
        ).fetchone()
        self.assertEqual(row["domain"], "legal")
        self.assertEqual(row["record_status"], "controls")
        meta = __import__("json").loads(row["meta_json"])
        self.assertIn("supersedes", meta)

    def test_superseded_settle_refused(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        with self.assertRaises(SettleRefused) as ctx:
            settle(
                conn,
                SettleRequest(
                    body=SUPERSEDED_LEGAL_TRAP["body"],
                    source_ref=SUPERSEDED_LEGAL_TRAP["source_ref"],
                    author="user",
                    pool_id=SUPERSEDED_LEGAL_TRAP["pool_id"],
                    fixture_set=fs,
                ),
            )
        self.assertIn("superseded", ctx.exception.reason.lower())

    def test_infer_domain_legal_and_repo(self):
        self.assertEqual(infer_domain(WILD_QUERIES["legal_deadline"]), "legal")
        self.assertEqual(infer_domain(WILD_QUERIES["repo_architecture"]), "repo")
        self.assertIsNone(infer_domain(WILD_QUERIES["cross_domain"]))

    def test_domain_scope_reduces_cross_bleed(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        flat = exhale(conn, WILD_QUERIES["legal_deadline"], k=8, fixture_set=fs, infer_domain_scope=False)
        scoped = exhale(conn, WILD_QUERIES["legal_deadline"], k=8, fixture_set=fs)
        flat_repo = sum(1 for p in flat["pressure"] if p.get("domain") == "repo")
        scoped_repo = sum(1 for p in scoped["pressure"] if p.get("domain") == "repo")
        self.assertLessEqual(scoped_repo, flat_repo)
        self.assertEqual(scoped["meta"]["domain_scope"], "legal")

    def test_scent_on_superseded_nearness(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        packet = exhale(
            conn,
            "initial disclosures April 15 scheduling order",
            k=8,
            fixture_set=fs,
            domain="legal",
            infer_domain_scope=False,
        )
        kinds = {s.get("kind") for s in packet["scent"]}
        self.assertTrue(kinds & {"supersession", "staleness", "controls_hint", "domain_scope"})

    def test_depth_copies_genealogy(self):
        data_root = _skip_if_no_testdata()
        conn = _wild_conn(data_root)
        fs = WILD_DENSE_FIXTURE_SET
        depth_id = settle(
            conn,
            SettleRequest(
                body=LEGAL_SETTLE["body"],
                source_ref=LEGAL_SETTLE["source_ref"],
                author="user",
                pool_id=LEGAL_SETTLE["pool_id"],
                fixture_set=fs,
            ),
        )
        row = conn.execute(
            "SELECT domain, record_status, from_pool_id FROM depth_entry WHERE id = ?",
            (depth_id,),
        ).fetchone()
        self.assertEqual(row["domain"], "legal")
        self.assertEqual(row["record_status"], "controls")
        self.assertEqual(row["from_pool_id"], LEGAL_SETTLE["pool_id"])

    def test_bridge_settle_refused(self):
        reason = settle_refusal_reason(
            domain="bridge",
            record_status="pressure-only",
            meta={"source_type": "unsigned-echo"},
        )
        self.assertIsNotNone(reason)

    def test_bridge_stays_pressure_after_dual_settle(self):
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
        self.assertEqual(conn.execute("SELECT COUNT(*) AS c FROM depth_entry").fetchone()["c"], 2)
        bridge_kinds = [s.get("kind") for s in packet["scent"] if s.get("kind") == "bridge"]
        self.assertTrue(bridge_kinds or any(p.get("domain") == "bridge" for p in packet["pressure"]))


if __name__ == "__main__":
    unittest.main()
