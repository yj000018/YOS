#!/usr/bin/env python3
"""
Y-OS Master Ledger — Delta-Sync Script
Fetches new Manus sessions since the last known session in the Ledger.
Usage: python3 delta_sync.py [--full]
  --full: Rebuild the entire Ledger from scratch
"""
import json
import urllib.request
import time
import sys
import os

LEDGER_PATH = os.path.join(os.path.dirname(__file__), 'master_ledger.json')
RAW_PATH = os.path.join(os.path.dirname(__file__), 'manus_raw.json')

URL = "https://api.manus.im/session.v1.SessionService/ListSessions"

# NOTE: Update this JWT when it expires (check expiry in jwt.io — current: 2026-08-26)
HEADERS = {
    "accept": "*/*",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Inlhbm5pY2suam9sbGlldEBnbWFpbC5jb20iLCJleHAiOjE3ODk3NTI1NTUsImlhdCI6MTc4MTk3NjU1NSwianRpIjoiNk1hVWM2UFhQaXNVY3dmRmZTSzZrMyIsIm5hbWUiOiJZYW5uaWNrIEpvbGxpZXQiLCJvcmlnaW5hbF91c2VyX2lkIjoiIiwidGVhbV91aWQiOiIiLCJ0eXBlIjoidXNlciIsInVzZXJfaWQiOiIzMTA0MTk2NjMwMzIzODE4MzMifQ.UtcPUVxrDEARjFrYo50rjcu6VD9Qr48ttSWVW5BusXE",
    "connect-protocol-version": "1",
    "content-type": "application/json",
    "x-client-id": "D9Bd6dANCoqJ4cmPV0cgxX",
}

def fetch_page(offset, limit=100):
    payload = {"limit": limit, "offset": offset}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode('utf-8'), headers=HEADERS, method='POST')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def load_ledger():
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r') as f:
            return json.load(f)
    return []

def save_ledger(ledger):
    with open(LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=2)

def session_to_ledger_row(s):
    return {
        "Global_UID": f"manus_{s.get('uid', '')}",
        "Source": "Manus",
        "Source_ID": s.get('uid', ''),
        "Title": s.get('title', 'Untitled'),
        "Project_ID": s.get('projectUid', ''),
        "Created_At": s.get('createdAt', ''),
        "Updated_At": s.get('updatedAt', ''),
        "Archive_Status": "Pending",
        "Archive_Link": "",
        "Topic_Summary": "",
        "Project_Tag": ""
    }

def run_full():
    """Full extraction from scratch."""
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
    
    with open(RAW_PATH, 'w') as f:
        json.dump(all_sessions, f, indent=2)
    
    ledger = [session_to_ledger_row(s) for s in all_sessions]
    save_ledger(ledger)
    print(f"\nFull sync complete. {len(ledger)} sessions in Ledger.")
    return ledger

def run_delta():
    """Fetch only sessions newer than the most recent in the Ledger."""
    ledger = load_ledger()
    if not ledger:
        print("Ledger empty. Running full sync...")
        return run_full()
    
    # Get the most recent session ID in the Ledger
    known_ids = {row['Source_ID'] for row in ledger}
    print(f"Ledger has {len(ledger)} sessions. Checking for new ones...")
    
    new_sessions = []
    offset = 0
    stop = False
    
    while not stop:
        data = fetch_page(offset)
        sessions = data.get("sessions", [])
        if not sessions:
            break
        
        for s in sessions:
            if s.get('uid') in known_ids:
                stop = True
                break
            new_sessions.append(s)
        
        if not data.get("hasNext", False):
            break
        offset += 100
        time.sleep(0.5)
    
    if new_sessions:
        new_rows = [session_to_ledger_row(s) for s in new_sessions]
        ledger = new_rows + ledger  # Prepend (newest first)
        save_ledger(ledger)
        print(f"Delta sync complete. Added {len(new_sessions)} new sessions. Total: {len(ledger)}")
    else:
        print("No new sessions found. Ledger is up to date.")
    
    return ledger

if __name__ == "__main__":
    if "--full" in sys.argv:
        run_full()
    else:
        run_delta()
