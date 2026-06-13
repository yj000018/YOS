#!/usr/bin/env python3
"""
MISSION-013B — Obsidian Graph Quality Audit
Quantitative analysis of y-os-doctrine corpus after MISSION-013 enrichment.
"""

import re
import json
import yaml
from pathlib import Path
from collections import defaultdict, Counter

REPO_ROOT = Path("/home/ubuntu/yreg")
OUT_DIR = REPO_ROOT / "mission_013b"
OUT_DIR.mkdir(exist_ok=True)

# ─── SCAN ────────────────────────────────────────────────────────────────────

def scan(root):
    files = []
    for p in sorted(root.rglob("*.md")):
        parts = p.parts
        if ".git" in parts or "node_modules" in parts:
            continue
        rel = str(p.relative_to(root))
        files.append({"path": p, "rel": rel, "stem": p.stem, "folder": str(p.relative_to(root).parent)})
    return files

def parse_fm(content):
    if not content.startswith("---\n"):
        return {}, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[4:end]) or {}
    except Exception:
        fm = {}
    body = content[end+5:]
    return fm, body

def extract_wikilinks(text):
    return re.findall(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", text)

def extract_wikilinks_raw(text):
    """All [[...]] including YAML quoted ones."""
    return re.findall(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", text)

# ─── MAIN AUDIT ──────────────────────────────────────────────────────────────

def run_audit():
    files = scan(REPO_ROOT)
    total = len(files)

    # Per-file data
    data = {}
    for f in files:
        content = f["path"].read_text(errors="ignore")
        fm, body = parse_fm(content)
        # Wikilinks in full content (YAML + body)
        wikilinks_out = extract_wikilinks_raw(content)
        data[f["rel"]] = {
            "rel": f["rel"],
            "stem": f["stem"],
            "folder": f["folder"],
            "has_fm": bool(fm),
            "fm": fm,
            "body": body,
            "wikilinks_out": wikilinks_out,
            "wikilinks_in": [],  # filled below
            "type": fm.get("type", "unknown"),
            "status": fm.get("status", ""),
            "tags": fm.get("tags", []),
            "aliases": fm.get("aliases", []),
            "related_adrs": fm.get("related_adrs", []),
            "related_missions": fm.get("related_missions", []),
            "mission": fm.get("mission", ""),
            "owner": fm.get("owner", ""),
            "id": fm.get("id", ""),
        }

    # Build inbound link index
    for rel, d in data.items():
        for link in d["wikilinks_out"]:
            # Try to resolve link to a file
            for target_rel, td in data.items():
                if td["stem"] == link or td["stem"] == link.replace(" ", "_"):
                    td["wikilinks_in"].append(rel)
                    break

    # ── METRICS ──────────────────────────────────────────────────────────────

    # Files by type
    type_counts = Counter(d["type"] for d in data.values())

    # Frontmatter coverage
    with_fm = sum(1 for d in data.values() if d["has_fm"])
    fm_fields_populated = []
    for d in data.values():
        if d["has_fm"]:
            populated = sum(1 for v in d["fm"].values() if v and v != [] and v != "")
            fm_fields_populated.append(populated)
    avg_fm_fields = round(sum(fm_fields_populated) / len(fm_fields_populated), 1) if fm_fields_populated else 0

    # Tags / aliases
    with_tags = sum(1 for d in data.values() if d["tags"])
    with_aliases = sum(1 for d in data.values() if d["aliases"])

    # Wikilinks
    total_wikilinks_out = sum(len(d["wikilinks_out"]) for d in data.values())
    files_with_outlinks = sum(1 for d in data.values() if d["wikilinks_out"])
    files_with_inlinks = sum(1 for d in data.values() if d["wikilinks_in"])

    # Orphans (no in, no out)
    orphans = [rel for rel, d in data.items() if not d["wikilinks_out"] and not d["wikilinks_in"]]

    # No inbound
    no_inbound = [rel for rel, d in data.items() if not d["wikilinks_in"]]

    # No outbound
    no_outbound = [rel for rel, d in data.items() if not d["wikilinks_out"]]

    # Unknown type
    unknowns = [rel for rel, d in data.items() if d["type"] == "unknown"]

    # ADR-specific
    adrs = {rel: d for rel, d in data.items() if d["type"] == "adr"}
    adrs_without_mission_links = [rel for rel, d in adrs.items() if not d["related_missions"]]
    adrs_without_adr_links = [rel for rel, d in adrs.items() if not d["related_adrs"]]

    # Mission-specific
    missions = {rel: d for rel, d in data.items() if d["type"] == "mission"}
    missions_without_adr_links = [rel for rel, d in missions.items() if not d["related_adrs"]]

    # Top 20 most connected nodes (in + out)
    connectivity = {rel: len(d["wikilinks_out"]) + len(d["wikilinks_in"]) for rel, d in data.items()}
    top20_connected = sorted(connectivity.items(), key=lambda x: -x[1])[:20]

    # Top 20 orphan/low-value (fewest connections)
    bottom20 = sorted(connectivity.items(), key=lambda x: x[1])[:20]

    # MOC files
    moc_files = [rel for rel, d in data.items() if d["type"] == "index" or "MOC" in d["stem"] or "Home" in d["stem"]]

    # YAML fields: count populated vs empty across all files
    all_fm_keys = set()
    for d in data.values():
        all_fm_keys.update(d["fm"].keys())
    yaml_field_stats = {}
    for key in sorted(all_fm_keys):
        populated = sum(1 for d in data.values() if d["fm"].get(key) and d["fm"][key] != [] and d["fm"][key] != "")
        yaml_field_stats[key] = {"populated": populated, "pct": round(populated/total*100, 1)}

    # ── COMPILE REPORT ───────────────────────────────────────────────────────

    metrics = {
        "total_md_files": total,
        "files_by_type": dict(type_counts.most_common()),
        "frontmatter_coverage": {"count": with_fm, "pct": round(with_fm/total*100, 1)},
        "avg_fm_fields_populated": avg_fm_fields,
        "files_with_tags": {"count": with_tags, "pct": round(with_tags/total*100, 1)},
        "files_with_aliases": {"count": with_aliases, "pct": round(with_aliases/total*100, 1)},
        "total_wikilinks": total_wikilinks_out,
        "files_with_outbound_links": {"count": files_with_outlinks, "pct": round(files_with_outlinks/total*100, 1)},
        "files_with_inbound_links": {"count": files_with_inlinks, "pct": round(files_with_inlinks/total*100, 1)},
        "orphan_files": {"count": len(orphans), "pct": round(len(orphans)/total*100, 1)},
        "files_no_inbound": {"count": len(no_inbound), "pct": round(len(no_inbound)/total*100, 1)},
        "files_no_outbound": {"count": len(no_outbound), "pct": round(len(no_outbound)/total*100, 1)},
        "unknown_type_files": {"count": len(unknowns), "pct": round(len(unknowns)/total*100, 1)},
        "adrs_total": len(adrs),
        "adrs_without_mission_links": {"count": len(adrs_without_mission_links), "files": [Path(r).name for r in adrs_without_mission_links]},
        "adrs_without_adr_links": {"count": len(adrs_without_adr_links), "files": [Path(r).name for r in adrs_without_adr_links]},
        "missions_total": len(missions),
        "missions_without_adr_links": {"count": len(missions_without_adr_links)},
        "moc_files": {"count": len(moc_files), "files": [Path(r).name for r in moc_files]},
        "top20_most_connected": [{"file": Path(r).name, "score": s} for r, s in top20_connected],
        "top20_orphan_low_value": [{"file": Path(r).name, "score": s} for r, s in bottom20],
        "yaml_field_coverage": yaml_field_stats,
        "orphan_file_list": [Path(r).name for r in orphans[:50]],
        "unknown_file_list": [Path(r).name for r in unknowns[:30]],
    }

    # Save metrics JSON
    metrics_path = OUT_DIR / "graph_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print("MISSION-013B — Graph Quality Audit")
    print(f"{'='*60}")
    print(f"Total files:          {total}")
    print(f"Frontmatter:          {with_fm}/{total} ({round(with_fm/total*100,1)}%)")
    print(f"Avg FM fields:        {avg_fm_fields}")
    print(f"With tags:            {with_tags} ({round(with_tags/total*100,1)}%)")
    print(f"With aliases:         {with_aliases} ({round(with_aliases/total*100,1)}%)")
    print(f"Total wikilinks:      {total_wikilinks_out}")
    print(f"Files with outlinks:  {files_with_outlinks} ({round(files_with_outlinks/total*100,1)}%)")
    print(f"Files with inlinks:   {files_with_inlinks} ({round(files_with_inlinks/total*100,1)}%)")
    print(f"Orphan files:         {len(orphans)} ({round(len(orphans)/total*100,1)}%)")
    print(f"No inbound:           {len(no_inbound)} ({round(len(no_inbound)/total*100,1)}%)")
    print(f"No outbound:          {len(no_outbound)} ({round(len(no_outbound)/total*100,1)}%)")
    print(f"Unknown type:         {len(unknowns)} ({round(len(unknowns)/total*100,1)}%)")
    print(f"ADRs total:           {len(adrs)}")
    print(f"ADRs w/o mission:     {len(adrs_without_mission_links)}")
    print(f"ADRs w/o ADR links:   {len(adrs_without_adr_links)}")
    print(f"Missions total:       {len(missions)}")
    print(f"Missions w/o ADR:     {len(missions_without_adr_links)}")
    print(f"MOC files:            {len(moc_files)}")
    print(f"\nTop 10 most connected:")
    for item in top20_connected[:10]:
        print(f"  {item[1]:3d}  {item[0]}")
    print(f"\nTop 10 orphans/low-value:")
    for item in bottom20[:10]:
        print(f"  {item[1]:3d}  {item[0]}")
    print(f"\nFiles by type:")
    for t, c in type_counts.most_common():
        print(f"  {c:4d}  {t}")

    print(f"\nMetrics saved: {metrics_path}")
    return metrics, data

if __name__ == "__main__":
    run_audit()
