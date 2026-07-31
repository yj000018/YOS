#!/usr/bin/env python3
"""
Y-OS Delta Manus Pipeline
=========================
Détecte les nouvelles sessions Manus depuis la dernière cutoff,
génère les fact sheets enrichies (verbatim + YAML front matter via Gemini),
redacte les secrets, et pousse dans GitHub main.

Cron: 0 2 * * * python3 /home/ubuntu/yos/ledger/delta_manus.py >> /home/ubuntu/yos/ledger/delta_manus.log 2>&1

State: /home/ubuntu/yos/ledger/state.json
  { "manus_cutoff": "2026-07-31T00:00:00Z", "last_run": "...", "total_processed": 564 }
"""

import json
import time
import re
import base64
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

# ─── CONFIG ───────────────────────────────────────────────────────────────────
STATE_FILE = Path("/home/ubuntu/yos/ledger/state.json")
ENRICHED_DIR = Path("/home/ubuntu/yos/ledger/factsheets_enriched")
ENRICHED_DIR.mkdir(exist_ok=True)

MANUS_API_KEY = open("/home/ubuntu/yos/ledger/.manus_key").read().strip()
GEMINI_KEY = open("/home/ubuntu/yos/ledger/.gemini_key").read().strip()
GITHUB_PAT = open("/home/ubuntu/yos/ledger/.github_pat").read().strip()

REPO = "yj000018/YOS"
GITHUB_PATH = "08_LOGS/session-ledger/sessions/manus"

# Subtask patterns to exclude
SUBTASK_PATTERNS = [
    "wide research subtask", "parallel subtask", "research subtask",
    "subtask", "sub-task", "worker task"
]

# Secret redaction patterns
SECRET_PATTERNS = [
    (r'sk-[A-Za-z0-9]{20,}', '[REDACTED_SK]'),
    (r'ghp_[A-Za-z0-9]{36,}', '[REDACTED_GHP]'),
    (r'AIza[A-Za-z0-9_\-]{35}', '[REDACTED_GOOG]'),
    (r're_[A-Za-z0-9]{32,}', '[REDACTED_RESEND]'),
    (r'r8_[A-Za-z0-9]{32,}', '[REDACTED_REPLICATE]'),
    (r'ops_[A-Za-z0-9]{32,}', '[REDACTED_1P_SAT]'),
    (r'[A-Z0-9]{32}\.[A-Z0-9]{32}', '[REDACTED_TOKEN]'),
    (r'Bearer [A-Za-z0-9\-_\.]{40,}', 'Bearer [REDACTED]'),
    (r'token["\s:=]+[A-Za-z0-9\-_\.]{40,}', 'token: [REDACTED]'),
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    # Default: cutoff = today (first run after initial bulk)
    return {
        "manus_cutoff": "2026-07-31T00:00:00Z",
        "last_run": None,
        "total_processed": 564
    }

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def manus_request(path, params=None):
    """Call Manus API v2."""
    url = f"https://api.manus.im/v2/{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{qs}"
    req = urllib.request.Request(url, headers={"x-manus-api-key": MANUS_API_KEY})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 5 * (attempt + 1)
                log(f"  Rate limit, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")

def gemini_extract(content_preview):
    """Extract semantic metadata via Gemini 2.5 Flash."""
    prompt = f"""Analyze this Manus AI session and extract metadata as JSON only.

Session content (first 2000 chars):
{content_preview[:2000]}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "importance": <1-5 integer>,
  "projects": ["project1", "project2"],
  "tags": ["tag1", "tag2", "tag3"],
  "summary_1line": "One sentence summary in English"
}}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 400, "temperature": 0.1}
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Parse JSON from response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        log(f"  Gemini error: {e}")
    return {"importance": 3, "projects": [], "tags": [], "summary_1line": ""}

def get_session_messages(task_id):
    """Get all messages for a session with pagination."""
    messages = []
    cursor = None
    while True:
        params = {"task_id": task_id, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = manus_request("task.listMessages", params)
        msgs = data.get("messages", [])
        messages.extend(msgs)
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        time.sleep(0.3)
    return messages

def extract_text(content):
    """Extract text from message content (string or array)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)
    return str(content)

def redact_secrets(text):
    """Remove secrets from text."""
    for pattern, replacement in SECRET_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text

def build_enriched_factsheet(session, messages, sem):
    """Build enriched MD fact sheet with YAML front matter."""
    task_id = session["id"]
    title = session.get("title", task_id)
    created_at = session.get("created_at", "")
    date = created_at[:10] if created_at else ""
    url = f"https://manus.im/app/task/{task_id}"

    importance = sem.get("importance", 3)
    projects = sem.get("projects", [])
    tags = sem.get("tags", [])
    summary = sem.get("summary_1line", "").replace('"', "'")[:200]

    # Build verbatim
    user_msgs = [m for m in messages if m.get("role") == "user"]
    assistant_msgs = [m for m in messages if m.get("role") == "assistant"]

    verbatim_parts = []
    for m in messages:
        role = m.get("role", "")
        content = extract_text(m.get("content", ""))
        if content.strip() and role in ("user", "assistant"):
            label = "**User**" if role == "user" else "**Assistant**"
            verbatim_parts.append(f"{label}: {content[:1000]}")

    verbatim = "\n\n".join(verbatim_parts[:20])  # Cap at 20 exchanges
    verbatim = redact_secrets(verbatim)

    front_matter = f"""---
id: {task_id}
title: "{title.replace('"', "'")}"
date: "{date}"
importance: {importance}
projects: {json.dumps(projects, ensure_ascii=False)}
tags: {json.dumps(tags, ensure_ascii=False)}
summary: "{summary}"
url: "{url}"
user_messages: {len(user_msgs)}
assistant_messages: {len(assistant_msgs)}
---"""

    body = f"""# {title}

| Field | Value |
|-------|-------|
| **Session ID** | `{task_id}` |
| **Date** | {date} |
| **URL** | [{url}]({url}) |
| **Importance** | {importance}/5 |
| **Projects** | {', '.join(projects) if projects else '—'} |
| **Tags** | {', '.join(tags) if tags else '—'} |

## Summary

{summary if summary else '_No summary available._'}

## Verbatim

{verbatim if verbatim else '_No messages available._'}
"""

    return front_matter + "\n\n" + body

def gh_request(method, path, data=None):
    """GitHub API request."""
    url = f"https://api.github.com/repos/{REPO}/{path}"
    headers = {"Authorization": f"token {GITHUB_PAT}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def push_files_to_github(files_dict, commit_message):
    """Push multiple files to GitHub in a single commit."""
    if not files_dict:
        return None

    ref_data = gh_request("GET", "git/ref/heads/main")
    base_sha = ref_data["object"]["sha"]
    commit_data = gh_request("GET", f"git/commits/{base_sha}")
    base_tree_sha = commit_data["tree"]["sha"]

    tree_entries = []
    for gh_path, content in files_dict.items():
        blob = gh_request("POST", "git/blobs", {"content": content, "encoding": "utf-8"})
        tree_entries.append({
            "path": gh_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob["sha"]
        })
        time.sleep(0.05)

    tree = gh_request("POST", "git/trees", {"base_tree": base_tree_sha, "tree": tree_entries})
    commit = gh_request("POST", "git/commits", {
        "message": commit_message,
        "tree": tree["sha"],
        "parents": [base_sha]
    })
    gh_request("PATCH", "git/refs/heads/main", {"sha": commit["sha"], "force": False})
    return commit["sha"]

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    log("=== Y-OS Delta Manus Pipeline START ===")
    state = load_state()
    cutoff = state["manus_cutoff"]
    log(f"Cutoff: {cutoff}")

    # Step 1: Get all sessions since cutoff
    log("Fetching sessions from Manus API...")
    all_sessions = []
    cursor = None
    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor
        data = manus_request("task.list", params)
        tasks = data.get("tasks", [])
        if not tasks:
            break

        new_in_batch = 0
        for t in tasks:
            created = t.get("created_at", "")
            if created <= cutoff:
                # Reached cutoff — stop pagination
                log(f"Reached cutoff at {created}")
                tasks = []
                break
            # Filter out subtasks
            title = (t.get("title") or "").lower()
            if any(p in title for p in SUBTASK_PATTERNS):
                continue
            all_sessions.append(t)
            new_in_batch += 1

        if not tasks or not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        log(f"  Fetched {len(all_sessions)} new sessions so far...")
        time.sleep(0.3)

    log(f"Found {len(all_sessions)} new named sessions since cutoff")

    if not all_sessions:
        log("No new sessions — nothing to do")
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        return

    # Step 2: Process each session
    files_to_push = {}
    new_cutoff = cutoff

    for i, session in enumerate(all_sessions):
        task_id = session["id"]
        title = session.get("title", task_id)
        created = session.get("created_at", "")
        log(f"  [{i+1}/{len(all_sessions)}] {task_id} — {title[:60]}")

        try:
            # Get messages
            messages = get_session_messages(task_id)

            # Build content preview for Gemini
            user_texts = [extract_text(m.get("content", "")) for m in messages if m.get("role") == "user"]
            preview = "\n".join(user_texts[:5])

            # Semantic extraction
            sem = gemini_extract(preview)
            time.sleep(0.5)

            # Build enriched fact sheet
            content = build_enriched_factsheet(session, messages, sem)

            # Save locally
            local_path = ENRICHED_DIR / f"{task_id}.md"
            local_path.write_text(content, encoding="utf-8")

            # Queue for GitHub push
            files_to_push[f"{GITHUB_PATH}/{task_id}.md"] = content

            # Update cutoff to latest processed
            if created > new_cutoff:
                new_cutoff = created

        except Exception as e:
            log(f"  ERROR {task_id}: {e}")
            continue

        time.sleep(0.5)

    # Step 3: Push to GitHub
    if files_to_push:
        log(f"Pushing {len(files_to_push)} files to GitHub...")
        commit_sha = push_files_to_github(
            files_to_push,
            f"feat: delta {len(files_to_push)} new Manus sessions ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})"
        )
        log(f"✅ Pushed — commit: {commit_sha[:10] if commit_sha else 'N/A'}")

    # Step 4: Update state
    state["manus_cutoff"] = new_cutoff
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["total_processed"] = state.get("total_processed", 564) + len(files_to_push)
    save_state(state)

    log(f"=== DONE — {len(files_to_push)} sessions processed. New cutoff: {new_cutoff} ===")

if __name__ == "__main__":
    main()
