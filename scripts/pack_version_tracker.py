#!/usr/bin/env python3
"""
pack_version_tracker.py — yOS Continuity Core Phase 1
Track Context Pack versions, maintain history, enable rollback.

Each pack update creates a versioned entry in the pack registry.
Rollback restores a previous version by pack_id or version number.

Usage:
  python3 pack_version_tracker.py --list [--project PROJECT]
  python3 pack_version_tracker.py --register --pack PATH --project PROJECT
  python3 pack_version_tracker.py --rollback --pack-id PACK_ID --output PATH
  python3 pack_version_tracker.py --diff --pack-a PACK_ID --pack-b PACK_ID
"""

import re
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

CONTEXT_PACKS_DIR = Path(__file__).parent.parent / "core/orchestration/context_packs"
PACK_REGISTRY_PATH = CONTEXT_PACKS_DIR / "pack_registry.json"
PACK_HISTORY_DIR = CONTEXT_PACKS_DIR / "history"


def load_registry() -> dict:
    if PACK_REGISTRY_PATH.exists():
        return json.loads(PACK_REGISTRY_PATH.read_text())
    return {"packs": [], "version": "1.0"}


def save_registry(registry: dict):
    PACK_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACK_REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


def register_pack(pack_path: Path, project: str, tier: str, notes: str = "") -> dict:
    """Register a pack in the version history."""
    content = pack_path.read_text(encoding="utf-8")

    # Extract pack_id and checksum from content
    pack_id_match = re.search(r"^pack_id:\s*(.+)$", content, re.MULTILINE)
    checksum_match = re.search(r"^pack_checksum:\s*([a-f0-9]+)", content, re.MULTILINE)
    tier_match = re.search(r"^tier:\s*(.+)$", content, re.MULTILINE)

    pack_id = pack_id_match.group(1).strip() if pack_id_match else f"pack_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    checksum = checksum_match.group(1).strip() if checksum_match else "unknown"
    detected_tier = tier_match.group(1).strip() if tier_match else tier

    # Save to history
    PACK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    history_path = PACK_HISTORY_DIR / f"{pack_id}.md"
    history_path.write_text(content)

    registry = load_registry()

    # Get version number for this project
    project_packs = [p for p in registry["packs"] if p.get("project") == project]
    version_num = len(project_packs) + 1

    entry = {
        "pack_id": pack_id,
        "version": version_num,
        "project": project,
        "tier": detected_tier,
        "checksum": checksum,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "history_path": str(history_path),
        "notes": notes
    }

    registry["packs"].append(entry)
    save_registry(registry)

    return entry


def list_packs(project: str = None) -> list:
    """List all registered packs, optionally filtered by project."""
    registry = load_registry()
    packs = registry["packs"]
    if project:
        packs = [p for p in packs if p.get("project") == project]
    return sorted(packs, key=lambda x: x.get("registered_at", ""), reverse=True)


def rollback_pack(pack_id: str, output_path: Path) -> dict:
    """Restore a specific pack version by pack_id."""
    registry = load_registry()
    entry = next((p for p in registry["packs"] if p["pack_id"] == pack_id), None)

    if not entry:
        return {"success": False, "error": f"Pack ID '{pack_id}' not found in registry"}

    history_path = Path(entry["history_path"])
    if not history_path.exists():
        return {"success": False, "error": f"History file not found: {history_path}"}

    content = history_path.read_text()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    return {
        "success": True,
        "pack_id": pack_id,
        "version": entry["version"],
        "project": entry["project"],
        "tier": entry["tier"],
        "restored_to": str(output_path),
        "original_registered_at": entry["registered_at"]
    }


def diff_packs(pack_id_a: str, pack_id_b: str) -> dict:
    """Show diff summary between two pack versions."""
    registry = load_registry()

    entry_a = next((p for p in registry["packs"] if p["pack_id"] == pack_id_a), None)
    entry_b = next((p for p in registry["packs"] if p["pack_id"] == pack_id_b), None)

    if not entry_a:
        return {"error": f"Pack A '{pack_id_a}' not found"}
    if not entry_b:
        return {"error": f"Pack B '{pack_id_b}' not found"}

    content_a = Path(entry_a["history_path"]).read_text() if Path(entry_a["history_path"]).exists() else ""
    content_b = Path(entry_b["history_path"]).read_text() if Path(entry_b["history_path"]).exists() else ""

    lines_a = set(content_a.split("\n"))
    lines_b = set(content_b.split("\n"))

    added = lines_b - lines_a
    removed = lines_a - lines_b

    return {
        "pack_a": {"pack_id": pack_id_a, "version": entry_a["version"], "tier": entry_a["tier"]},
        "pack_b": {"pack_id": pack_id_b, "version": entry_b["version"], "tier": entry_b["tier"]},
        "lines_added": len(added),
        "lines_removed": len(removed),
        "sample_added": list(added)[:5],
        "sample_removed": list(removed)[:5],
        "checksum_changed": entry_a["checksum"] != entry_b["checksum"]
    }


def main():
    parser = argparse.ArgumentParser(description="yOS Pack Version Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--project")

    # Register
    reg_parser = subparsers.add_parser("register")
    reg_parser.add_argument("--pack", type=Path, required=True)
    reg_parser.add_argument("--project", required=True)
    reg_parser.add_argument("--tier", default="T1_standard")
    reg_parser.add_argument("--notes", default="")

    # Rollback
    rb_parser = subparsers.add_parser("rollback")
    rb_parser.add_argument("--pack-id", required=True)
    rb_parser.add_argument("--output", type=Path, required=True)

    # Diff
    diff_parser = subparsers.add_parser("diff")
    diff_parser.add_argument("--pack-a", required=True)
    diff_parser.add_argument("--pack-b", required=True)

    # Legacy flags support
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--pack", type=Path)
    parser.add_argument("--project")
    parser.add_argument("--pack-id")
    parser.add_argument("--pack-a")
    parser.add_argument("--pack-b")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    # Handle legacy flags
    if args.list or args.command == "list":
        packs = list_packs(args.project)
        if args.json:
            print(json.dumps(packs, indent=2))
        else:
            print(f"{'Pack ID':<40} {'Version':<8} {'Project':<20} {'Tier':<20} {'Registered'}")
            print("-" * 110)
            for p in packs:
                print(f"{p['pack_id']:<40} {p['version']:<8} {p['project']:<20} {p['tier']:<20} {p['registered_at']}")

    elif args.register or args.command == "register":
        pack_path = args.pack
        if not pack_path or not pack_path.exists():
            print("[ERROR] --pack required and must exist", file=sys.stderr)
            sys.exit(1)
        entry = register_pack(pack_path, args.project or "unknown", args.tier or "T1_standard", args.notes or "")
        if args.json:
            print(json.dumps(entry, indent=2))
        else:
            print(f"Registered: {entry['pack_id']} v{entry['version']} ({entry['tier']})")

    elif args.rollback or args.command == "rollback":
        result = rollback_pack(args.pack_id, args.output)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"✅ Rolled back to: {result['pack_id']} v{result['version']} → {result['restored_to']}")
            else:
                print(f"❌ Rollback failed: {result['error']}")
                sys.exit(1)

    elif args.diff or args.command == "diff":
        result = diff_packs(args.pack_a, args.pack_b)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(f"Diff: {result['pack_a']['pack_id']} (v{result['pack_a']['version']}) → {result['pack_b']['pack_id']} (v{result['pack_b']['version']})")
                print(f"Lines added: {result['lines_added']}, removed: {result['lines_removed']}")
                print(f"Checksum changed: {result['checksum_changed']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
