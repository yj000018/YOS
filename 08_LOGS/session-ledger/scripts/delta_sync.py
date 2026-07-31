#!/usr/bin/env python3
"""
Y-OS Master Ledger — Delta-Sync Script
Fetches new Manus sessions since the last known session in the Ledger.

Usage: python3 delta_sync.py [--full] [--dry-run]
  --full:    Rebuild the entire Ledger from scratch
  --dry-run: Preview without writing

MIGRATION NOTE (Phase 2 — MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR):
  - Removed hardcoded JWT and client_id (security fix — was exposed in public repo)
  - Replaced custom JSON ledger I/O with yos_memory.SessionLedger (CSV)
  - Credentials now loaded exclusively from environment variables:
      MANUS_JWT_TOKEN   — Bearer token for Manus API
      MANUS_CLIENT_ID   — x-client-id header value
"""
import json
import urllib.request
import time
import sys
import os
import argparse
from pathlib import Path

# ─── yos_memory import ────────────────────────────────────────────────────────
_PIPELINE_DIR = Path(__file__).resolve().parents[4] / "yos-automations" / "scripts" / "yos-llm-pipeline"
if str(_PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(_PIPELINE_DIR))

from yos_memory.ledger import SessionLedger
from yos_memory.ids import generate_global_uid

# ─── Constants ────────────────────────────────────────────────────────────────
URL = "https://api.manus.im/session.v1.SessionService/ListSessions"


# ─── Credentials from environment (NO hardcoded tokens) ──────────────────────
def get_headers() -> dict:
    jwt_token = os.environ.get("MANUS_JWT_TOKEN", "")
    client_id = os.environ.get("MANUS_CLIENT_ID", "")
    if not jwt_token:
        print("ERROR: MANUS_JWT_TOKEN not set. Export it before running.")
        sys.exit(1)
    if not client_id:
        print("ERROR: MANUS_CLIENT_ID not set. Export it before running.")
        sys.exit(1)
    return {
        "accept": "*/*",
        "authorization": f"Bearer {jwt_token}",
        "connect-protocol-version": "1",
        "content-type": "application/json",
        "x-client-id": client_id,
    }


# ─── API calls ────────────────────────────────────────────────────────────────
def fetch_page(offset: int, limit: int = 100) -> dict:
    headers = get_headers()
    payload = {"limit": limit, "offset": offset}
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def session_to_ledger_row(s: dict) -> dict:
    source_id = s.get("uid", "")
    return {
        "Global_UID": generate_global_uid("Manus", source_id) if source_id else "",
        "Source": "Manus",
        "Source_ID": source_id,
        "Title": s.get("title", "Untitled"),
        "Project_ID": s.get("projectUid", ""),
        "Created_At": s.get("createdAt", ""),
        "Updated_At": s.get("updatedAt", ""),
        "Archive_Status": "Pending",
        "Processing_Status": "pending",
        "Archive_Link": "",
        "Topic_Summary": "",
        "Project_Tag": "",
        "Git_Path": "",
        "Content_Hash": "",
        "Mem0_Status": "",
        "Mem0_Memory_IDs": "",
        "Schema_Version": "yos-memory/v1",
        "Last_Processed_At": "",
        "Legacy_Notion_URL": "",
    }


# ─── Sync modes ───────────────────────────────────────────────────────────────
def run_full(ledger: SessionLedger) -> list:
    all_sessions = []
    offset = 0
    page = 1
    while True:
        data = fetch_page(offset)
        sessions = data.get("sessions", [])
        if not sessions:
            break
        all_sessions.extend(sessions)
        print(f"Page {page}: +{len(sessions)} sessions. Total: {len(all_sessions)}")
        if not data.get("hasNext", False):
            break
        offset += 100
        page += 1
        time.sleep(0.5)
    rows = [session_to_ledger_row(s) for s in all_sessions]
    ledger.write_all(rows)
    print(f"\nFull sync complete. {len(rows)} sessions written to ledger.")
    return rows


def run_delta(ledger: SessionLedger) -> list:
    existing_rows = ledger.read_all()
    if not existing_rows:
        print("Ledger empty. Running full sync...")
        return run_full(ledger)
    known_ids = {row["Source_ID"] for row in existing_rows}
    print(f"Ledger has {len(existing_rows)} sessions. Checking for new ones...")
    new_sessions = []
    offset = 0
    stop = False
    while not stop:
        data = fetch_page(offset)
        sessions = data.get("sessions", [])
        if not sessions:
            break
        for s in sessions:
            if s.get("uid") in known_ids:
                stop = True
                break
            new_sessions.append(s)
        if not data.get("hasNext", False):
            break
        offset += 100
        time.sleep(0.3)
    if not new_sessions:
        print("No new sessions found.")
        return []
    print(f"Found {len(new_sessions)} new sessions.")
    new_rows = [session_to_ledger_row(s) for s in new_sessions]
    for row in new_rows:
        ledger.update_session(row["Global_UID"], row)
    print(f"Delta sync complete. {len(new_rows)} new sessions added to ledger.")
    return new_rows


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Y-OS Session Ledger Delta-Sync")
    parser.add_argument("--full", action="store_true", help="Full rebuild from scratch")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    ledger = SessionLedger()
    if args.dry_run:
        print("DRY RUN mode — no writes will occur.")
        data = fetch_page(0, limit=5)
        sessions = data.get("sessions", [])
        print(f"API reachable. First {len(sessions)} sessions:")
        for s in sessions:
            print(f"  [{s.get('uid', '?')}] {s.get('title', 'Untitled')[:70]}")
        return
    if args.full:
        run_full(ledger)
    else:
        run_delta(ledger)


if __name__ == "__main__":
    main()
