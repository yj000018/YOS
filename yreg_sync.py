#!/usr/bin/env python3
"""
Y-REG Sync — Git → Supabase Parser
====================================
Source of truth: Obsidian + Git (registry/*.md)
Runtime cache:   Supabase (yreg_objects table)
Direction:       UNIDIRECTIONAL — Git → Supabase ONLY

Usage:
    python3 yreg_sync.py [--dry-run] [--verbose]

Environment variables required:
    SUPABASE_URL         e.g. https://zcgqqzlxzcxkswwlbxhc.supabase.co
    SUPABASE_SERVICE_KEY Supabase service_role key (NOT anon key)
"""

import os
import sys
import json
import glob
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Dependencies ─────────────────────────────────────────────────────────────
try:
    import yaml
except ImportError:
    print("Installing PyYAML...")
    os.system("sudo pip3 install pyyaml -q")
    import yaml

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("sudo pip3 install requests -q")
    import requests

# ── Config ───────────────────────────────────────────────────────────────────
REGISTRY_DIR = Path(__file__).parent / "registry"
SUPABASE_URL = os.environ.get("YREG_SUPABASE_URL", "https://zcgqqzlxzcxkswwlbxhc.supabase.co")
SUPABASE_KEY = os.environ.get("YREG_SUPABASE_KEY", "")

VALID_TYPES = {
    "protocol", "agent", "project", "knowledge_system", "collection",
    "workflow", "service", "capability", "skill", "automation",
    "prompt", "script", "command"
}
VALID_STATUSES = {"idea", "draft", "needs_review", "active", "broken", "deprecated", "archived"}
VALID_VISIBILITY = {"public", "advanced", "hidden"}
VALID_STAGES = {"discovery", "candidate", "validation", "registry"}

# ── Frontmatter Parser ───────────────────────────────────────────────────────
def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract and parse YAML frontmatter from a Markdown file."""
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else None
    except yaml.YAMLError as e:
        print(f"  [WARN] YAML parse error in {filepath.name}: {e}")
        return None

# ── Validation ───────────────────────────────────────────────────────────────
def validate_object(data: dict, filename: str) -> tuple[bool, list[str]]:
    """Validate required fields and enum values."""
    errors = []
    required = ["slug", "name", "type", "status", "visibility", "registration_stage", "description"]
    for field in required:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")

    if data.get("type") not in VALID_TYPES:
        errors.append(f"Invalid type: {data.get('type')} — must be one of {VALID_TYPES}")
    if data.get("status") not in VALID_STATUSES:
        errors.append(f"Invalid status: {data.get('status')}")
    if data.get("visibility") not in VALID_VISIBILITY:
        errors.append(f"Invalid visibility: {data.get('visibility')}")
    if data.get("registration_stage") not in VALID_STAGES:
        errors.append(f"Invalid registration_stage: {data.get('registration_stage')}")

    return len(errors) == 0, errors

# ── Supabase Upsert ───────────────────────────────────────────────────────────
def upsert_object(data: dict, dry_run: bool = False) -> bool:
    """Upsert a single object into Supabase yreg_objects."""
    payload = {
        "slug":               data["slug"],
        "name":               data["name"],
        "type":               data["type"],
        "status":             data["status"],
        "visibility":         data["visibility"],
        "registration_stage": data["registration_stage"],
        "description":        data.get("description", ""),
        "tags":               data.get("tags", []),
        "git_path":           data.get("git_path", ""),
        "version":            data.get("version", "0.1.0"),
        "synced_at":          datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        print(f"  [DRY-RUN] Would upsert: {payload['slug']} ({payload['type']})")
        return True

    if not SUPABASE_KEY:
        print("  [ERROR] YREG_SUPABASE_KEY not set. Cannot upsert.")
        return False

    headers = {
        "apikey":        SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type":  "application/json",
        "Prefer":        "resolution=merge-duplicates",
    }
    url = f"{SUPABASE_URL}/rest/v1/yreg_objects"
    resp = requests.post(url, headers=headers, json=payload, timeout=15)

    if resp.status_code in (200, 201):
        return True
    else:
        print(f"  [ERROR] Supabase upsert failed ({resp.status_code}): {resp.text[:200]}")
        return False

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Y-REG Sync: Git → Supabase")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing to Supabase")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Y-REG Sync — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"  Registry: {REGISTRY_DIR}")
    print(f"  Supabase: {SUPABASE_URL}")
    print(f"  Time:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    files = sorted(REGISTRY_DIR.glob("*.md"))
    if not files:
        print("[ERROR] No .md files found in registry/")
        sys.exit(1)

    results = {"ok": [], "skipped": [], "errors": []}

    for filepath in files:
        if args.verbose:
            print(f"Processing: {filepath.name}")

        data = parse_frontmatter(filepath)
        if data is None:
            print(f"  [SKIP] No valid frontmatter: {filepath.name}")
            results["skipped"].append(filepath.name)
            continue

        valid, errors = validate_object(data, filepath.name)
        if not valid:
            print(f"  [INVALID] {filepath.name}:")
            for err in errors:
                print(f"    - {err}")
            results["errors"].append({"file": filepath.name, "errors": errors})
            continue

        success = upsert_object(data, dry_run=args.dry_run)
        if success:
            status_icon = "✓" if not args.dry_run else "~"
            print(f"  [{status_icon}] {data['slug']} ({data['type']}) [{data['status']}] [{data['visibility']}]")
            results["ok"].append(data["slug"])
        else:
            results["errors"].append({"file": filepath.name, "errors": ["Supabase upsert failed"]})

    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"  Total files:  {len(files)}")
    print(f"  Synced:       {len(results['ok'])}")
    print(f"  Skipped:      {len(results['skipped'])}")
    print(f"  Errors:       {len(results['errors'])}")
    print(f"{'='*60}\n")

    if results["errors"]:
        print("Errors:")
        for e in results["errors"]:
            print(f"  {e['file']}: {', '.join(e['errors'])}")
        sys.exit(1)

    print("Sync complete.\n")

if __name__ == "__main__":
    main()
