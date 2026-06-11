#!/usr/bin/env python3
"""
Y-REG Sync via Supabase MCP (execute_sql)
==========================================
Uses the Supabase MCP server to upsert objects directly via SQL.
This avoids the need for a service_role key in the environment.

Usage:
    python3 yreg_sync_mcp.py [--dry-run] [--verbose]
"""

import os
import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    os.system("sudo pip3 install pyyaml -q")
    import yaml

REGISTRY_DIR = Path(__file__).parent / "registry"
PROJECT_ID   = "zcgqqzlxzcxkswwlbxhc"

VALID_TYPES    = {"protocol","agent","project","knowledge_system","collection","workflow","service","capability","skill","automation","prompt","script","command"}
VALID_STATUSES = {"idea","draft","needs_review","active","broken","deprecated","archived"}
VALID_VIS      = {"public","advanced","hidden"}
VALID_STAGES   = {"discovery","candidate","validation","registry"}

def parse_frontmatter(filepath: Path) -> dict | None:
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None

def validate(data: dict) -> tuple[bool, list[str]]:
    errors = []
    for f in ["slug","name","type","status","visibility","registration_stage","description"]:
        if not data.get(f):
            errors.append(f"Missing: {f}")
    if data.get("type") not in VALID_TYPES:
        errors.append(f"Invalid type: {data.get('type')}")
    if data.get("status") not in VALID_STATUSES:
        errors.append(f"Invalid status: {data.get('status')}")
    if data.get("visibility") not in VALID_VIS:
        errors.append(f"Invalid visibility: {data.get('visibility')}")
    if data.get("registration_stage") not in VALID_STAGES:
        errors.append(f"Invalid stage: {data.get('registration_stage')}")
    return len(errors) == 0, errors

def escape_sql_string(s: str) -> str:
    """Escape single quotes for SQL."""
    return str(s).replace("'", "''")

def build_upsert_sql(data: dict) -> str:
    slug    = escape_sql_string(data["slug"])
    name    = escape_sql_string(data["name"])
    typ     = data["type"]
    status  = data["status"]
    vis     = data["visibility"]
    stage   = data["registration_stage"]
    desc    = escape_sql_string(data.get("description",""))
    tags    = data.get("tags", [])
    tags_pg = "{" + ",".join(escape_sql_string(t) for t in tags) + "}"
    git_p   = escape_sql_string(data.get("git_path",""))
    ver     = escape_sql_string(data.get("version","0.1.0"))
    now     = datetime.now(timezone.utc).isoformat()

    return f"""
INSERT INTO yreg_objects (slug, name, type, status, visibility, registration_stage, description, tags, git_path, version, synced_at)
VALUES (
  '{slug}', '{name}', '{typ}'::"object_type", '{status}'::"object_status",
  '{vis}'::"object_visibility", '{stage}'::"registration_stage",
  '{desc}', ARRAY[{",".join(f"'{escape_sql_string(t)}'" for t in tags)}]::text[],
  '{git_p}', '{ver}', '{now}'
)
ON CONFLICT (slug) DO UPDATE SET
  name               = EXCLUDED.name,
  type               = EXCLUDED.type,
  status             = EXCLUDED.status,
  visibility         = EXCLUDED.visibility,
  registration_stage = EXCLUDED.registration_stage,
  description        = EXCLUDED.description,
  tags               = EXCLUDED.tags,
  git_path           = EXCLUDED.git_path,
  version            = EXCLUDED.version,
  synced_at          = EXCLUDED.synced_at;
""".strip()

def run_sql_via_mcp(sql: str) -> tuple[bool, str]:
    """Execute SQL via Supabase MCP server."""
    payload = json.dumps({"project_id": PROJECT_ID, "query": sql})
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql", "--server", "supabase", "--input", payload]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        if "error" in output.lower() and "Error:" in output:
            return False, output[:300]
        return True, output[:200]
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Y-REG Sync via Supabase MCP")
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--verbose",  action="store_true")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Y-REG Sync (MCP) — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"  Registry: {REGISTRY_DIR}")
    print(f"  Project:  {PROJECT_ID}")
    print(f"  Time:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    files = sorted(REGISTRY_DIR.glob("*.md"))
    if not files:
        print("[ERROR] No .md files found in registry/")
        sys.exit(1)

    ok, skipped, errors = [], [], []

    for filepath in files:
        data = parse_frontmatter(filepath)
        if data is None:
            print(f"  [SKIP] No frontmatter: {filepath.name}")
            skipped.append(filepath.name)
            continue

        valid, errs = validate(data)
        if not valid:
            print(f"  [INVALID] {filepath.name}: {', '.join(errs)}")
            errors.append(filepath.name)
            continue

        sql = build_upsert_sql(data)

        if args.dry_run:
            print(f"  [DRY] {data['slug']} ({data['type']}) [{data['status']}]")
            if args.verbose:
                print(f"    SQL: {sql[:120]}...")
            ok.append(data["slug"])
            continue

        success, msg = run_sql_via_mcp(sql)
        if success:
            print(f"  [✓] {data['slug']} ({data['type']}) [{data['status']}] [{data['visibility']}]")
            ok.append(data["slug"])
        else:
            print(f"  [✗] {data['slug']}: {msg}")
            errors.append(filepath.name)

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"  Files:    {len(files)}")
    print(f"  Synced:   {len(ok)}")
    print(f"  Skipped:  {len(skipped)}")
    print(f"  Errors:   {len(errors)}")
    print(f"{'='*60}\n")

    if errors:
        sys.exit(1)
    print("Sync complete.\n")

if __name__ == "__main__":
    main()
