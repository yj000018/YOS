#!/usr/bin/env python3
"""
pack_command.py — yOS Continuity Core Phase 1
/pack command — one-click Context Pack generation.

This is the user-facing entry point for generating a Context Pack.
Reads project state from Notion / local config / JSON input.
Generates pack at requested tier and writes to context_packs/ directory.

Usage:
  python3 pack_command.py [PROJECT] [--tier T1_standard] [--preview] [--output PATH]
  python3 pack_command.py yos-continuity-core --tier T2_full_lineage --preview
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from context_pack_generator import generate_pack, CANONICAL_TIERS
from pack_staleness_detector import detect_staleness

CONTEXT_PACKS_DIR = Path(__file__).parent.parent / "core/orchestration/context_packs"
PACK_REGISTRY_PATH = CONTEXT_PACKS_DIR / "pack_registry.json"

PREVIEW_LINES = 30  # Lines to show in preview mode


def load_pack_registry() -> dict:
    """Load or initialize the pack registry."""
    if PACK_REGISTRY_PATH.exists():
        return json.loads(PACK_REGISTRY_PATH.read_text())
    return {"packs": []}


def save_pack_registry(registry: dict):
    """Save the pack registry."""
    PACK_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACK_REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


def register_pack(pack_path: Path, project: str, tier: str, checksum: str):
    """Register a generated pack in the registry."""
    registry = load_pack_registry()
    entry = {
        "pack_path": str(pack_path),
        "project": project,
        "tier": tier,
        "checksum": checksum,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
    registry["packs"].append(entry)
    save_pack_registry(registry)


def preview_pack(pack_content: str, lines: int = PREVIEW_LINES) -> str:
    """Show first N lines of pack as preview."""
    pack_lines = pack_content.split("\n")
    preview = "\n".join(pack_lines[:lines])
    if len(pack_lines) > lines:
        preview += f"\n\n... [{len(pack_lines) - lines} more lines — use --output to save full pack]"
    return preview


def resolve_project_data(project: str, input_json: Path = None) -> dict:
    """Resolve project data from input sources."""
    if input_json and input_json.exists():
        return json.loads(input_json.read_text())

    # Minimal project data from project name
    return {
        "project": project,
        "founder": "Yannick",
        "program": "yOS",
        "mission": f"Context pack for project: {project}",
        "current_phase": "active",
        "task_class": "architecture",
        "constraints": [
            "Do not start F02",
            "Do not generate book prose",
            "Do not modify manuscript",
            "Do not implement scripts without GO",
            "Do not delete files",
            "FCS is downstream application",
            "yOS Continuity Core belongs to yOS Core"
        ],
        "project_state": {
            "status": "active",
            "milestone": "",
            "blockers": "none",
            "last_completed": ""
        },
        "active_decisions": [],
        "key_artifacts": [],
        "next_action": "",
        "expected_output": "",
        "success_criteria": ""
    }


def main():
    parser = argparse.ArgumentParser(description="yOS /pack command — Context Pack Generator")
    parser.add_argument("project", nargs="?", default="yos", help="Project name")
    parser.add_argument("--tier", default="T1_standard", choices=CANONICAL_TIERS)
    parser.add_argument("--preview", action="store_true", help="Preview pack before saving")
    parser.add_argument("--output", type=Path, help="Custom output path")
    parser.add_argument("--input-json", type=Path, help="JSON file with project data")
    parser.add_argument("--no-register", action="store_true", help="Skip registry entry")
    args = parser.parse_args()

    project_data = resolve_project_data(args.project, args.input_json)

    print(f"[/pack] Generating {args.tier} pack for project: {args.project}")

    pack_content = generate_pack(project_data, args.tier)

    if args.preview:
        print("\n=== PACK PREVIEW ===")
        print(preview_pack(pack_content))
        print("\n[Preview complete — use --output to save]")
        return

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{args.project}_{args.tier}_{ts}.md"
        output_path = CONTEXT_PACKS_DIR / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(pack_content, encoding="utf-8")

    # Extract checksum from generated pack
    import re
    checksum_match = re.search(r"pack_checksum: ([a-f0-9]{64})", pack_content)
    checksum = checksum_match.group(1) if checksum_match else "unknown"

    if not args.no_register:
        register_pack(output_path, args.project, args.tier, checksum)

    print(f"[/pack] ✅ Pack saved: {output_path}")
    print(f"[/pack] Checksum: {checksum[:16]}...")
    print(f"[/pack] Tier: {args.tier}")
    print(f"[/pack] Lines: {len(pack_content.split(chr(10)))}")


if __name__ == "__main__":
    main()
