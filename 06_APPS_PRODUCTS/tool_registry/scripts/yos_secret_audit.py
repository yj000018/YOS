#!/usr/bin/env python3
"""
Y-OS Secret Audit — yos_secret_audit.py
========================================
Vérifie la cohérence entre 1Password (SSOT) et les miroirs locaux.

Pour chaque système (Manus, futur: JGPT, n8n, etc.) :
  - Compare les secrets attendus (1P) vs présents (miroir)
  - Identifie : PRESENT, MISSING, EXTRA, STALE (si date disponible)
  - Génère un rapport de santé avec score de couverture

Usage:
  python3 yos_secret_audit.py [--system manus] [--verbose]
"""

import json
import subprocess
import sys
import os
import re
import argparse
from datetime import datetime
from pathlib import Path

# Import du mapping depuis le script de sync
sys.path.insert(0, "/home/ubuntu")
try:
    from sync_1p_to_manus import (
        fetch_1p_items, fetch_1p_item_detail, extract_credential,
        get_item_tags, match_connector_def, VAULT, TARGET_TAGS, CONNECTOR_MAP
    )
except ImportError:
    print("ERROR: Cannot import sync_1p_to_manus.py — ensure it exists in /home/ubuntu/")
    sys.exit(1)

AUDIT_REPORT_FILE = "/home/ubuntu/yos_secret_audit_report.json"

# ─── MANUS AUDIT ──────────────────────────────────────────────────────────────

def audit_manus() -> dict:
    """Audite les connectors Manus vs 1Password."""
    results = {}

    # 1. Récupérer l'état attendu depuis 1Password
    print("  Fetching 1Password items...", flush=True)
    items = fetch_1p_items()
    expected = {}  # connector_name → {env_var, has_credential, tags, title}
    
    for item in items:
        try:
            detail = fetch_1p_item_detail(item["id"])
            credential = extract_credential(detail.get("fields", []))
            tags = get_item_tags(detail)
            env_override = ""
            for f in detail.get("fields", []):
                if f.get("label", "").lower() in ["yos-env-var", "manus secret name"]:
                    env_override = f.get("value", "")
                    break
            
            mapping = match_connector_def(item["title"], env_override)
            if not mapping:
                continue
                
            cname = mapping["name"]
            if cname not in expected:
                expected[cname] = {
                    "connector_name": cname,
                    "env_var": env_override or mapping["env"],
                    "has_credential": bool(credential),
                    "tags": tags,
                    "1p_title": item["title"],
                    "1p_id": item["id"],
                    "updated_at": item.get("updated_at", ""),
                }
        except Exception as e:
            print(f"  Warning: Error processing {item['title']}: {e}")

    print(f"  → {len(expected)} expected connectors from 1Password")

    # 2. Récupérer l'état actuel du miroir Manus
    print("  Fetching Manus connectors...", flush=True)
    r = subprocess.run(["manus-config", "connector", "list"],
                       capture_output=True, text=True, timeout=10)
    
    manus_actual = {}  # connector_name → {uid, kind, enabled, editable}
    for line in r.stdout.splitlines():
        parts = [p.strip() for p in line.split("  ") if p.strip()]
        if len(parts) >= 2:
            uid = parts[0]
            name = parts[1]
            kind = parts[2] if len(parts) > 2 else ""
            enabled = "enabled" in line
            editable = "editable" in line
            manus_actual[name.lower()] = {
                "uid": uid, "name": name, "kind": kind,
                "enabled": enabled, "editable": editable
            }

    print(f"  → {len(manus_actual)} connectors in Manus mirror")

    # 3. Comparer
    comparison = []
    
    for cname, exp in expected.items():
        cname_lower = cname.lower()
        actual = manus_actual.get(cname_lower)
        
        if actual:
            status = "PRESENT"
            if not actual.get("enabled"):
                status = "PRESENT_DISABLED"
        else:
            status = "MISSING"
            
        comparison.append({
            "connector": cname,
            "env_var": exp["env_var"],
            "1p_title": exp["1p_title"],
            "1p_has_credential": exp["has_credential"],
            "1p_tags": exp["tags"],
            "manus_status": status,
            "manus_uid": actual.get("uid", "") if actual else "",
            "manus_enabled": actual.get("enabled", False) if actual else False,
            "manus_editable": actual.get("editable", False) if actual else False,
        })

    # Items dans Manus mais pas dans 1P (EXTRA)
    expected_names_lower = {k.lower() for k in expected.keys()}
    for mname_lower, actual in manus_actual.items():
        if mname_lower not in expected_names_lower and actual.get("editable"):
            comparison.append({
                "connector": actual["name"],
                "env_var": "",
                "1p_title": "",
                "1p_has_credential": False,
                "1p_tags": [],
                "manus_status": "EXTRA_IN_MANUS",
                "manus_uid": actual["uid"],
                "manus_enabled": actual["enabled"],
                "manus_editable": actual["editable"],
            })

    # 4. Calculer les métriques
    total = len([c for c in comparison if c["manus_status"] != "EXTRA_IN_MANUS"])
    present = len([c for c in comparison if c["manus_status"] in ["PRESENT", "PRESENT_DISABLED"]])
    missing = len([c for c in comparison if c["manus_status"] == "MISSING"])
    disabled = len([c for c in comparison if c["manus_status"] == "PRESENT_DISABLED"])
    extra = len([c for c in comparison if c["manus_status"] == "EXTRA_IN_MANUS"])
    coverage = round(present / total * 100, 1) if total > 0 else 0

    return {
        "system": "manus",
        "total_expected": total,
        "present": present,
        "missing": missing,
        "disabled": disabled,
        "extra_in_mirror": extra,
        "coverage_pct": coverage,
        "health": "HEALTHY" if coverage >= 90 else ("WARNING" if coverage >= 70 else "CRITICAL"),
        "comparison": comparison,
    }


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Y-OS Secret Audit")
    parser.add_argument("--system", default="manus", choices=["manus", "all"],
                        help="System to audit (default: manus)")
    parser.add_argument("--verbose", action="store_true", help="Show all items")
    args = parser.parse_args()

    print("=" * 65)
    print("Y-OS SECRET AUDIT")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 65)

    audit_results = {}

    if args.system in ["manus", "all"]:
        print("\n[MANUS] Auditing Manus mirror...")
        result = audit_manus()
        audit_results["manus"] = result

        # Afficher le résumé
        print(f"\n  {'─'*50}")
        health_icon = "✅" if result["health"] == "HEALTHY" else ("⚠️" if result["health"] == "WARNING" else "🚨")
        print(f"  {health_icon} MANUS MIRROR — {result['health']}")
        print(f"  Coverage : {result['coverage_pct']}% ({result['present']}/{result['total_expected']})")
        print(f"  Present  : {result['present']}")
        print(f"  Missing  : {result['missing']}")
        print(f"  Disabled : {result['disabled']}")
        print(f"  Extra    : {result['extra_in_mirror']}")
        print(f"  {'─'*50}")

        # Afficher les MISSING en priorité
        missing_items = [c for c in result["comparison"] if c["manus_status"] == "MISSING"]
        if missing_items:
            print(f"\n  🔴 MISSING ({len(missing_items)}) — Run sync to fix:")
            for c in missing_items:
                print(f"    - {c['connector']} ({c['env_var']}) ← 1P: '{c['1p_title']}'")

        disabled_items = [c for c in result["comparison"] if c["manus_status"] == "PRESENT_DISABLED"]
        if disabled_items:
            print(f"\n  🟡 DISABLED ({len(disabled_items)}):")
            for c in disabled_items:
                print(f"    - {c['connector']} (uid: {c['manus_uid'][:8]}...)")

        if args.verbose:
            print(f"\n  ✅ PRESENT ({result['present']}):")
            for c in result["comparison"]:
                if c["manus_status"] == "PRESENT":
                    print(f"    - {c['connector']} ({c['env_var']})")

    # Sauvegarder le rapport
    report = {
        "timestamp": datetime.now().isoformat(),
        "systems": audit_results,
    }
    with open(AUDIT_REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved: {AUDIT_REPORT_FILE}")
    print("=" * 65)

    # Exit code basé sur la santé
    all_healthy = all(r.get("health") == "HEALTHY" for r in audit_results.values())
    return 0 if all_healthy else 1


if __name__ == "__main__":
    sys.exit(main())
