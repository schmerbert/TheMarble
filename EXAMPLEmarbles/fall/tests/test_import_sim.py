"""import_sim.py --check end-to-end demo."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall.fixtures_wild import ensure_wild_demo_db


class TestImportSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_wild_demo_db()

    def test_check_runs_clean(self):
        r = subprocess.run(
            [sys.executable, "import_sim.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(r.returncode, 0, r.stderr or r.stdout)
        self.assertIn("imported: legal=5 repo=5", r.stdout)
        self.assertIn("OK: fresh wash surfaced", r.stdout)
        self.assertNotIn("Traceback", r.stdout)
        self.assertNotIn("Traceback", r.stderr)
        # No mojibake from cp1252 fallback on law strings
        self.assertIn("Hedged words in the spray - feel them", r.stdout)


if __name__ == "__main__":
    unittest.main()
