#!/usr/bin/env python3
"""
generate_factsheets.py — Génère les fact sheets MD pour toutes les sessions Manus
Pipeline: master_ledger.json → task.listMessages API v2 → fact sheets MD → GitHub YOS

Usage: python3 generate_factsheets.py [--limit N] [--start N] [--session-id SID]
"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
MANUS_API_KEY = "sk-Lwjt1ISkT1C73fY9EuIk42wa0JKbrySvwCGMhgzBHAkio0r0dJNAgN9aBnWuXSI6kzSXMy1tqAGkmWHlDKuRbPod4P4A"
LEDGER_PATH = "/home/ubuntu/yos/ledger/master_ledger.json"
OUTPUT_DIR = Path("/home/ubuntu/yos/ledger/factsheets_manus")
RATE_LIMIT_DELAY = 0.5  # seconds between API calls
MAX_MESSAGES_PER_SESSION = 200  # limit per page
MAX_PAGES = 10  # max pages to paginate (200 * 10 = 2000 messages max)

# ── API ──────────────────────────────────────────────────────────────────────
def fetch_messages(task_id: str, limit: int = 200, cursor: str = None) -> dict:
    url = f"https://api.manus.im/v2/task.listMessages?task_id={task_id}&limit={limit}"
    if cursor:
        url += f"&cursor={cursor}"
    headers = {
        "accept": "application/json",
        "x-manus-api-key": MANUS_API_KEY,
    }
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        return {"ok": False, "error": {"code": str(e.code), "message": body}}
    except Exception as e:
        return {"ok": False, "error": {"code": "network", "message": str(e)}}


def fetch_all_messages(task_id: str) -> list:
    """Paginate through all messages for a task."""
    all_messages = []
    cursor = None
    page = 0
    while page < MAX_PAGES:
        resp = fetch_messages(task_id, limit=MAX_MESSAGES_PER_SESSION, cursor=cursor)
        if not resp.get("ok"):
            return None, resp.get("error", {})
        msgs = resp.get("messages", [])
        all_messages.extend(msgs)
        if not resp.get("has_more") or not resp.get("next_cursor"):
            break
        cursor = resp["next_cursor"]
        page += 1
        time.sleep(0.2)
    return all_messages, None


# ── Parser ───────────────────────────────────────────────────────────────────
def extract_content(messages: list) -> dict:
    """Extract user messages and assistant messages from raw API messages."""
    user_msgs = []
    assistant_msgs = []
    
    for m in messages:
        ts = m.get("timestamp", "")
        if "user_message" in m:
            um = m["user_message"]
            content = um.get("content", "")
            if isinstance(content, list):
                # content_parts format
                text_parts = []
                for part in content:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                        elif "text" in part:
                            text_parts.append(part["text"])
                content = " ".join(text_parts)
            if content and str(content).strip():
                user_msgs.append({"ts": ts, "text": str(content).strip()})
        
        elif "assistant_message" in m:
            am = m["assistant_message"]
            content = am.get("content", "")
            if content and str(content).strip():
                assistant_msgs.append({"ts": ts, "text": str(content).strip()})
    
    return {"user": user_msgs, "assistant": assistant_msgs}


def build_factsheet(session: dict, messages: list) -> str:
    """Build a Markdown fact sheet for a session."""
    sid = session.get("Source_ID", session.get("id", "unknown"))
    title = session.get("Title", session.get("title", "Untitled"))
    created_at = session.get("Created_At", session.get("created_at", ""))
    project_id = session.get("Project_ID", session.get("project_id", ""))
    url = f"https://manus.im/app/sessions/{sid}"
    
    # Parse date
    date_str = ""
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d %H:%M UTC")
        except:
            date_str = str(created_at)[:19]
    
    # Extract content
    content = extract_content(messages)
    user_msgs = content["user"]
    assistant_msgs = content["assistant"]
    
    # Build first user message (the "prompt")
    first_user = user_msgs[0]["text"] if user_msgs else ""
    first_assistant = assistant_msgs[0]["text"] if assistant_msgs else ""
    
    # Build summary: first 3 user messages + first 2 assistant responses
    user_summary = "\n\n".join([
        f"> **User:** {m['text'][:500]}{'...' if len(m['text']) > 500 else ''}"
        for m in user_msgs[:3]
    ])
    
    assistant_summary = "\n\n".join([
        f"> **Manus:** {m['text'][:800]}{'...' if len(m['text']) > 800 else ''}"
        for m in assistant_msgs[:2]
    ])
    
    # Build full verbatim (all messages, truncated)
    verbatim_lines = []
    for m in messages:
        ts = m.get("timestamp", "")[:19]
        if "user_message" in m:
            um = m["user_message"]
            c = um.get("content", "")
            if isinstance(c, list):
                c = " ".join([p.get("text", "") if isinstance(p, dict) else str(p) for p in c])
            c = str(c).strip()
            if c:
                verbatim_lines.append(f"**[{ts}] USER:** {c[:1000]}{'...' if len(c) > 1000 else ''}")
        elif "assistant_message" in m:
            am = m["assistant_message"]
            c = str(am.get("content", "")).strip()
            if c:
                verbatim_lines.append(f"**[{ts}] MANUS:** {c[:1000]}{'...' if len(c) > 1000 else ''}")
    
    md = f"""---
session_id: {sid}
title: "{title.replace('"', "'")}"
date: {date_str}
url: {url}
project_id: {project_id or "none"}
user_messages: {len(user_msgs)}
assistant_messages: {len(assistant_msgs)}
total_messages: {len(messages)}
processed: true
---

# {title}

| Field | Value |
|-------|-------|
| **Session ID** | `{sid}` |
| **Date** | {date_str} |
| **Project** | {project_id or "—"} |
| **URL** | [{url}]({url}) |
| **Messages** | {len(user_msgs)} user · {len(assistant_msgs)} assistant · {len(messages)} total |

## Initial Prompt

{first_user[:1000] if first_user else "_No user message found_"}

## First Response

{first_assistant[:1000] if first_assistant else "_No assistant message found_"}

## Conversation Summary

{user_summary or "_No user messages_"}

{assistant_summary or "_No assistant messages_"}

## Full Verbatim

<details>
<summary>Expand full conversation ({len(verbatim_lines)} messages)</summary>

{chr(10).join(verbatim_lines[:100])}

{"_[Truncated — " + str(len(verbatim_lines) - 100) + " more messages]_" if len(verbatim_lines) > 100 else ""}

</details>
"""
    return md


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate Manus session fact sheets")
    parser.add_argument("--limit", type=int, default=None, help="Max sessions to process")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--session-id", type=str, default=None, help="Process single session")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="Skip already processed")
    args = parser.parse_args()

    # Load ledger
    with open(LEDGER_PATH) as f:
        data = json.load(f)
    sessions = data if isinstance(data, list) else data.get("sessions", [])
    print(f"Loaded {len(sessions)} sessions from ledger")

    # Filter
    if args.session_id:
        sessions = [s for s in sessions if s.get("Source_ID") == args.session_id]
        print(f"Filtered to 1 session: {args.session_id}")
    else:
        sessions = sessions[args.start:]
        if args.limit:
            sessions = sessions[:args.limit]
    
    print(f"Processing {len(sessions)} sessions → {OUTPUT_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Stats
    ok_count = 0
    skip_count = 0
    error_count = 0
    errors = []

    for i, session in enumerate(sessions):
        sid = session.get("Source_ID", session.get("id", "unknown"))
        title = session.get("Title", session.get("title", "Untitled"))
        
        # Output path
        out_path = OUTPUT_DIR / f"{sid}.md"
        
        # Skip if exists
        if args.skip_existing and out_path.exists():
            skip_count += 1
            if i % 50 == 0:
                print(f"[{i+1}/{len(sessions)}] SKIP {sid[:12]} — {title[:40]}")
            continue
        
        # Fetch messages
        messages, error = fetch_all_messages(sid)
        
        if error:
            error_count += 1
            errors.append({"sid": sid, "title": title, "error": error})
            print(f"[{i+1}/{len(sessions)}] ❌ {sid[:12]} — {error.get('code')}: {error.get('message','')[:60]}")
            time.sleep(RATE_LIMIT_DELAY)
            continue
        
        # Build fact sheet
        md = build_factsheet(session, messages)
        out_path.write_text(md, encoding="utf-8")
        ok_count += 1
        
        if i % 10 == 0 or i < 5:
            print(f"[{i+1}/{len(sessions)}] ✅ {sid[:12]} — {title[:40]} ({len(messages)} msgs)")
        
        time.sleep(RATE_LIMIT_DELAY)

    # Summary
    print(f"\n{'='*60}")
    print(f"DONE: {ok_count} generated, {skip_count} skipped, {error_count} errors")
    print(f"Output: {OUTPUT_DIR}")
    
    if errors:
        err_path = OUTPUT_DIR / "_errors.json"
        err_path.write_text(json.dumps(errors, indent=2, ensure_ascii=False))
        print(f"Errors saved to: {err_path}")
    
    # Save stats
    stats = {
        "generated": ok_count,
        "skipped": skip_count,
        "errors": error_count,
        "total": len(sessions),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "output_dir": str(OUTPUT_DIR)
    }
    (OUTPUT_DIR / "_stats.json").write_text(json.dumps(stats, indent=2))
    print(f"Stats: {stats}")


if __name__ == "__main__":
    main()
