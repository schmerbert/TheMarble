-- Fall schema — law in DDL where possible.
-- Settle gate: fall/promote.py + pool genealogy (domain, record_status, meta_json).

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS handoff (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  phase TEXT NOT NULL,
  shift_stone TEXT,
  surface_frozen_at TEXT,
  surface_dirty INTEGER NOT NULL DEFAULT 0,
  decided TEXT,
  open_items TEXT,
  untrusted TEXT,
  next_action TEXT,
  updated_at TEXT NOT NULL
);

INSERT OR IGNORE INTO handoff (id, phase, shift_stone, decided, open_items, untrusted, next_action, updated_at)
VALUES (
  1,
  'spirit_v3',
  'on rock, glass law',
  'pool_edge, source lock, silence on exhale, stress harness',
  'embed still demo; surface freshness open',
  'deterministic embed; run stress_harness',
  'python wild_run.py',
  '2026-07-01'
);

-- Append-only arrivals (inhale)
CREATE TABLE IF NOT EXISTS wash_in (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  washed_at TEXT NOT NULL,
  body TEXT NOT NULL,
  source_ref TEXT,
  fixture_set TEXT,
  author TEXT NOT NULL CHECK (author IN ('user', 'instance', 'fixture'))
);

-- Pool: raw + embedded (pressure by default) + optional pack genealogy
CREATE TABLE IF NOT EXISTS pool_chunk (
  id TEXT PRIMARY KEY,
  washed_at TEXT NOT NULL,
  body TEXT NOT NULL,
  source_ref TEXT,
  fixture_set TEXT,
  author TEXT NOT NULL,
  authority TEXT NOT NULL DEFAULT 'pressure' CHECK (authority = 'pressure'),
  embedding BLOB NOT NULL,
  domain TEXT,
  record_status TEXT,
  meta_json TEXT
);

-- Queryable supersession edges (glass law)
CREATE TABLE IF NOT EXISTS pool_edge (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_id TEXT NOT NULL,
  to_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('supersedes', 'superseded_by')),
  fixture_set TEXT,
  UNIQUE(from_id, to_id, kind)
);

-- Depth: settled ground only (genealogy copied from pool at Settle)
CREATE TABLE IF NOT EXISTS depth_entry (
  id TEXT PRIMARY KEY,
  settled_at TEXT NOT NULL,
  body TEXT NOT NULL,
  source_ref TEXT NOT NULL,
  fixture_set TEXT,
  author TEXT NOT NULL CHECK (author IN ('user', 'instance')),
  authority TEXT NOT NULL DEFAULT 'ground' CHECK (authority = 'ground'),
  use_limit TEXT,
  from_pool_id TEXT REFERENCES pool_chunk(id),
  domain TEXT,
  record_status TEXT,
  meta_json TEXT
);

-- Every Settle attempt
CREATE TABLE IF NOT EXISTS settle_audit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  attempted_at TEXT NOT NULL,
  pool_id TEXT,
  body TEXT NOT NULL,
  source_ref TEXT,
  author TEXT,
  outcome TEXT NOT NULL CHECK (outcome IN ('settled', 'refused')),
  reason TEXT NOT NULL
);

-- Exhale packets (stream)
CREATE TABLE IF NOT EXISTS stream_packet (
  id TEXT PRIMARY KEY,
  exhaled_at TEXT NOT NULL,
  stream_version TEXT NOT NULL DEFAULT 'fall/stream/v1',
  query TEXT,
  fixture_set TEXT,
  payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pool_fixture ON pool_chunk(fixture_set);
CREATE INDEX IF NOT EXISTS idx_pool_domain ON pool_chunk(domain);
CREATE INDEX IF NOT EXISTS idx_pool_edge_from ON pool_edge(from_id, kind);
CREATE INDEX IF NOT EXISTS idx_depth_fixture ON depth_entry(fixture_set);
CREATE INDEX IF NOT EXISTS idx_depth_domain ON depth_entry(domain);

-- DDL glass: depth must cite source; pool ancestry must exist when cited
CREATE TRIGGER IF NOT EXISTS depth_source_ref_nonempty
BEFORE INSERT ON depth_entry
WHEN NEW.source_ref IS NULL OR trim(NEW.source_ref) = ''
BEGIN
  SELECT RAISE(ABORT, 'depth requires non-empty source_ref');
END;

CREATE TRIGGER IF NOT EXISTS depth_from_pool_must_exist
BEFORE INSERT ON depth_entry
WHEN NEW.from_pool_id IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM pool_chunk WHERE id = NEW.from_pool_id)
BEGIN
  SELECT RAISE(ABORT, 'from_pool_id must reference an existing pool_chunk');
END;
