#!/usr/bin/env python3
"""
Y-OS Session Ledger — Process Pending Sessions
Fetches verbatim, generates summary, archives to Git + Mem0.
Notion write is optional (legacy, requires NOTION_API_KEY + NOTION_SESSIONS_DB_ID).

Usage: python3 process_ledger.py [--limit N] [--source Manus] [--dry-run]

MIGRATION NOTE (Phase 2 — MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR):
  - Primary destination: Git (canonical Markdown) + Mem0 (semantic projection)
  - Notion write: optional, legacy, guarded by NOTION_API_KEY env var
  - Replaced custom load_ledger/save_ledger with yos_memory.SessionLedger
  - Replaced custom CSV I/O with yos_memory.DedupState
  - Credentials exclusively from environment variables (no hardcoded tokens)
"""
import os
import sys
import json
import argparse
import urllib.request
from pathlib import Path

# ─── yos_memory import ────────────────────────────────────────────────────────
_PIPELINE_DIR = Path(__file__).resolve().parents[4] / "yos-automations" / "scripts" / "yos-llm-pipeline"
if str(_PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(_PIPELINE_DIR))

from yos_memory.ledger import SessionLedger
from yos_memory.dedup import DedupState
from yos_memory.session_store import SessionStore

# ─── Manus verbatim fetch ─────────────────────────────────────────────────────
def fetch_manus_verbatim(session_uid: str, jwt_token: str, client_id: str) -> dict:
    url = "https://api.manus.im/session.v1.SessionService/GetSession"
    headers = {
        "accept": "*/*",
        "authorization": f"Bearer {jwt_token}",
        "connect-protocol-version": "1",
        "content-type": "application/json",
        "x-client-id": client_id,
    }
    payload = {"sessionUid": session_uid}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


# ─── LLM Summary ─────────────────────────────────────────────────────────────
def generate_summary(title: str, verbatim_snippet: str, anthropic_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=anthropic_key)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": (
                f"Session title: {title}\n\n"
                f"First 500 chars of content: {verbatim_snippet[:500]}\n\n"
                "Write a 1-2 sentence summary of what this session is about. "
                "Be specific and concise."
            )
        }]
    )
    return message.content[0].text.strip()


# ─── Legacy Notion write (optional) ──────────────────────────────────────────
def push_to_notion_legacy(session: dict, summary: str, notion_key: str, database_id: str) -> str:
    """
    Legacy: push to Notion Sessions DB.
    Only called if NOTION_API_KEY and NOTION_SESSIONS_DB_ID are set.
    """
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": session["Title"]}}]},
            "Source": {"select": {"name": session["Source"]}},
            "Source_ID": {"rich_text": [{"text": {"content": session["Source_ID"]}}]},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Date": {"date": {"start": session["Created_At"][:10] if session.get("Created_At") else ""}},
        }
    }
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode())
        return f"https://notion.so/{result['id'].replace('-', '')}"


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Process Pending sessions in the Ledger")
    parser.add_argument("--limit", type=int, default=10, help="Number of sessions to process")
    parser.add_argument("--source", default=None, help="Filter by source (e.g., Manus, ChatGPT)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    # Credentials from environment only
    jwt_token = os.environ.get("MANUS_JWT_TOKEN", "")
    client_id = os.environ.get("MANUS_CLIENT_ID", "")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    notion_key = os.environ.get("NOTION_API_KEY", "")
    notion_db_id = os.environ.get("NOTION_SESSIONS_DB_ID", "")

    # Load ledger via yos_memory
    ledger = SessionLedger()
    session_store = SessionStore()

    all_rows = ledger.read_all()
    pending = [s for s in all_rows if s.get("Processing_Status") != "processed"
               and s.get("Archive_Status") != "Archived"]

    if args.source:
        pending = [s for s in pending if s.get("Source") == args.source]

    print(f"Total pending: {len(pending)}")
    print(f"Processing: {min(args.limit, len(pending))} sessions")

    if args.dry_run:
        print("\nDRY RUN — sessions that would be processed:")
        for s in pending[:args.limit]:
            print(f"  [{s.get('Source', '?')}] {s.get('Title', 'Untitled')[:70]}")
        return

    if not anthropic_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Export it before running.")
        sys.exit(1)

    processed = 0
    for session in pending[:args.limit]:
        title = session.get("Title", "Untitled")
        source = session.get("Source", "Unknown")
        source_id = session.get("Source_ID", "")
        created_at = session.get("Created_At", "")

        print(f"\nProcessing: {title[:60]}...")

        try:
            # Step 1: Fetch verbatim (Manus only)
            verbatim = ""
            if source == "Manus" and jwt_token and client_id:
                try:
                    data = fetch_manus_verbatim(source_id, jwt_token, client_id)
                    verbatim = str(data)[:2000]
                except Exception as e:
                    print(f"  Verbatim fetch failed: {e}")

            # Step 2: Generate summary
            summary = generate_summary(title, verbatim, anthropic_key)
            print(f"  Summary: {summary[:80]}...")

            # Step 3: Archive to Git + Mem0 (primary destination)
            body = f"## Summary\n\n{summary}\n\n## Verbatim Snippet\n\n{verbatim[:1000]}"
            result = session_store.archive_session(
                source=source,
                source_id=source_id,
                title=title,
                body_markdown=body,
                created_at=created_at,
                project_id=session.get("Project_ID", ""),
            )
            print(f"  Git: {result.get('path', '?')} [{result.get('status')}]")
            print(f"  Mem0: {result.get('mem0_status', '?')}")

            # Step 4: Legacy Notion write (optional)
            notion_url = ""
            if notion_key and notion_db_id:
                try:
                    notion_url = push_to_notion_legacy(session, summary, notion_key, notion_db_id)
                    print(f"  Notion (legacy): {notion_url}")
                except Exception as e:
                    print(f"  Notion write failed (non-blocking): {e}")

            # Step 5: Update ledger with all results
            ledger.update_session(session.get("Global_UID", ""), {
                "Archive_Status": "Archived",
                "Processing_Status": "processed",
                "Topic_Summary": summary,
                "Archive_Link": notion_url,
                "Git_Path": result.get("path", ""),
                "Content_Hash": result.get("hash", ""),
                "Mem0_Status": result.get("mem0_status", ""),
            })

            processed += 1

        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\nDone. Processed {processed}/{min(args.limit, len(pending))} sessions.")


if __name__ == "__main__":
    main()
