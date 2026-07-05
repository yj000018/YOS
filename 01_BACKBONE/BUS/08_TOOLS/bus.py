#!/usr/bin/env python3
"""
bus.py — YOS BUS CLI Tool
Version: 1.1.0
Requirements: Python 3 stdlib only — no external dependencies.
Usage: python 01_BACKBONE/BUS/08_TOOLS/bus.py <command> [options]

Commands:
  status                    Show BUS status and configuration
  domains                   List all registered BUS domains
  inbox --domain <domain>   List inbox contents for a domain
  claim --domain <domain> --dry-run   Show what would be claimed
  claim --domain <domain> --apply     Claim one file from inbox to workspace
  validate                  Validate BUS structure
  runtime-paths             Show runtime paths
  init-runtime --root <path>  Initialize a new runtime root
  outbox --domain <domain>  List outbox contents for a domain

  [v1.1.0 — First/Last Mile Integration]
  ingest --domain <domain> --file <path>   Ingest a local file into BUS inbox
  write --domain <domain> --file <path> [--backend <backend>]  Write packet to BUS backend
  latest-report             Show latest MPR pointer (fixed path, no search)
  report-pointer --domain <domain>  Emit BUS-friendly report pointer for a domain
  entry-backends            List entry backend registry
  report-backends           List report backend registry
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

VERSION = "1.1.0"
DOMAINS = ["general", "mpm", "kap", "casatao", "kosmos", "yworld"]
LIFECYCLE_STAGES = ["inbox", "workspace", "outbox", "archive"]
RUNTIME_ENV_VAR = "YOS_BUS_RUNTIME_ROOT"
ENTRY_BACKEND_ENV_VAR = "YOS_BUS_ENTRY_BACKEND"
REPORT_BACKEND_ENV_VAR = "YOS_BUS_REPORT_BACKEND"

# Locate the BUS canonical path (relative to this script)
SCRIPT_DIR = Path(__file__).parent.resolve()
BUS_ROOT = SCRIPT_DIR.parent  # 01_BACKBONE/BUS/
RUNTIME_REGISTRY_PATH = BUS_ROOT / "05_RUNTIME" / "runtime-registry.json"
ENTRY_BACKEND_REGISTRY_PATH = BUS_ROOT / "05_RUNTIME" / "entry-backend-registry.json"
REPORT_BACKEND_REGISTRY_PATH = BUS_ROOT / "05_RUNTIME" / "report-backend-registry.json"
BUS_MANIFEST_PATH = BUS_ROOT / "bus_manifest.yaml"
DOMAINS_PATH = BUS_ROOT / "04_DOMAINS"
LATEST_ENTRY_EVENT_PATH = BUS_ROOT / "06_INDEXES" / "latest-entry-event.json"
LATEST_REPORT_EVENT_PATH = BUS_ROOT / "06_INDEXES" / "latest-report-event.json"

# MPM canonical paths (relative to repo root)
REPO_ROOT = BUS_ROOT.parent.parent  # yos-monorepo/
LATEST_MPR_JSON_PATH = REPO_ROOT / "01_BACKBONE" / "MPM" / "06_REPORTS" / "indexes" / "latest-mpr.json"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_path(base: Path, *parts: str) -> Path:
    """Resolve a path safely, preventing traversal outside base."""
    resolved = (base / Path(*parts)).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise ValueError(f"Path traversal detected: {resolved}")
    return resolved


def get_runtime_root() -> Path | None:
    """Return the configured runtime root or None."""
    val = os.environ.get(RUNTIME_ENV_VAR)
    if val:
        p = Path(val)
        if p.exists() and p.is_dir():
            return p
    return None


def load_runtime_registry() -> dict:
    """Load runtime-registry.json."""
    if RUNTIME_REGISTRY_PATH.exists():
        with open(RUNTIME_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_entry_backend_registry() -> dict:
    """Load entry-backend-registry.json."""
    if ENTRY_BACKEND_REGISTRY_PATH.exists():
        with open(ENTRY_BACKEND_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_report_backend_registry() -> dict:
    """Load report-backend-registry.json."""
    if REPORT_BACKEND_REGISTRY_PATH.exists():
        with open(REPORT_BACKEND_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def list_files_in(path: Path) -> list[str]:
    """List non-hidden files in a directory."""
    if not path.exists():
        return []
    return sorted([
        f.name for f in path.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ])


def write_entry_event(domain: str, backend: str, packet_id: str, status: str) -> None:
    """Update latest-entry-event.json."""
    event = {
        "$schema": "yos-bus-latest-entry-event-v1.0.0",
        "event_id": f"BUS-ENTRY-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        "event_type": "ingest",
        "domain": domain,
        "status": status,
        "backend_used": backend,
        "packet_id": packet_id,
        "updated_at": now_iso()
    }
    try:
        with open(LATEST_ENTRY_EVENT_PATH, "w", encoding="utf-8") as f:
            json.dump(event, f, indent=2)
    except Exception:
        pass  # Non-fatal


def write_report_event(domain: str, backend: str, mpr_path: str) -> None:
    """Update latest-report-event.json."""
    event = {
        "$schema": "yos-bus-latest-report-event-v1.0.0",
        "event_id": f"BUS-REPORT-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        "event_type": "latest_report_read",
        "domain": domain,
        "status": "read",
        "backend_used": backend,
        "latest_mpr_path": mpr_path,
        "updated_at": now_iso()
    }
    try:
        with open(LATEST_REPORT_EVENT_PATH, "w", encoding="utf-8") as f:
            json.dump(event, f, indent=2)
    except Exception:
        pass  # Non-fatal


# ─────────────────────────────────────────────────────────────────────────────
# Commands (original)
# ─────────────────────────────────────────────────────────────────────────────

def cmd_status(args) -> int:
    """Show BUS status and configuration."""
    runtime_root = get_runtime_root()
    registry = load_runtime_registry()

    print("=" * 60)
    print(f"YOS BUS — Status")
    print(f"Version:         {VERSION}")
    print(f"BUS Root:        {BUS_ROOT}")
    print(f"Manifest:        {'OK' if BUS_MANIFEST_PATH.exists() else 'MISSING'}")
    print(f"Runtime Registry: {'OK' if RUNTIME_REGISTRY_PATH.exists() else 'MISSING'}")
    print(f"Domains Path:    {DOMAINS_PATH}")
    print()
    print(f"Runtime Root Env ({RUNTIME_ENV_VAR}):")
    if runtime_root:
        print(f"  Configured: {runtime_root}")
        print(f"  Status:     accessible")
        active_backend = "direct_file"
    else:
        env_val = os.environ.get(RUNTIME_ENV_VAR)
        if env_val:
            print(f"  Configured: {env_val}")
            print(f"  Status:     NOT ACCESSIBLE (path does not exist)")
        else:
            print(f"  Not configured.")
        active_backend = "git (fallback)"
    print()
    print(f"Active Backend:  {active_backend}")
    print()
    if registry:
        priority = registry.get("backend_priority", [])
        print(f"Backend Priority: {' -> '.join(priority)}")
    print("=" * 60)
    return 0


def cmd_domains(args) -> int:
    """List all registered BUS domains."""
    registry = load_runtime_registry()
    domains = registry.get("domains", DOMAINS)

    print("=" * 60)
    print("YOS BUS — Domains")
    print()
    for domain in domains:
        domain_path = DOMAINS_PATH / domain
        git_exists = domain_path.exists()
        runtime_root = get_runtime_root()
        runtime_exists = False
        if runtime_root:
            runtime_exists = (runtime_root / "inbox" / domain).exists()
        print(f"  {domain}")
        print(f"    Git path:     {domain_path} ({'OK' if git_exists else 'MISSING'})")
        if runtime_root:
            print(f"    Runtime path: {runtime_root}/inbox/{domain} ({'OK' if runtime_exists else 'not initialized'})")
    print("=" * 60)
    return 0


def cmd_inbox(args) -> int:
    """List inbox contents for a domain."""
    domain = args.domain
    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    print(f"YOS BUS — Inbox: {domain}")
    print()

    # Check runtime first
    runtime_root = get_runtime_root()
    if runtime_root:
        runtime_inbox = runtime_root / "inbox" / domain
        files = list_files_in(runtime_inbox)
        print(f"[direct_file] {runtime_inbox}")
        if files:
            for f in files:
                print(f"  - {f}")
        else:
            print("  (empty)")
        print()

    # Check Git BUS domain inbox
    git_inbox = DOMAINS_PATH / domain / "inbox"
    git_files = list_files_in(git_inbox)
    print(f"[git fallback] {git_inbox}")
    if git_files:
        for f in git_files:
            print(f"  - {f}")
    else:
        print("  (empty)")

    return 0


def cmd_claim(args) -> int:
    """Claim a packet from domain inbox to workspace."""
    domain = args.domain
    dry_run = getattr(args, "dry_run", True)
    apply = getattr(args, "apply", False)

    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    # Determine source inbox
    runtime_root = get_runtime_root()
    inbox_path = None
    backend_used = None

    if runtime_root:
        runtime_inbox = runtime_root / "inbox" / domain
        if runtime_inbox.exists():
            inbox_path = runtime_inbox
            backend_used = "direct_file"

    if inbox_path is None:
        git_inbox = DOMAINS_PATH / domain / "inbox"
        if git_inbox.exists():
            inbox_path = git_inbox
            backend_used = "git"

    if inbox_path is None:
        print(f"No inbox found for domain '{domain}'.")
        return 0

    files = list_files_in(inbox_path)
    if not files:
        print(f"Inbox '{domain}' is empty. Nothing to claim.")
        return 0

    if len(files) > 1:
        print(f"Multiple candidates in inbox '{domain}' — micro-menu required:")
        for i, f in enumerate(files, 1):
            print(f"  {i}. {f}")
        print("Use manual selection or resolve ambiguity before claiming.")
        return 0

    candidate = files[0]
    src = inbox_path / candidate

    # Determine workspace path
    if backend_used == "direct_file":
        workspace_path = runtime_root / "workspace" / domain
    else:
        workspace_path = DOMAINS_PATH / domain / "workspace"

    dst = workspace_path / candidate

    print(f"YOS BUS — Claim ({backend_used})")
    print(f"  Domain:    {domain}")
    print(f"  Candidate: {candidate}")
    print(f"  From:      {src}")
    print(f"  To:        {dst}")
    print()

    if dry_run and not apply:
        print("[DRY RUN] No files moved. Use --apply to execute.")
        return 0

    if apply:
        workspace_path.mkdir(parents=True, exist_ok=True)
        try:
            src.rename(dst)
            print(f"[CLAIMED] Moved {candidate} to workspace/{domain}/")
        except OSError as e:
            # Fallback: copy + delete (cross-device)
            shutil.copy2(str(src), str(dst))
            src.unlink()
            print(f"[CLAIMED] Moved {candidate} to workspace/{domain}/ (copy+delete)")
        return 0

    print("[DRY RUN] No files moved. Use --apply to execute.")
    return 0


def cmd_validate(args) -> int:
    """Validate BUS structure."""
    errors = []
    warnings = []

    print("YOS BUS — Validate")
    print()

    # Check BUS root
    if not BUS_ROOT.exists():
        errors.append(f"BUS root missing: {BUS_ROOT}")
    else:
        print(f"  [OK] BUS root: {BUS_ROOT}")

    # Check manifest
    if not BUS_MANIFEST_PATH.exists():
        errors.append(f"bus_manifest.yaml missing")
    else:
        print(f"  [OK] bus_manifest.yaml")

    # Check runtime registry
    if not RUNTIME_REGISTRY_PATH.exists():
        errors.append(f"runtime-registry.json missing")
    else:
        print(f"  [OK] runtime-registry.json")

    # Check required folders
    required_folders = [
        "00_PROTOCOLS", "01_SCHEMAS", "02_ADAPTERS", "03_TEMPLATES",
        "04_DOMAINS", "05_RUNTIME", "06_INDEXES", "08_TOOLS", "99_ARCHIVE"
    ]
    for folder in required_folders:
        p = BUS_ROOT / folder
        if not p.exists():
            errors.append(f"Required folder missing: {folder}/")
        else:
            print(f"  [OK] {folder}/")

    # Check domains
    for domain in DOMAINS:
        domain_path = DOMAINS_PATH / domain
        if not domain_path.exists():
            errors.append(f"Domain folder missing: 04_DOMAINS/{domain}/")
        else:
            print(f"  [OK] 04_DOMAINS/{domain}/")

    # Check entry/report backend registries (v1.1.0)
    if ENTRY_BACKEND_REGISTRY_PATH.exists():
        print(f"  [OK] entry-backend-registry.json")
    else:
        warnings.append("entry-backend-registry.json missing — first-mile registry not initialized")

    if REPORT_BACKEND_REGISTRY_PATH.exists():
        print(f"  [OK] report-backend-registry.json")
    else:
        warnings.append("report-backend-registry.json missing — last-mile registry not initialized")

    # Check latest-mpr.json (last-mile fixed path)
    if LATEST_MPR_JSON_PATH.exists():
        print(f"  [OK] latest-mpr.json (last-mile fixed path)")
    else:
        warnings.append(f"latest-mpr.json not found at {LATEST_MPR_JSON_PATH} — last-mile report path unavailable")

    # Check runtime root
    runtime_root = get_runtime_root()
    if runtime_root:
        print(f"  [OK] Runtime root: {runtime_root}")
    else:
        warnings.append(f"{RUNTIME_ENV_VAR} not set or not accessible — will use git fallback")

    print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")
        print()

    if errors:
        print("RESULT: FAIL")
        return 1
    elif warnings:
        print("RESULT: PASS_WITH_WARNINGS")
        return 0
    else:
        print("RESULT: PASS")
        return 0


def cmd_runtime_paths(args) -> int:
    """Show runtime paths."""
    runtime_root = get_runtime_root()
    registry = load_runtime_registry()

    print("YOS BUS — Runtime Paths")
    print()
    print(f"BUS Canonical Root:  {BUS_ROOT}")
    print(f"Runtime Registry:    {RUNTIME_REGISTRY_PATH}")
    print(f"Domains:             {DOMAINS_PATH}")
    print()
    print(f"Runtime Root Env:    {RUNTIME_ENV_VAR}")
    if runtime_root:
        print(f"Runtime Root:        {runtime_root} [accessible]")
        print()
        print("Runtime Structure:")
        for stage in LIFECYCLE_STAGES:
            for domain in DOMAINS:
                p = runtime_root / stage / domain
                status = "exists" if p.exists() else "not initialized"
                print(f"  {runtime_root}/{stage}/{domain}  [{status}]")
    else:
        env_val = os.environ.get(RUNTIME_ENV_VAR)
        if env_val:
            print(f"Runtime Root:        {env_val} [NOT ACCESSIBLE]")
        else:
            print(f"Runtime Root:        not configured")
        print()
        print("Git Fallback Paths:")
        for domain in DOMAINS:
            for stage in LIFECYCLE_STAGES:
                p = DOMAINS_PATH / domain / stage
                status = "exists" if p.exists() else "not initialized"
                print(f"  01_BACKBONE/BUS/04_DOMAINS/{domain}/{stage}/  [{status}]")

    return 0


def cmd_init_runtime(args) -> int:
    """Initialize a new runtime root."""
    root = Path(args.root).resolve()
    print(f"YOS BUS — Init Runtime: {root}")
    print()

    created = []
    for stage in LIFECYCLE_STAGES + ["ack", "locks", "dead-letter"]:
        if stage in ["ack", "locks", "dead-letter"]:
            p = root / stage
            p.mkdir(parents=True, exist_ok=True)
            created.append(str(p))
        else:
            for domain in DOMAINS:
                p = root / stage / domain
                p.mkdir(parents=True, exist_ok=True)
                created.append(str(p))

    print(f"Created {len(created)} directories.")
    print()
    print(f"Set runtime root:")
    print(f"  export {RUNTIME_ENV_VAR}={root}")
    return 0


def cmd_outbox(args) -> int:
    """List outbox contents for a domain."""
    domain = args.domain
    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    print(f"YOS BUS — Outbox: {domain}")
    print()

    runtime_root = get_runtime_root()
    if runtime_root:
        runtime_outbox = runtime_root / "outbox" / domain
        files = list_files_in(runtime_outbox)
        print(f"[direct_file] {runtime_outbox}")
        if files:
            for f in files:
                print(f"  - {f}")
        else:
            print("  (empty)")
        print()

    git_outbox = DOMAINS_PATH / domain / "outbox"
    git_files = list_files_in(git_outbox)
    print(f"[git fallback] {git_outbox}")
    if git_files:
        for f in git_files:
            print(f"  - {f}")
    else:
        print("  (empty)")

    return 0


# ─────────────────────────────────────────────────────────────────────────────
# Commands (v1.1.0 — First/Last Mile Integration)
# ─────────────────────────────────────────────────────────────────────────────

def cmd_ingest(args) -> int:
    """Ingest a local file into BUS inbox/domain (first-mile manual upload bridge)."""
    domain = args.domain
    file_path = Path(args.file)

    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return 1

    if not file_path.is_file():
        print(f"ERROR: Not a file: {file_path}", file=sys.stderr)
        return 1

    print(f"YOS BUS — Ingest")
    print(f"  Domain:  {domain}")
    print(f"  File:    {file_path}")
    print()

    # Try direct_file backend first
    runtime_root = get_runtime_root()
    backend_used = None
    dst = None

    if runtime_root:
        inbox_dir = runtime_root / "inbox" / domain
        inbox_dir.mkdir(parents=True, exist_ok=True)
        dst = inbox_dir / file_path.name
        backend_used = "direct_file"
        print(f"  Backend: direct_file")
        print(f"  Target:  {dst}")
    else:
        # Git fallback
        inbox_dir = DOMAINS_PATH / domain / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        dst = inbox_dir / file_path.name
        backend_used = "git"
        print(f"  Backend: git (fallback — YOS_BUS_RUNTIME_ROOT not set)")
        print(f"  Target:  {dst}")

    try:
        shutil.copy2(str(file_path), str(dst))
        print(f"  Status:  INGESTED")
        print()
        print(f"[INGESTED] {file_path.name} -> {dst}")
        write_entry_event(domain, backend_used, file_path.name, "ingested")
        return 0
    except Exception as e:
        print(f"  Status:  ERROR — {e}", file=sys.stderr)
        write_entry_event(domain, backend_used, file_path.name, f"error: {e}")
        return 1


def cmd_write(args) -> int:
    """Write a packet to BUS backend (programmatic first-mile write)."""
    domain = args.domain
    file_path = Path(args.file)
    backend_override = getattr(args, "backend", None)

    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return 1

    print(f"YOS BUS — Write")
    print(f"  Domain:  {domain}")
    print(f"  File:    {file_path}")

    # Select backend
    env_backend = os.environ.get(ENTRY_BACKEND_ENV_VAR)
    selected_backend = backend_override or env_backend

    runtime_root = get_runtime_root()

    if selected_backend == "git":
        # Force git backend
        inbox_dir = DOMAINS_PATH / domain / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        dst = inbox_dir / file_path.name
        backend_used = "git"
    elif runtime_root and (selected_backend in (None, "direct_file")):
        # direct_file (default if runtime root available)
        inbox_dir = runtime_root / "inbox" / domain
        inbox_dir.mkdir(parents=True, exist_ok=True)
        dst = inbox_dir / file_path.name
        backend_used = "direct_file"
    else:
        # Git fallback
        inbox_dir = DOMAINS_PATH / domain / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        dst = inbox_dir / file_path.name
        backend_used = "git"

    print(f"  Backend: {backend_used}")
    print(f"  Target:  {dst}")
    print()

    try:
        shutil.copy2(str(file_path), str(dst))
        print(f"[WRITTEN] {file_path.name} -> {dst}")
        write_entry_event(domain, backend_used, file_path.name, "written")
        return 0
    except Exception as e:
        print(f"ERROR: Write failed — {e}", file=sys.stderr)
        write_entry_event(domain, backend_used, file_path.name, f"error: {e}")
        return 1


def cmd_latest_report(args) -> int:
    """Show latest MPR pointer using canonical fixed path (no search)."""
    print("YOS BUS — Latest Report")
    print()
    print(f"Fixed path: {LATEST_MPR_JSON_PATH}")
    print()

    if not LATEST_MPR_JSON_PATH.exists():
        print(f"ERROR: latest-mpr.json not found at {LATEST_MPR_JSON_PATH}", file=sys.stderr)
        print("Ensure 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json exists.")
        return 1

    try:
        with open(LATEST_MPR_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read latest-mpr.json — {e}", file=sys.stderr)
        return 1

    latest_mp_id = data.get("latest_mp_id", "unknown")
    latest_mpr_path = data.get("latest_mpr_path", "unknown")
    latest_status = data.get("latest_status", "unknown")
    commit = data.get("commit", "unknown")
    updated_at = data.get("updated_at", "unknown")

    print(f"  latest_mp_id:    {latest_mp_id}")
    print(f"  latest_mpr_path: {latest_mpr_path}")
    print(f"  latest_status:   {latest_status}")
    print(f"  commit:          {commit}")
    print(f"  updated_at:      {updated_at}")
    print()

    # Verify MPR file exists
    mpr_full_path = REPO_ROOT / latest_mpr_path
    if mpr_full_path.exists():
        print(f"  [OK] MPR file exists: {mpr_full_path}")
    else:
        print(f"  [WARN] MPR file not found at: {mpr_full_path}")

    write_report_event("mpm", "latest_mpr_json", latest_mpr_path)
    return 0


def cmd_report_pointer(args) -> int:
    """Emit BUS-friendly report pointer for a domain."""
    domain = args.domain

    if domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{domain}'. Valid: {DOMAINS}", file=sys.stderr)
        return 1

    print(f"YOS BUS — Report Pointer: {domain}")
    print()

    if not LATEST_MPR_JSON_PATH.exists():
        print(f"ERROR: latest-mpr.json not found at {LATEST_MPR_JSON_PATH}", file=sys.stderr)
        return 1

    try:
        with open(LATEST_MPR_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read latest-mpr.json — {e}", file=sys.stderr)
        return 1

    latest_mp_id = data.get("latest_mp_id", "unknown")
    latest_mpr_path = data.get("latest_mpr_path", "unknown")
    latest_status = data.get("latest_status", "unknown")
    commit = data.get("commit", "unknown")
    updated_at = data.get("updated_at", "unknown")

    print(f"MPR_DOMAIN:     {domain}")
    print(f"MPR_MP_ID:      {latest_mp_id}")
    print(f"MPR_PATH:       {latest_mpr_path}")
    print(f"MPR_COMMIT:     {commit}")
    print(f"MPR_STATUS:     {latest_status}")
    print(f"MPR_UPDATED_AT: {updated_at}")
    print(f"MPR_FAST_PATH:  01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json")

    write_report_event(domain, "latest_mpr_json", latest_mpr_path)
    return 0


def cmd_entry_backends(args) -> int:
    """List entry backend registry."""
    print("YOS BUS — Entry Backends")
    print()

    registry = load_entry_backend_registry()
    if not registry:
        print("  [WARN] entry-backend-registry.json not found.")
        return 0

    print(f"  Abstraction: {registry.get('entry_abstraction', 'BUS.write(packet)')}")
    print()
    print(f"  Preferred order:")
    for i, b in enumerate(registry.get("preferred_order", []), 1):
        backends = registry.get("backends", {})
        info = backends.get(b, {})
        status = info.get("status", "unknown")
        print(f"    {i}. {b}  [{status}]")

    env_backend = os.environ.get(ENTRY_BACKEND_ENV_VAR)
    runtime_root = get_runtime_root()
    print()
    print(f"  Active selection:")
    if env_backend:
        print(f"    YOS_BUS_ENTRY_BACKEND={env_backend} (override)")
    elif runtime_root:
        print(f"    direct_file (YOS_BUS_RUNTIME_ROOT={runtime_root})")
    else:
        print(f"    git (fallback — no runtime root configured)")

    return 0


def cmd_report_backends(args) -> int:
    """List report backend registry."""
    print("YOS BUS — Report Backends")
    print()

    registry = load_report_backend_registry()
    if not registry:
        print("  [WARN] report-backend-registry.json not found.")
        return 0

    print(f"  Canonical last mile: {registry.get('canonical_last_mile', 'MPR fast path')}")
    print(f"  Fixed MPR path:      {registry.get('fixed_latest_mpr_path', '')}")
    print()
    print(f"  Preferred order:")
    for i, b in enumerate(registry.get("preferred_order", []), 1):
        print(f"    {i}. {b}")
    print()
    print(f"  Rules:")
    for rule in registry.get("rules", []):
        print(f"    - {rule}")

    return 0


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="bus.py",
        description="YOS BUS CLI v1.1.0 — Universal Transport and Inter-Agent Exchange Layer"
    )
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Show BUS status and configuration")

    # domains
    subparsers.add_parser("domains", help="List all registered BUS domains")

    # inbox
    p_inbox = subparsers.add_parser("inbox", help="List inbox contents for a domain")
    p_inbox.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")

    # claim
    p_claim = subparsers.add_parser("claim", help="Claim a packet from domain inbox")
    p_claim.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")
    p_claim.add_argument("--dry-run", action="store_true", default=False, help="Show what would be claimed (no file moves)")
    p_claim.add_argument("--apply", action="store_true", default=False, help="Execute the claim (move file)")

    # validate
    subparsers.add_parser("validate", help="Validate BUS structure")

    # runtime-paths
    subparsers.add_parser("runtime-paths", help="Show runtime paths")

    # init-runtime
    p_init = subparsers.add_parser("init-runtime", help="Initialize a new runtime root")
    p_init.add_argument("--root", required=True, help="Path to initialize as runtime root")

    # outbox
    p_outbox = subparsers.add_parser("outbox", help="List outbox contents for a domain")
    p_outbox.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")

    # ── v1.1.0 commands ──────────────────────────────────────────────────────

    # ingest (manual upload bridge)
    p_ingest = subparsers.add_parser("ingest", help="Ingest a local file into BUS inbox (first-mile manual bridge)")
    p_ingest.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")
    p_ingest.add_argument("--file", required=True, help="Path to the file to ingest")

    # write (programmatic first-mile write)
    p_write = subparsers.add_parser("write", help="Write a packet to BUS backend (programmatic first-mile)")
    p_write.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")
    p_write.add_argument("--file", required=True, help="Path to the packet file")
    p_write.add_argument("--backend", required=False, default=None,
                         choices=["direct_file", "git", "manus_workspace", "google_drive", "nas", "manual_upload"],
                         help="Override entry backend (default: auto-select)")

    # latest-report (last-mile fixed path)
    subparsers.add_parser("latest-report", help="Show latest MPR pointer (fixed path, no search)")

    # report-pointer (BUS-friendly last-mile pointer)
    p_rp = subparsers.add_parser("report-pointer", help="Emit BUS-friendly report pointer for a domain")
    p_rp.add_argument("--domain", required=True, choices=DOMAINS, help="BUS domain")

    # entry-backends
    subparsers.add_parser("entry-backends", help="List entry backend registry")

    # report-backends
    subparsers.add_parser("report-backends", help="List report backend registry")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    dispatch = {
        "status": cmd_status,
        "domains": cmd_domains,
        "inbox": cmd_inbox,
        "claim": cmd_claim,
        "validate": cmd_validate,
        "runtime-paths": cmd_runtime_paths,
        "init-runtime": cmd_init_runtime,
        "outbox": cmd_outbox,
        # v1.1.0
        "ingest": cmd_ingest,
        "write": cmd_write,
        "latest-report": cmd_latest_report,
        "report-pointer": cmd_report_pointer,
        "entry-backends": cmd_entry_backends,
        "report-backends": cmd_report_backends,
    }

    handler = dispatch.get(args.command)
    if handler is None:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
