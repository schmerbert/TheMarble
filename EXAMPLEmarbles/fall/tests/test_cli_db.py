"""CLI --db resolution for showcase commands."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.fixtures_wild import ensure_wild_demo_db


class TestCliDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_wild_demo_db()

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        cmd = [sys.executable, "-m", "fall.cli", *args]
        return subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_status_after_subcommand_with_wild_db(self):
        r = self._run("status", "--db", "fixtures/fall_wild.db")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("db:", r.stdout)
        self.assertIn("pool_chunk", r.stdout)

    def test_exhale_wild_without_db_uses_showcase_db(self):
        r = self._run(
            "exhale",
            "Are we safe to ship the monolith Friday because the legal deadline is handled?",
            "--wild",
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"fixture_set": "wild_dense_v1"', r.stdout)
        self.assertIn('"pressure"', r.stdout)
        self.assertIn("bridge", r.stdout.lower())

    def test_exhale_wild_db_before_subcommand_still_works(self):
        r = self._run(
            "--db",
            "fixtures/fall_wild.db",
            "exhale",
            "test",
            "--wild",
        )
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_status_db_before_subcommand_uses_wild_db(self):
        r = self._run("--db", "fixtures/fall_wild.db", "status")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("fall_wild.db", r.stdout.replace("\\", "/"))
        self.assertNotIn("fall.db", r.stdout.replace("\\", "/").split("db:")[1].splitlines()[0])


if __name__ == "__main__":
    unittest.main()
