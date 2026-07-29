#!/usr/bin/env python3
"""
Y-OS Session Ledger — LMP Phase 2: Deep Processing
Processes Pending sessions: generates Topic_Summary via LLM, pushes to Notion, marks as Archived.

Usage:
  python3 process_ledger.py --limit 10          # Process 10 pending sessions
  python3 process_ledger.py --source Manus      # Process only Manus sessions
  python3 process_ledger.py --dry-run           # Preview without writing

Architecture:
  1. Load Ledger → filter Pending sessions
  2. For each session:
     a. Fetch verbatim (Manus API GetSession, or from raw export file)
     b. Generate Topic_Summary via LLM (Anthropic Claude)
     c. Push synthesis to Notion (yOS Memory — Sessions)
     d. Update Ledger: Archive_Status=Archived, Archive_Link=<notion_url>
  3. Save updated Ledger

NOTE: This script is a STUB. Full implementation requires:
  - Manus API GetSession endpoint (to fetch verbatim for Manus sessions)
  - Anthropic API key (set as ANTHROPIC_API_KEY env var)
  - Notion API key (set as NOTION_API_KEY env var)
  - Notion database ID for yOS Memory — Sessions
"""
import json
import csv
import sys
import os
import argparse

LEDGER_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'master_ledger.csv')

def load_ledger():
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_ledger(rows):
    fieldnames = ['Global_UID', 'Source', 'Source_ID', 'Title', 'Project_ID',
                  'Created_At', 'Updated_At', 'Archive_Status', 'Archive_Link',
                  'Topic_Summary', 'Project_Tag']
    with open(LEDGER_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def fetch_manus_verbatim(session_uid, jwt_token, client_id):
    """Fetch full session content from Manus API."""
    import urllib.request
    url = "https://api.manus.im/session.v1.SessionService/GetSession"
    headers = {
        "accept": "*/*",
        "authorization": f"Bearer {jwt_token}",
        "connect-protocol-version": "1",
        "content-type": "application/json",
        "x-client-id": client_id,
    }
    payload = {"sessionUid": session_uid}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def generate_summary(title, verbatim_snippet, anthropic_key):
    """Generate a 1-2 sentence topic summary using Claude."""
    import anthropic
    client = anthropic.Anthropic(api_key=anthropic_key)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": f"Session title: {title}\n\nFirst 500 chars of content: {verbatim_snippet[:500]}\n\nWrite a 1-2 sentence summary of what this session is about. Be specific and concise."
        }]
    )
    return message.content[0].text.strip()

def push_to_notion(session, summary, notion_key, database_id):
    """Push session synthesis to Notion yOS Memory — Sessions database."""
    import urllib.request
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": session['Title']}}]},
            "Source": {"select": {"name": session['Source']}},
            "Source_ID": {"rich_text": [{"text": {"content": session['Source_ID']}}]},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Date": {"date": {"start": session['Created_At'][:10] if session['Created_At'] else ""}},
        }
    }
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode())
        return f"https://notion.so/{result['id'].replace('-', '')}"

def main():
    parser = argparse.ArgumentParser(description='Process Pending sessions in the Ledger')
    parser.add_argument('--limit', type=int, default=10, help='Number of sessions to process')
    parser.add_argument('--source', default=None, help='Filter by source (e.g., Manus, ChatGPT)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = parser.parse_args()

    # Load credentials from environment
    jwt_token = os.environ.get('MANUS_JWT_TOKEN', '')
    client_id = os.environ.get('MANUS_CLIENT_ID', '')
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
    notion_key = os.environ.get('NOTION_API_KEY', '')
    notion_db_id = os.environ.get('NOTION_SESSIONS_DB_ID', '')

    ledger = load_ledger()
    pending = [s for s in ledger if s['Archive_Status'] == 'Pending']
    
    if args.source:
        pending = [s for s in pending if s['Source'] == args.source]
    
    print(f"Total pending: {len(pending)}")
    print(f"Processing: {min(args.limit, len(pending))} sessions")
    
    if args.dry_run:
        print("\nDRY RUN — sessions that would be processed:")
        for s in pending[:args.limit]:
            print(f"  [{s['Source']}] {s['Title'][:70]}")
        return
    
    if not anthropic_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Export it before running.")
        sys.exit(1)
    
    processed = 0
    for session in pending[:args.limit]:
        print(f"\nProcessing: {session['Title'][:60]}...")
        
        try:
            # Step 1: Fetch verbatim
            verbatim = ""
            if session['Source'] == 'Manus' and jwt_token:
                data = fetch_manus_verbatim(session['Source_ID'], jwt_token, client_id)
                # Extract first message content as snippet
                verbatim = str(data)[:500]
            
            # Step 2: Generate summary
            summary = generate_summary(session['Title'], verbatim, anthropic_key)
            print(f"  Summary: {summary[:80]}...")
            
            # Step 3: Push to Notion (optional)
            notion_url = ""
            if notion_key and notion_db_id:
                notion_url = push_to_notion(session, summary, notion_key, notion_db_id)
                print(f"  Notion: {notion_url}")
            
            # Step 4: Update Ledger
            for row in ledger:
                if row['Source_ID'] == session['Source_ID']:
                    row['Archive_Status'] = 'Archived'
                    row['Topic_Summary'] = summary
                    row['Archive_Link'] = notion_url
                    break
            
            processed += 1
            
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    save_ledger(ledger)
    print(f"\nDone. Processed {processed}/{min(args.limit, len(pending))} sessions.")

if __name__ == '__main__':
    main()
