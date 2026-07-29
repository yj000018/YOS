#!/usr/bin/env python3
"""
Y-OS Session Ledger — ChatGPT Ingestion via Cookie-Editor
Uses session cookies exported from browser to call ChatGPT's internal API.
No Playwright, no ZIP export needed. Works with ChatGPT Team/Business accounts.

SETUP (one-time, ~5 minutes):
  1. Install Cookie-Editor extension: https://cookie-editor.com
     - Chrome/Brave: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
  2. Go to https://chatgpt.com (must be logged in)
  3. Click Cookie-Editor icon → Export → "Export as JSON"
  4. Save the JSON to: /home/ubuntu/yos/ledger/chatgpt_cookies.json
     (on Cloud Computer — never commit this file to Git)

USAGE:
  python3 ingest_chatgpt_cookies.py                          # Delta sync
  python3 ingest_chatgpt_cookies.py --full                   # Full rebuild
  python3 ingest_chatgpt_cookies.py --limit 200              # First 200 only
  python3 ingest_chatgpt_cookies.py --cookies /path/to.json  # Custom cookie file
  python3 ingest_chatgpt_cookies.py --dry-run                # Preview, no write

NOTES:
  - Cookies expire after ~30 days of inactivity. Re-export when you get 401 errors.
  - ChatGPT Team accounts: cookies work the same way as personal accounts.
  - The API endpoint is unofficial (internal) — may change if OpenAI updates their app.
  - Rate limit: ~1 req/sec is safe. Script adds 0.5s delay between pages.
"""
import json
import csv
import sys
import os
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'master_ledger.csv')
DEFAULT_COOKIES_PATH = os.path.expanduser('~/yos/ledger/chatgpt_cookies.json')

# ── ChatGPT internal API ───────────────────────────────────────────────────────
CHATGPT_API_BASE = "https://chatgpt.com/backend-api"
PAGE_SIZE = 100  # Max allowed by ChatGPT API

# ── Ledger helpers ─────────────────────────────────────────────────────────────
LEDGER_FIELDS = ['Global_UID', 'Source', 'Source_ID', 'Title', 'Project_ID',
                 'Created_At', 'Updated_At', 'Archive_Status', 'Archive_Link',
                 'Topic_Summary', 'Project_Tag']

def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_ledger(rows):
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

# ── Cookie handling ────────────────────────────────────────────────────────────
def load_cookies(cookies_path):
    """Load cookies from Cookie-Editor JSON export format."""
    with open(cookies_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    
    # Cookie-Editor exports as array of objects with 'name' and 'value' keys
    # Handle both formats: [{name, value, ...}] and {name: value}
    if isinstance(raw, list):
        return {c['name']: c['value'] for c in raw if 'name' in c and 'value' in c}
    elif isinstance(raw, dict):
        return raw
    else:
        raise ValueError(f"Unknown cookie format in {cookies_path}")

def cookies_to_header(cookies_dict):
    """Convert cookie dict to Cookie header string."""
    return '; '.join(f"{k}={v}" for k, v in cookies_dict.items())

# ── ChatGPT API calls ──────────────────────────────────────────────────────────
def get_conversations(cookies_dict, offset=0, limit=PAGE_SIZE):
    """Fetch one page of conversations from ChatGPT internal API."""
    url = f"{CHATGPT_API_BASE}/conversations?offset={offset}&limit={limit}&order=updated"
    headers = {
        "Accept": "application/json",
        "Cookie": cookies_to_header(cookies_dict),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Referer": "https://chatgpt.com/",
        "Origin": "https://chatgpt.com",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("ERROR 401: Cookies expired. Re-export from Cookie-Editor and try again.")
            sys.exit(1)
        elif e.code == 429:
            print("Rate limited. Waiting 10 seconds...")
            time.sleep(10)
            return get_conversations(cookies_dict, offset, limit)
        else:
            raise

def fetch_all_conversations(cookies_dict, known_ids=None, max_sessions=None):
    """
    Fetch all conversations with delta detection.
    Stops early when it hits a known ID (delta mode) or max_sessions limit.
    """
    all_sessions = []
    offset = 0
    total_fetched = 0
    
    while True:
        print(f"  Fetching offset={offset}...", end=' ', flush=True)
        data = get_conversations(cookies_dict, offset=offset, limit=PAGE_SIZE)
        
        items = data.get('items', [])
        total_available = data.get('total', '?')
        
        if not items:
            print("No more items.")
            break
        
        print(f"{len(items)} conversations (total available: {total_available})")
        
        new_in_page = 0
        stop_early = False
        
        for item in items:
            conv_id = item.get('id', '')
            
            # Delta detection: stop when we hit a known ID
            if known_ids and conv_id in known_ids:
                print(f"  Delta boundary reached at: {item.get('title', '')[:50]}")
                stop_early = True
                break
            
            title = item.get('title', 'Untitled')
            created = item.get('create_time', 0)
            updated = item.get('update_time', 0)
            
            created_dt = datetime.fromtimestamp(created).isoformat() if created else ''
            updated_dt = datetime.fromtimestamp(updated).isoformat() if updated else ''
            
            all_sessions.append({
                'Global_UID': f'chatgpt_{conv_id}',
                'Source': 'ChatGPT',
                'Source_ID': conv_id,
                'Title': title,
                'Project_ID': '',
                'Created_At': created_dt,
                'Updated_At': updated_dt,
                'Archive_Status': 'Pending',
                'Archive_Link': '',
                'Topic_Summary': '',
                'Project_Tag': ''
            })
            new_in_page += 1
            total_fetched += 1
        
        if stop_early:
            break
        
        if max_sessions and total_fetched >= max_sessions:
            print(f"  Reached limit of {max_sessions} sessions.")
            break
        
        # Check if there are more pages
        has_missing = data.get('has_missing_conversations', False)
        if len(items) < PAGE_SIZE and not has_missing:
            print("  Last page reached.")
            break
        
        offset += PAGE_SIZE
        time.sleep(0.5)  # Polite rate limiting
    
    return all_sessions

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Ingest ChatGPT conversations into Y-OS Ledger')
    parser.add_argument('--cookies', default=DEFAULT_COOKIES_PATH,
                        help=f'Path to Cookie-Editor JSON export (default: {DEFAULT_COOKIES_PATH})')
    parser.add_argument('--full', action='store_true',
                        help='Full rebuild — ignore existing Ledger entries')
    parser.add_argument('--limit', type=int, default=None,
                        help='Max sessions to fetch (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview without writing to Ledger')
    args = parser.parse_args()
    
    # Validate cookies file
    if not os.path.exists(args.cookies):
        print(f"ERROR: Cookie file not found: {args.cookies}")
        print("\nSetup instructions:")
        print("  1. Install Cookie-Editor: https://cookie-editor.com")
        print("  2. Go to chatgpt.com (logged in)")
        print("  3. Click Cookie-Editor → Export → Export as JSON")
        print(f"  4. Save to: {args.cookies}")
        sys.exit(1)
    
    print(f"Loading cookies from: {args.cookies}")
    cookies = load_cookies(args.cookies)
    print(f"Loaded {len(cookies)} cookies")
    
    # Load existing Ledger
    ledger = load_ledger()
    chatgpt_known_ids = {row['Source_ID'] for row in ledger if row['Source'] == 'ChatGPT'}
    print(f"Existing ChatGPT sessions in Ledger: {len(chatgpt_known_ids)}")
    
    # Fetch conversations
    known_ids = None if args.full else chatgpt_known_ids
    print(f"\nFetching ChatGPT conversations ({'full rebuild' if args.full else 'delta sync'})...")
    
    new_sessions = fetch_all_conversations(cookies, known_ids=known_ids, max_sessions=args.limit)
    
    print(f"\nNew sessions found: {len(new_sessions)}")
    
    if not new_sessions:
        print("Ledger is already up to date. Nothing to add.")
        return
    
    if args.dry_run:
        print("\nDRY RUN — sessions that would be added:")
        for s in new_sessions[:20]:
            print(f"  {s['Created_At'][:10]} | {s['Title'][:70]}")
        if len(new_sessions) > 20:
            print(f"  ... and {len(new_sessions) - 20} more")
        return
    
    # Merge: new sessions first (newest first in delta, then existing)
    if args.full:
        # Full rebuild: replace all ChatGPT entries
        non_chatgpt = [row for row in ledger if row['Source'] != 'ChatGPT']
        updated_ledger = new_sessions + non_chatgpt
    else:
        # Delta: prepend new sessions
        updated_ledger = new_sessions + ledger
    
    save_ledger(updated_ledger)
    
    total_chatgpt = len([r for r in updated_ledger if r['Source'] == 'ChatGPT'])
    print(f"\nLedger updated successfully.")
    print(f"  Added: {len(new_sessions)} new ChatGPT sessions")
    print(f"  Total ChatGPT in Ledger: {total_chatgpt}")
    print(f"  Total Ledger size: {len(updated_ledger)} sessions")

if __name__ == '__main__':
    main()
