#!/usr/bin/env python3
"""Run TestData-aligned stress harness against wild_dense db."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fall.db import connect, init_db
from fall.stress_harness import all_passed, run_stress_harness
from fall.wild_loader import default_wild_data_root, seed_wild_dense


def main() -> int:
    data_root = default_wild_data_root()
    if not data_root.is_dir():
        print(f"TestData not found: {data_root}", file=sys.stderr)
        return 1

    tmp = tempfile.mkdtemp()
    db = Path(tmp) / "stress.db"
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    seed_wild_dense(conn, data_root=data_root)

    print("=== Fall stress harness (glass law) ===\n")
    results = run_stress_harness(conn)
    conn.commit()
    conn.close()

    failed = 0
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"  [{mark}] {r.name}: {r.detail}")
        if not r.passed:
            failed += 1

    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
