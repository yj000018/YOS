#!/usr/bin/env python3
"""
Y-OS Session Ledger — ChatGPT Ingestion Script
Ingests conversations from a ChatGPT export ZIP or conversations.json file.

Usage:
  python3 ingest_chatgpt.py <path_to_conversations.json>
  python3 ingest_chatgpt.py <path_to_chatgpt_export.zip>

How to get your ChatGPT export:
  1. Go to https://chatgpt.com
  2. Settings → Data controls → Export data
  3. Wait for email with download link
  4. Download ZIP, extract conversations.json
  5. Run: python3 ingest_chatgpt.py /path/to/conversations.json
"""
import json
import csv
import sys
import os
import zipfile
from datetime import datetime

LEDGER_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'master_ledger.csv')

def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_ledger(rows):
    fieldnames = ['Global_UID', 'Source', 'Source_ID', 'Title', 'Project_ID',
                  'Created_At', 'Updated_At', 'Archive_Status', 'Archive_Link',
                  'Topic_Summary', 'Project_Tag']
    with open(LEDGER_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def parse_conversations_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sessions = []
    for conv in data:
        conv_id = conv.get('id', '')
        title = conv.get('title', 'Untitled')
        created = conv.get('create_time', 0)
        updated = conv.get('update_time', 0)
        
        created_dt = datetime.fromtimestamp(created).isoformat() if created else ''
        updated_dt = datetime.fromtimestamp(updated).isoformat() if updated else ''
        
        sessions.append({
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
    
    return sessions

def ingest(input_path):
    # Handle ZIP or JSON
    if input_path.endswith('.zip'):
        with zipfile.ZipFile(input_path, 'r') as z:
            if 'conversations.json' in z.namelist():
                tmp_path = '/tmp/chatgpt_conversations.json'
                z.extract('conversations.json', '/tmp/')
                input_path = tmp_path
            else:
                print(f"ERROR: conversations.json not found in ZIP. Files: {z.namelist()}")
                return
    
    print(f"Parsing {input_path}...")
    new_sessions = parse_conversations_json(input_path)
    print(f"Found {len(new_sessions)} ChatGPT conversations")
    
    # Load existing Ledger and find delta
    ledger = load_ledger()
    known_ids = {row['Source_ID'] for row in ledger}
    
    delta = [s for s in new_sessions if s['Source_ID'] not in known_ids]
    print(f"New sessions (not in Ledger): {len(delta)}")
    
    if not delta:
        print("No new sessions to add. Ledger is up to date.")
        return
    
    # Prepend new sessions (newest first)
    updated_ledger = delta + ledger
    save_ledger(updated_ledger)
    print(f"Ledger updated. Total: {len(updated_ledger)} sessions ({len(delta)} new ChatGPT added)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ingest(sys.argv[1])
