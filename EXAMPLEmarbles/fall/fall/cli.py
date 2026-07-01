"""Terminal front door for ongoing shifts (does not wipe the db like dry_run)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fall.breath import FIXTURE_SET, INFINITY_FIXTURE_SET, WILD_DENSE_FIXTURE_SET, exhale, to_pool, wash_in
from fall.db import connect, init_db, migrate_schema
from fall.fixtures import seed_fixture_pool, seed_infinity_pool
from fall.surface import arrival_breath, detect_fixture_set
from fall.surface_state import surface_stale_banner
from fall.intake import cli_inhale_ack, intake_posture_lines, live_wash_stats
from fall.console import configure_stdio
from fall.promote import SettleRefused, SettleRequest, settle

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "fixtures" / "fall.db"
WILD_DB = ROOT / "fixtures" / "fall_wild.db"
INFINITY_DB = ROOT / "fixtures" / "fall_infinity.db"


def _resolve_db(args: argparse.Namespace) -> Path:
    """--wild/--infinity imply the showcase db unless --db was explicitly chosen."""
    db = Path(args.db)
    if getattr(args, "wild", False) and db == DEFAULT_DB:
        return WILD_DB
    if getattr(args, "infinity", False) and db == DEFAULT_DB:
        return INFINITY_DB
    return db


def _bind_db(args: argparse.Namespace) -> None:
    args.db = _resolve_db(args)


def _conn(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    new = not db_path.exists()
    conn = connect(db_path)
    if new:
        init_db(conn, ROOT / "schema.sql")
    else:
        try:
            conn.execute("SELECT 1 FROM handoff LIMIT 1").fetchone()
        except Exception:
            init_db(conn, ROOT / "schema.sql")
        else:
            migrate_schema(conn)
    return conn


def cmd_init(args: argparse.Namespace) -> int:
    db = args.db
    if args.reset and db.exists():
        db.unlink()
    conn = connect(db)
    init_db(conn, ROOT / "schema.sql")
    conn.commit()
    conn.close()
    print(f"initialized {db}")
    return 0


def cmd_seed(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    n = conn.execute("SELECT COUNT(*) AS c FROM pool_chunk").fetchone()["c"]
    if n and not args.force:
        print(f"pool already has {n} chunks; use --force to re-seed")
        return 0
    if args.force:
        for table in (
            "stream_packet",
            "settle_audit",
            "depth_entry",
            "pool_edge",
            "pool_chunk",
            "wash_in",
        ):
            conn.execute(f"DELETE FROM {table}")
    if args.infinity:
        seed_infinity_pool(conn)
        label = INFINITY_FIXTURE_SET
    elif args.wild:
        counts = seed_wild_dense(conn, data_root=args.wild_data, include_bridge=args.bridge)
        label = f"{WILD_DENSE_FIXTURE_SET} (legal={counts['legal']} repo={counts['repo']})"
    else:
        seed_fixture_pool(conn)
        label = FIXTURE_SET
    conn.commit()
    conn.close()
    print(f"fixture pool seeded ({label})")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    row = conn.execute("SELECT phase, shift_stone FROM handoff WHERE id = 1").fetchone()
    counts = {
        t: conn.execute(f"SELECT COUNT(*) AS c FROM {t}").fetchone()["c"]
        for t in ("wash_in", "pool_chunk", "depth_entry", "settle_audit", "stream_packet")
    }
    stale = surface_stale_banner(conn)
    live = live_wash_stats(conn)
    conn.close()
    print(f"phase: {row['phase'] if row else '?'}")
    print(f"shift_stone: {row['shift_stone'] if row else '?'}")
    print(f"db: {args.db}")
    if stale:
        print(f"WARNING: {stale}")
    if live["count"]:
        print(f"  live_wash: {live['count']} chunk(s) in churn")
        for line in intake_posture_lines(live):
            print(f"  {line}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


def cmd_inhale(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    fixture = None if args.live else FIXTURE_SET
    wash_in(conn, args.text, source_ref=args.source, author=args.author, fixture_set=fixture)
    chunk_id = args.id or f"pool-live-{conn.execute('SELECT COUNT(*) AS c FROM pool_chunk').fetchone()['c'] + 1}"
    to_pool(conn, chunk_id, args.text, source_ref=args.source, author=args.author, fixture_set=fixture)
    stats = live_wash_stats(conn) if args.live else None
    conn.commit()
    conn.close()
    msg = cli_inhale_ack(live=args.live, stats=stats)
    print(f"{msg} (pool {chunk_id})")
    return 0


def cmd_settle(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    try:
        depth_id = settle(
            conn,
            SettleRequest(
                body=args.text,
                source_ref=args.source,
                author=args.author,
                pool_id=args.pool_id,
                fixture_set=None if args.live else FIXTURE_SET,
                basis=args.basis,
            ),
        )
    except SettleRefused as e:
        conn.commit()
        conn.close()
        print(f"refused: {e.reason}", file=sys.stderr)
        return 1
    conn.commit()
    conn.close()
    print(f"settled -> {depth_id}")
    return 0


def cmd_arrive(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    fs = args.fixture_set
    if fs is None and args.wild:
        fs = WILD_DENSE_FIXTURE_SET
    elif fs is None and args.infinity:
        fs = INFINITY_FIXTURE_SET
    elif fs is None:
        fs = detect_fixture_set(conn)
    path = arrival_breath(
        conn,
        fixture_set=fs,
        k=args.k,
        surface_path=args.surface,
    )
    conn.commit()
    conn.close()
    print(f"arrival breath -> {path}")
    return 0


def cmd_exhale(args: argparse.Namespace) -> int:
    conn = _conn(args.db)
    fixture = None if args.live else (WILD_DENSE_FIXTURE_SET if args.wild else FIXTURE_SET)
    if args.fixture_set:
        fixture = args.fixture_set
    packet = exhale(
        conn,
        args.query,
        k=args.k,
        fixture_set=fixture,
        domain=args.domain,
        infer_domain_scope=not args.no_infer_domain,
    )
    conn.commit()
    conn.close()
    print(json.dumps(packet, indent=2))
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Accept --db before or after the subcommand without duplicate-arg override."""
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--db", type=Path, default=None)
    pre_args, remaining = pre.parse_known_args(argv)

    parser = argparse.ArgumentParser(description="Fall shift CLI")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", parents=[common], help="create or reset database")
    p_init.add_argument("--reset", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_seed = sub.add_parser("seed", parents=[common], help="load fixture pool")
    p_seed.add_argument("--force", action="store_true")
    p_seed.add_argument(
        "--infinity",
        action="store_true",
        help=f"load {INFINITY_FIXTURE_SET} braid instead of {FIXTURE_SET}",
    )
    p_seed.add_argument(
        "--wild",
        action="store_true",
        help=f"load legal+repo packs as {WILD_DENSE_FIXTURE_SET}",
    )
    p_seed.add_argument(
        "--wild-data",
        type=Path,
        default=None,
        help="override path to wild_dense_test_packs folder",
    )
    p_seed.add_argument(
        "--bridge",
        action="store_true",
        help="include optional bridge pressure records (with --wild)",
    )
    p_seed.set_defaults(func=cmd_seed)

    p_status = sub.add_parser("status", parents=[common], help="show counts")
    p_status.set_defaults(func=cmd_status)

    p_inhale = sub.add_parser("inhale", parents=[common], help="wash in + pool")
    p_inhale.add_argument("text")
    p_inhale.add_argument("--source", default=None)
    p_inhale.add_argument("--author", default="instance", choices=("user", "instance"))
    p_inhale.add_argument("--id", default=None)
    p_inhale.add_argument("--live", action="store_true", help="omit fixture_set tag")
    p_inhale.set_defaults(func=cmd_inhale)

    p_settle = sub.add_parser("settle", parents=[common], help="pool -> depth crossing")
    p_settle.add_argument("text")
    p_settle.add_argument("--source", required=True)
    p_settle.add_argument("--author", default="user", choices=("user", "instance"))
    p_settle.add_argument("--pool-id", default=None)
    p_settle.add_argument("--basis", default="user_confirmation")
    p_settle.add_argument("--live", action="store_true")
    p_settle.set_defaults(func=cmd_settle)

    p_exhale = sub.add_parser("exhale", parents=[common], help="summon + stream packet")
    p_exhale.add_argument("query")
    p_exhale.add_argument("-k", type=int, default=3)
    p_exhale.add_argument("--live", action="store_true")
    p_exhale.add_argument("--domain", choices=("legal", "repo", "bridge"), default=None)
    p_exhale.add_argument(
        "--no-infer-domain",
        action="store_true",
        help="do not auto-scope summon from query keywords",
    )
    p_exhale.add_argument("--wild", action="store_true", help="use wild_dense_v1 fixture_set")
    p_exhale.add_argument("--fixture-set", default=None)
    p_exhale.set_defaults(func=cmd_exhale)

    p_arrive = sub.add_parser(
        "arrive",
        aliases=["breath"],
        parents=[common],
        help="orientation exhale(s) -> SURFACE.md for this shift",
    )
    p_arrive.add_argument("-k", type=int, default=4)
    p_arrive.add_argument("--wild", action="store_true")
    p_arrive.add_argument("--infinity", action="store_true")
    p_arrive.add_argument("--fixture-set", default=None)
    p_arrive.add_argument(
        "--surface",
        type=Path,
        default=ROOT / "SURFACE.md",
        help="where to write arrival breath (default: SURFACE.md)",
    )
    p_arrive.set_defaults(func=cmd_arrive)

    args = parser.parse_args(remaining)
    if pre_args.db is not None:
        args.db = pre_args.db
    return args


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = _parse_args(argv)
    _bind_db(args)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
