#!/usr/bin/env python3
"""
yOS MPM — Local CLI Tool
Canonical runtime: yj000018/YOS @ main / 01_BACKBONE/MPM/
Usage: python 01_BACKBONE/MPM/08_TOOLS/mpm.py <command> [options]

Commands:
  queue                          Show ready queue + queue condition
  latest-report                  Show latest MPR pointer
  validate                       Validate MPM structure integrity
  run-next --dry-run             Show what would run (no execution)
  reconcile-ledger --dry-run     Show ledger inconsistencies
  reconcile-ledger --apply       Apply safe metadata patches
  write-latest-report --mp-id    Update latest-mpr.json pointer
  finalize-run --mp-id --status  Update ledger after execution

Design: Python 3 stdlib only. No arbitrary code execution from MP content.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# ─── Paths (relative to repo root) ───────────────────────────────────────────
MPM_ROOT = Path("01_BACKBONE/MPM")
QUEUE_READY = MPM_ROOT / "04_QUEUE" / "ready"
QUEUE_EXECUTED = MPM_ROOT / "04_QUEUE" / "executed"
LEDGER_JSON = MPM_ROOT / "05_LEDGER" / "mp-ledger.json"
LATEST_MPR_JSON = MPM_ROOT / "06_REPORTS" / "indexes" / "latest-mpr.json"
LATEST_MPR_MD = MPM_ROOT / "06_REPORTS" / "indexes" / "latest-mpr.md"
LATEST_EXEC_JSON = MPM_ROOT / "05_LEDGER" / "latest-executed-mp.json"
MPR_INDEX_JSON = MPM_ROOT / "06_REPORTS" / "indexes" / "mpr-index.json"

RISK_FLAGS = [
    "source_mutation", "github_push", "gdrive_mutation", "icloud_mutation",
    "merge_execution", "canonicalization_execution", "destructive_deduplication",
    "broad_scan", "ludivine_content_access", "notion_body_block_export",
    "unclear_authorization", "unclear_target"
]


def _repo_root():
    """Find repo root by walking up from CWD."""
    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        if (p / ".git").exists():
            return p
    return cwd


def _load_json(path: Path):
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def _parse_frontmatter(md_path: Path) -> dict:
    """Parse YAML-style frontmatter from a Markdown file (stdlib only)."""
    meta = {}
    try:
        text = md_path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return meta
        end = text.find("---", 3)
        if end == -1:
            return meta
        fm = text[3:end].strip()
        for line in fm.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return meta


def _scan_ready_queue(root: Path) -> list:
    """Scan ready/*.md and return list of MP metadata dicts."""
    ready_dir = root / QUEUE_READY
    packets = []
    if not ready_dir.exists():
        return packets
    for f in sorted(ready_dir.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        meta = _parse_frontmatter(f)
        if not meta.get("mp_id"):
            meta["mp_id"] = f.stem
        meta["_physical_path"] = str(f.relative_to(root))
        packets.append(meta)
    return packets


def _load_ledger_ready(root: Path) -> list:
    """Load ledger entries with status ready_for_execution."""
    ledger = _load_json(root / LEDGER_JSON)
    if not ledger:
        return []
    return [e for e in ledger.get("entries", []) if e.get("status") == "ready_for_execution"]


def _resolve_queue(root: Path) -> dict:
    """
    Resolve queue condition.
    Priority: physical ready/*.md > ledger ready entries.
    Returns dict with queue_condition, ready_mps, selected_mp.
    """
    physical = _scan_ready_queue(root)
    ledger_ready = _load_ledger_ready(root)

    # Merge by mp_id, physical takes precedence
    seen = {}
    for p in physical:
        seen[p["mp_id"]] = p
    for l in ledger_ready:
        if l["mp_id"] not in seen:
            l["_source"] = "ledger_only"
            seen[l["mp_id"]] = l

    all_ready = list(seen.values())

    if len(all_ready) == 0:
        condition = "none"
        selected = None
    elif len(all_ready) == 1:
        mp = all_ready[0]
        flags = mp.get("risk_flags", [])
        if isinstance(flags, str):
            flags = [f.strip() for f in flags.strip("[]").split(",") if f.strip()]
        if not flags:
            condition = "exactly_one_ready"
        else:
            condition = "risk_flagged"
        selected = mp
    else:
        condition = "multiple_ready"
        selected = None

    return {
        "queue_condition": condition,
        "ready_count": len(all_ready),
        "ready_mps": all_ready,
        "selected_mp": selected
    }


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_queue(root: Path, args):
    """Show ready queue and queue condition."""
    q = _resolve_queue(root)
    print(f"\n{'='*60}")
    print(f"  yOS MPM — Queue Status")
    print(f"  Runtime: yj000018/YOS @ main / 01_BACKBONE/MPM/")
    print(f"{'='*60}")
    print(f"  Queue condition:  {q['queue_condition'].upper()}")
    print(f"  Ready MPs:        {q['ready_count']}")

    if q["ready_mps"]:
        print()
        for mp in q["ready_mps"]:
            flags = mp.get("risk_flags", [])
            src = mp.get("_source", "physical_ready_dir")
            print(f"  [{mp['mp_id']}]")
            print(f"    title:      {mp.get('title', '(no title)')}")
            print(f"    mode:       {mp.get('mode', '?')}")
            print(f"    risk_flags: {flags if flags else 'none'}")
            print(f"    source:     {src}")
            print(f"    path:       {mp.get('_physical_path', mp.get('canonical_mp_path', '?'))}")
    else:
        print()
        print("  No ready MPs found.")
        print("  Use `MP queue` to inspect or `MP` to check for auto-run.")

    if q["queue_condition"] == "exactly_one_ready":
        print()
        print(f"  AUTO-RUN ELIGIBLE: YES")
        print(f"  Selected: {q['selected_mp']['mp_id']}")
    elif q["queue_condition"] == "multiple_ready":
        print()
        print("  MICRO-MENU REQUIRED: multiple ready MPs — select manually.")
    elif q["queue_condition"] == "risk_flagged":
        print()
        print("  MICRO-MENU REQUIRED: risk flags detected.")
    print()


def cmd_latest_report(root: Path, args):
    """Show latest MPR pointer."""
    ptr = _load_json(root / LATEST_MPR_JSON)
    if not ptr:
        print("\n  No latest-mpr.json found.")
        print(f"  Expected: {LATEST_MPR_JSON}\n")
        return
    print(f"\n{'='*60}")
    print(f"  yOS MPM — Latest MPR")
    print(f"{'='*60}")
    for k, v in ptr.items():
        if not k.startswith("$"):
            print(f"  {k}: {v}")
    print()


def cmd_validate(root: Path, args):
    """Validate MPM structure integrity."""
    print(f"\n{'='*60}")
    print(f"  yOS MPM — Validate")
    print(f"{'='*60}")

    issues = []
    warnings = []

    # Required paths
    required = [
        MPM_ROOT / "04_QUEUE" / "ready",
        MPM_ROOT / "04_QUEUE" / "executed",
        LEDGER_JSON,
        MPM_ROOT / "06_REPORTS" / "awaiting-review",
        MPM_ROOT / "06_REPORTS" / "indexes",
        MPM_ROOT / "00_PROTOCOLS",
        MPM_ROOT / "08_TOOLS" / "mpm.py",
    ]
    for p in required:
        full = root / p
        status = "OK" if full.exists() else "MISSING"
        if status == "MISSING":
            issues.append(f"MISSING: {p}")
        print(f"  {status:8} {p}")

    # Ledger check
    ledger = _load_json(root / LEDGER_JSON)
    if ledger:
        entries = ledger.get("entries", [])
        stale_running = [e for e in entries if e.get("status") == "running"]
        if stale_running:
            for e in stale_running:
                warnings.append(f"STALE_RUNNING: {e['mp_id']} — status=running but may be completed")

    # Latest pointers
    for ptr_path in [LATEST_MPR_JSON, LATEST_EXEC_JSON]:
        full = root / ptr_path
        if not full.exists():
            warnings.append(f"MISSING_POINTER: {ptr_path}")

    print()
    if issues:
        print(f"  STATUS: FAIL ({len(issues)} issue(s))")
        for i in issues:
            print(f"    ERROR: {i}")
    elif warnings:
        print(f"  STATUS: PASS_WITH_WARNINGS ({len(warnings)} warning(s))")
        for w in warnings:
            print(f"    WARN: {w}")
    else:
        print("  STATUS: PASS")
    print()


def cmd_run_next_dry_run(root: Path, args):
    """Show what would run — no execution."""
    q = _resolve_queue(root)
    print(f"\n{'='*60}")
    print(f"  yOS MPM — run-next --dry-run")
    print(f"{'='*60}")
    print(f"  Runtime resolved:  yj000018/YOS @ main / 01_BACKBONE/MPM/")
    print(f"  Ready MP count:    {q['ready_count']}")
    print(f"  Queue condition:   {q['queue_condition'].upper()}")

    if q["queue_condition"] == "exactly_one_ready":
        mp = q["selected_mp"]
        flags = mp.get("risk_flags", [])
        print(f"  Selected mp_id:    {mp['mp_id']}")
        print(f"  Risk flags:        {flags if flags else 'none'}")
        print(f"  Canonical path:    {mp.get('_physical_path', mp.get('canonical_mp_path', '?'))}")
        print(f"  Expected MPR path: {mp.get('canonical_mpr_path', mp.get('expected_mpr_path', '?'))}")
        print()
        print("  ACTION: Would auto-run this MP (no micro-menu).")
        print("  NOTE:   This is --dry-run. No execution performed.")
    elif q["queue_condition"] == "none":
        print()
        print("  No ready MP found. Nothing to run.")
    elif q["queue_condition"] == "multiple_ready":
        print()
        print("  Multiple ready MPs — micro-menu required. Use `MP queue` to select.")
    elif q["queue_condition"] == "risk_flagged":
        mp = q["selected_mp"]
        print(f"  Selected mp_id:    {mp['mp_id']}")
        print(f"  Risk flags:        {mp.get('risk_flags', [])}")
        print()
        print("  BLOCKED: risk flags detected. Clarification required.")
    print()


def cmd_reconcile_ledger(root: Path, args):
    """Reconcile ledger metadata safely."""
    apply = getattr(args, "apply", False)
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"\n{'='*60}")
    print(f"  yOS MPM — reconcile-ledger ({mode})")
    print(f"{'='*60}")

    ledger = _load_json(root / LEDGER_JSON)
    if not ledger:
        print("  ERROR: ledger not found.")
        return

    patches = []
    executed_dir = root / QUEUE_EXECUTED

    for e in ledger.get("entries", []):
        mp_id = e.get("mp_id", "")
        status = e.get("status", "")
        path = e.get("canonical_mp_path", "")

        # Check: executed status but path still points to ready/
        if status in ("executed_awaiting_architect_guardian_review",
                      "executed_awaiting_guardian_review") and "ready/" in path:
            executed_file = executed_dir / f"{mp_id}.md"
            if executed_file.exists():
                new_path = str(executed_file.relative_to(root))
                patches.append({
                    "mp_id": mp_id,
                    "field": "canonical_mp_path",
                    "old": path,
                    "new": new_path,
                    "reason": "packet found in executed/ — path updated"
                })
            else:
                print(f"  WARN: {mp_id} — status={status} but not found in executed/ (skip)")

        # Check: stale running
        if status == "running":
            patches.append({
                "mp_id": mp_id,
                "field": "status",
                "old": status,
                "new": "MANUAL_REVIEW_REQUIRED",
                "reason": "stale running entry — requires manual review"
            })

    if not patches:
        print("  No inconsistencies found. Ledger is clean.")
        print()
        return

    print(f"  Found {len(patches)} patch(es):")
    for p in patches:
        print(f"\n  [{p['mp_id']}]")
        print(f"    field:  {p['field']}")
        print(f"    old:    {p['old']}")
        print(f"    new:    {p['new']}")
        print(f"    reason: {p['reason']}")

    if apply:
        # Apply only safe patches (not MANUAL_REVIEW_REQUIRED)
        applied = 0
        for p in patches:
            if p["new"] == "MANUAL_REVIEW_REQUIRED":
                print(f"\n  SKIP (manual review required): {p['mp_id']}")
                continue
            for e in ledger["entries"]:
                if e.get("mp_id") == p["mp_id"]:
                    e[p["field"]] = p["new"]
                    applied += 1
        if applied:
            ledger["last_updated"] = datetime.now(timezone.utc).isoformat()
            _save_json(root / LEDGER_JSON, ledger)
            print(f"\n  Applied {applied} safe patch(es). Ledger saved.")
        else:
            print("\n  No safe patches to apply.")
    else:
        print(f"\n  DRY-RUN only. Use --apply to apply safe patches.")
    print()


def cmd_write_latest_report(root: Path, args):
    """Update latest-mpr.json pointer for a given mp_id."""
    mp_id = args.mp_id
    ledger = _load_json(root / LEDGER_JSON)
    if not ledger:
        print("ERROR: ledger not found.")
        return

    entry = next((e for e in ledger.get("entries", []) if e.get("mp_id") == mp_id), None)
    if not entry:
        print(f"ERROR: mp_id {mp_id} not found in ledger.")
        return

    mpr_path = entry.get("expected_mpr_path", entry.get("canonical_mpr_path", ""))
    log_ptr = entry.get("log_pointer_path", "")
    commit = entry.get("commit", "pending_execution")

    ptr = {
        "$schema": "yos-mpm-latest-mpr-v1.0.0",
        "latest_mp_id": mp_id,
        "latest_mpr_id": f"{mp_id}-REPORT",
        "latest_status": entry.get("status", "unknown"),
        "latest_mpr_path": mpr_path,
        "latest_log_pointer_path": log_ptr,
        "branch": "main",
        "commit": commit,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    _save_json(root / LATEST_MPR_JSON, ptr)

    # Regenerate MD view
    md = f"# Latest MPR\n\n> **JSON source of truth:** `{LATEST_MPR_JSON}`\n> Do not edit this file directly.\n\n"
    md += "| Field | Value |\n| :--- | :--- |\n"
    for k, v in ptr.items():
        if not k.startswith("$"):
            md += f"| `{k}` | `{v}` |\n"
    (root / LATEST_MPR_MD).write_text(md)

    print(f"  latest-mpr.json updated → {mp_id}")
    print(f"  latest-mpr.md regenerated")


def cmd_finalize_run(root: Path, args):
    """Update ledger status after execution."""
    mp_id = args.mp_id
    status = args.status

    allowed_statuses = [
        "executed_awaiting_architect_guardian_review",
        "executed_awaiting_guardian_review",
        "guardian_accepted",
        "blocked",
        "superseded"
    ]
    if status not in allowed_statuses:
        print(f"ERROR: status must be one of: {allowed_statuses}")
        return

    ledger = _load_json(root / LEDGER_JSON)
    if not ledger:
        print("ERROR: ledger not found.")
        return

    found = False
    for e in ledger["entries"]:
        if e.get("mp_id") == mp_id:
            e["status"] = status
            found = True
            break

    if not found:
        print(f"ERROR: mp_id {mp_id} not found in ledger.")
        return

    ledger["last_updated"] = datetime.now(timezone.utc).isoformat()
    _save_json(root / LEDGER_JSON, ledger)
    print(f"  Ledger updated: {mp_id} → {status}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="yOS MPM — Local CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("queue", help="Show ready queue + queue condition")
    subparsers.add_parser("latest-report", help="Show latest MPR pointer")
    subparsers.add_parser("validate", help="Validate MPM structure integrity")

    p_run = subparsers.add_parser("run-next", help="Show what would run (dry-run only)")
    p_run.add_argument("--dry-run", action="store_true", required=True)

    p_rec = subparsers.add_parser("reconcile-ledger", help="Reconcile ledger metadata")
    p_rec_group = p_rec.add_mutually_exclusive_group(required=True)
    p_rec_group.add_argument("--dry-run", action="store_true")
    p_rec_group.add_argument("--apply", action="store_true")

    p_wlr = subparsers.add_parser("write-latest-report", help="Update latest-mpr.json pointer")
    p_wlr.add_argument("--mp-id", required=True)

    p_fin = subparsers.add_parser("finalize-run", help="Update ledger after execution")
    p_fin.add_argument("--mp-id", required=True)
    p_fin.add_argument("--status", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    root = _repo_root()
    os.chdir(root)

    dispatch = {
        "queue": cmd_queue,
        "latest-report": cmd_latest_report,
        "validate": cmd_validate,
        "run-next": cmd_run_next_dry_run,
        "reconcile-ledger": cmd_reconcile_ledger,
        "write-latest-report": cmd_write_latest_report,
        "finalize-run": cmd_finalize_run,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(root, args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
