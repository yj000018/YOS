#!/usr/bin/env python3
"""
/YOS — Y-OS Launcher (Text Prototype v1.0)
==========================================
Queries Supabase (runtime cache) for all visible Y-REG objects.
Falls back to parsing Git/Markdown files if Supabase is unavailable.

Usage:
    python3 yos.py                  # Show public objects
    python3 yos.py --advanced       # Show public + advanced objects
    python3 yos.py --all            # Show all objects
    python3 yos.py --type skill     # Filter by type
    python3 yos.py --status active  # Filter by status
    python3 yos.py --json           # JSON output

Environment variables:
    YREG_SUPABASE_URL        Supabase project URL
    YREG_SUPABASE_KEY        Supabase anon or service_role key
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    os.system("sudo pip3 install pyyaml -q")
    import yaml

try:
    import requests
except ImportError:
    os.system("sudo pip3 install requests -q")
    import requests

# ── Config ───────────────────────────────────────────────────────────────────
REGISTRY_DIR  = Path(__file__).parent / "registry"
SUPABASE_URL  = os.environ.get("YREG_SUPABASE_URL", "https://zcgqqzlxzcxkswwlbxhc.supabase.co")
SUPABASE_KEY  = os.environ.get("YREG_SUPABASE_KEY", "")

TYPE_ICONS = {
    "protocol":         "📜",
    "agent":            "🤖",
    "project":          "📁",
    "knowledge_system": "🧠",
    "collection":       "📦",
    "workflow":         "⚙️",
    "service":          "🔌",
    "capability":       "⚡",
    "skill":            "🛠️",
    "automation":       "🔄",
    "prompt":           "💬",
    "script":           "📝",
    "command":          "⌨️",
}

STATUS_ICONS = {
    "idea":         "💡",
    "draft":        "✏️",
    "needs_review": "🔍",
    "active":       "✅",
    "broken":       "🔴",
    "deprecated":   "⚠️",
    "archived":     "📦",
}

# ── Supabase Fetch ────────────────────────────────────────────────────────────
def fetch_from_supabase(visibility_filter: list[str], type_filter: str | None, status_filter: str | None) -> tuple[list[dict], str]:
    """Fetch objects from Supabase runtime cache."""
    if not SUPABASE_KEY:
        return [], "no_key"

    headers = {
        "apikey":        SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type":  "application/json",
    }

    # Build query
    vis_param = ",".join(f'"{v}"' for v in visibility_filter)
    params = f"visibility=in.({','.join(visibility_filter)})&order=type.asc,name.asc"
    if type_filter:
        params += f"&type=eq.{type_filter}"
    if status_filter:
        params += f"&status=eq.{status_filter}"

    url = f"{SUPABASE_URL}/rest/v1/yreg_objects?{params}"

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.json(), "supabase"
        else:
            return [], f"error_{resp.status_code}"
    except requests.exceptions.ConnectionError:
        return [], "unreachable"
    except requests.exceptions.Timeout:
        return [], "timeout"

# ── Git Fallback ──────────────────────────────────────────────────────────────
def fetch_from_git(visibility_filter: list[str], type_filter: str | None, status_filter: str | None) -> tuple[list[dict], str]:
    """Fallback: parse Markdown files directly from Git registry."""
    objects = []
    for filepath in sorted(REGISTRY_DIR.glob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            continue
        try:
            data = yaml.safe_load(match.group(1))
            if not isinstance(data, dict):
                continue
            if data.get("visibility") not in visibility_filter:
                continue
            if type_filter and data.get("type") != type_filter:
                continue
            if status_filter and data.get("status") != status_filter:
                continue
            objects.append(data)
        except yaml.YAMLError:
            continue

    objects.sort(key=lambda x: (x.get("type", ""), x.get("name", "")))
    return objects, "git_fallback"

# ── Render ────────────────────────────────────────────────────────────────────
def render_text(objects: list[dict], source: str) -> str:
    """Render objects as a structured text menu."""
    lines = []
    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════════╗")
    lines.append("║              /YOS — Y-OS Launcher v1.0                  ║")
    lines.append(f"║  Source: {'Supabase (cache)' if source == 'supabase' else 'Git/Markdown (fallback)':40s}║")
    lines.append(f"║  Objects: {str(len(objects)):3s}  │  {datetime.now().strftime('%Y-%m-%d %H:%M'):20s}              ║")
    lines.append("╚══════════════════════════════════════════════════════════╝")
    lines.append("")

    if not objects:
        lines.append("  No objects found matching your filters.")
        return "\n".join(lines)

    # Group by type
    by_type: dict[str, list[dict]] = {}
    for obj in objects:
        t = obj.get("type", "unknown")
        by_type.setdefault(t, []).append(obj)

    for obj_type, items in sorted(by_type.items()):
        icon = TYPE_ICONS.get(obj_type, "•")
        lines.append(f"  {icon}  {obj_type.upper().replace('_', ' ')}  ({len(items)})")
        lines.append("  " + "─" * 54)
        for item in items:
            s_icon = STATUS_ICONS.get(item.get("status", ""), "•")
            name    = item.get("name", item.get("slug", "?"))
            desc    = item.get("description", "")
            version = item.get("version", "")
            # Truncate description
            if len(desc) > 52:
                desc = desc[:49] + "..."
            lines.append(f"    {s_icon} {name:<20s} v{version:<8s} {desc}")
        lines.append("")

    lines.append("  Legend: ✅ active  ✏️ draft  🔍 needs_review  ⚠️ deprecated")
    lines.append(f"  Source: {source}")
    lines.append("")
    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="/YOS — Y-OS Launcher")
    parser.add_argument("--advanced", action="store_true", help="Include advanced visibility objects")
    parser.add_argument("--all",      action="store_true", help="Include all objects (public + advanced + hidden)")
    parser.add_argument("--type",     type=str, default=None, help="Filter by object type")
    parser.add_argument("--status",   type=str, default=None, help="Filter by status")
    parser.add_argument("--json",     action="store_true", help="Output raw JSON")
    parser.add_argument("--source",   type=str, choices=["auto", "supabase", "git"], default="auto",
                        help="Force data source (default: auto with fallback)")
    args = parser.parse_args()

    # Determine visibility filter
    if args.all:
        visibility = ["public", "advanced", "hidden"]
    elif args.advanced:
        visibility = ["public", "advanced"]
    else:
        visibility = ["public"]

    objects = []
    source  = "none"

    # Fetch data
    if args.source == "git":
        objects, source = fetch_from_git(visibility, args.type, args.status)
    elif args.source == "supabase":
        objects, source = fetch_from_supabase(visibility, args.type, args.status)
        if not objects and source != "supabase":
            print(f"[WARN] Supabase unavailable ({source}). No fallback requested.", file=sys.stderr)
    else:
        # Auto mode: try Supabase first, fallback to Git
        objects, source = fetch_from_supabase(visibility, args.type, args.status)
        if source != "supabase" or not objects:
            if source != "supabase":
                print(f"[WARN] Supabase unavailable ({source}). Falling back to Git/Markdown.", file=sys.stderr)
            objects, source = fetch_from_git(visibility, args.type, args.status)

    # Output
    if args.json:
        print(json.dumps(objects, indent=2, ensure_ascii=False))
    else:
        print(render_text(objects, source))

if __name__ == "__main__":
    main()
