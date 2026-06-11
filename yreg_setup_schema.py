#!/usr/bin/env python3
"""Apply Y-REG schema to Supabase via MCP execute_sql, step by step."""
import subprocess, json, sys

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

STEPS = [
    ("Drop existing types if any", """
DO $$ BEGIN
  DROP TYPE IF EXISTS object_type CASCADE;
  DROP TYPE IF EXISTS object_status CASCADE;
  DROP TYPE IF EXISTS object_visibility CASCADE;
  DROP TYPE IF EXISTS registration_stage CASCADE;
EXCEPTION WHEN OTHERS THEN NULL;
END $$;
"""),
    ("Create object_type enum", """
CREATE TYPE object_type AS ENUM (
  'protocol','agent','project','knowledge_system','collection',
  'workflow','service','capability','skill','automation',
  'prompt','script','command'
);
"""),
    ("Create object_status enum", """
CREATE TYPE object_status AS ENUM (
  'idea','draft','needs_review','active','broken','deprecated','archived'
);
"""),
    ("Create object_visibility enum", """
CREATE TYPE object_visibility AS ENUM ('public','advanced','hidden');
"""),
    ("Create registration_stage enum", """
CREATE TYPE registration_stage AS ENUM ('discovery','candidate','validation','registry');
"""),
    ("Create yreg_objects table", """
CREATE TABLE IF NOT EXISTS yreg_objects (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  type               object_type NOT NULL,
  status             object_status NOT NULL DEFAULT 'draft',
  visibility         object_visibility NOT NULL DEFAULT 'hidden',
  registration_stage registration_stage NOT NULL DEFAULT 'discovery',
  description        TEXT,
  tags               TEXT[] DEFAULT '{}',
  git_path           TEXT,
  version            TEXT DEFAULT '0.1.0',
  created_at         TIMESTAMPTZ DEFAULT now(),
  updated_at         TIMESTAMPTZ DEFAULT now(),
  synced_at          TIMESTAMPTZ DEFAULT now()
);
"""),
    ("Create yreg_relations table", """
CREATE TABLE IF NOT EXISTS yreg_relations (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_slug   TEXT NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
  target_slug   TEXT NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
  relation_type TEXT NOT NULL,
  created_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(source_slug, target_slug, relation_type)
);
"""),
    ("Create yreg_capabilities table", """
CREATE TABLE IF NOT EXISTS yreg_capabilities (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug             TEXT UNIQUE NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
  input_schema     JSONB,
  output_schema    JSONB,
  implemented_by   TEXT[],
  created_at       TIMESTAMPTZ DEFAULT now()
);
"""),
    ("Create indexes", """
CREATE INDEX IF NOT EXISTS idx_objects_visibility   ON yreg_objects(visibility);
CREATE INDEX IF NOT EXISTS idx_objects_type         ON yreg_objects(type);
CREATE INDEX IF NOT EXISTS idx_objects_status       ON yreg_objects(status);
CREATE INDEX IF NOT EXISTS idx_objects_registration ON yreg_objects(registration_stage);
"""),
    ("Create updated_at trigger", """
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_objects_updated_at ON yreg_objects;
CREATE TRIGGER trg_objects_updated_at
  BEFORE UPDATE ON yreg_objects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
"""),
]

def run_sql(sql: str) -> tuple[bool, str]:
    payload = json.dumps({"project_id": PROJECT_ID, "query": sql.strip()})
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql", "--server", "supabase", "--input", payload]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    if '"error"' in output and 'Error:' in output:
        return False, output
    return True, output

print(f"\n{'='*55}")
print("  Y-REG Schema Setup")
print(f"{'='*55}\n")

all_ok = True
for label, sql in STEPS:
    ok, msg = run_sql(sql)
    status = "✓" if ok else "✗"
    print(f"  [{status}] {label}")
    if not ok:
        print(f"       {msg[:200]}")
        all_ok = False

print(f"\n{'='*55}")
print(f"  {'Schema applied successfully!' if all_ok else 'Schema setup FAILED — see errors above.'}")
print(f"{'='*55}\n")

sys.exit(0 if all_ok else 1)
