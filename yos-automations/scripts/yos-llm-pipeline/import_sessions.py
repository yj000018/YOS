#!/usr/bin/env python3.11
"""
LLM Session Importer
====================
Imports exported LLM chat sessions (JSON) into Chat_Export_Sessions Notion database.

Usage:
    python3.11 import_sessions.py --file sessions.json [--source ChatGPT]
    python3.11 import_sessions.py --dir ./exports/ [--source Claude]

Input JSON format (per session):
    {
      "session_id": "uuid",
      "title": "Session title",
      "source_llm": "ChatGPT",
      "source_export": "Chrome extension",
      "date_session": "2026-03-07T14:30:00Z",
      "language": "fr",
      "content_raw": "...",
      "metadata": {"url": "...", "tags": [...]}
    }

Minimum required fields: session_id, title, source_llm, date_session, content_raw
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────

DB_CHAT_SESSIONS_DS = "13633cbd-7c08-475e-b610-a5377fbdfa91"

VALID_SOURCE_LLM    = {"ChatGPT", "Claude", "Manus", "Other"}
VALID_SOURCE_EXPORT = {"Chrome extension", "Notion plugin", "JSON import", "Other"}
VALID_LANGUAGE      = {"FR", "EN", "IT", "Mixed"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("importer")

# ─── MCP helper ───────────────────────────────────────────────────────────────

def mcp_create_page(properties: dict, content: str = "") -> dict:
    page_obj = {"properties": properties}
    if content:
        page_obj["content"] = content[:50000]  # Notion page content limit
    payload = {
        "parent": {"data_source_id": DB_CHAT_SESSIONS_DS},
        "pages": [page_obj],
    }
    cmd = [
        "manus-mcp-cli", "tool", "call", "notion-create-pages",
        "--server", "notion",
        "--input", json.dumps(payload),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"MCP error: {result.stderr.strip()}")
    output = result.stdout.strip()
    if "Tool execution result:" in output:
        json_part = output.split("Tool execution result:\n", 1)[-1].strip()
    else:
        json_part = output
    return json.loads(json_part)

# ─── Normalization ────────────────────────────────────────────────────────────

def normalize_session(raw: dict, default_source: str = "Other") -> dict:
    """Normalize a raw session dict to Notion properties."""
    session_id   = str(raw.get("session_id", raw.get("id", "")))
    title        = str(raw.get("title", raw.get("name", "Untitled Session")))[:200]
    source_llm   = raw.get("source_llm", raw.get("model", default_source))
    source_export = raw.get("source_export", "JSON import")
    date_raw     = raw.get("date_session", raw.get("created_at", raw.get("date", "")))
    language     = raw.get("language", "").upper()
    content_raw  = raw.get("content_raw", raw.get("content", raw.get("messages", "")))

    # Normalize source_llm
    if source_llm not in VALID_SOURCE_LLM:
        # Try to detect from string
        sl = str(source_llm).lower()
        if "gpt" in sl or "chatgpt" in sl or "openai" in sl:
            source_llm = "ChatGPT"
        elif "claude" in sl or "anthropic" in sl:
            source_llm = "Claude"
        elif "manus" in sl:
            source_llm = "Manus"
        else:
            source_llm = "Other"

    # Normalize source_export
    if source_export not in VALID_SOURCE_EXPORT:
        source_export = "JSON import"

    # Normalize language
    if language not in VALID_LANGUAGE:
        language = None

    # Normalize date
    date_iso = None
    if date_raw:
        try:
            if isinstance(date_raw, (int, float)):
                dt = datetime.fromtimestamp(date_raw, tz=timezone.utc)
                date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                # Try parsing ISO string
                date_str = str(date_raw).replace("Z", "+00:00")
                dt = datetime.fromisoformat(date_str)
                date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception:
            date_iso = None

    # Normalize content
    if isinstance(content_raw, list):
        # Handle messages array format
        parts = []
        for msg in content_raw:
            if isinstance(msg, dict):
                role = msg.get("role", msg.get("author", ""))
                text = msg.get("content", msg.get("text", ""))
                if isinstance(text, list):
                    text = " ".join(str(t.get("text", t)) if isinstance(t, dict) else str(t) for t in text)
                parts.append(f"[{role}]: {text}")
            else:
                parts.append(str(msg))
        content_raw = "\n\n".join(parts)
    elif not isinstance(content_raw, str):
        content_raw = json.dumps(content_raw, ensure_ascii=False)

    # Estimate token size (rough: chars / 4)
    token_est = len(content_raw) // 4

    # Build properties
    props = {
        "Title": title,
        "Source_LLM": source_llm,
        "Source_Export": source_export,
        "Session_ID": session_id,
        "Content_Raw": content_raw[:2000],  # Notion text property limit
        "Token_Size_Est": token_est,
        "Processed": "__NO__",
    }

    if date_iso:
        props["date:Date_Session:start"] = date_iso
        props["date:Date_Session:is_datetime"] = 1

    if language:
        props["Language"] = language

    # Page content = full raw content (no limit in page body)
    page_content = f"# {title}\n\n**Source:** {source_llm} | **Export:** {source_export}\n\n---\n\n{content_raw}"

    return props, page_content


def import_file(filepath: str, default_source: str = "Other", dry_run: bool = False):
    """Import sessions from a JSON file."""
    log.info(f"Importing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle both array and single object
    if isinstance(data, dict):
        sessions = [data]
    elif isinstance(data, list):
        sessions = data
    else:
        log.error(f"Unexpected JSON format in {filepath}")
        return 0, 0

    success = 0
    errors = 0
    for i, session in enumerate(sessions):
        try:
            props, content = normalize_session(session, default_source)
            title = props.get("Title", "?")
            if dry_run:
                log.info(f"  [DRY-RUN] Would import: {title} ({props.get('Source_LLM')})")
                success += 1
            else:
                result = mcp_create_page(props, content)
                created_url = result.get("pages", [{}])[0].get("url", "?")
                log.info(f"  ✓ Imported: {title} → {created_url}")
                success += 1
        except Exception as e:
            log.error(f"  ✗ Error on session {i}: {e}")
            errors += 1

    return success, errors


def import_directory(dirpath: str, default_source: str = "Other", dry_run: bool = False):
    """Import all JSON files from a directory."""
    p = Path(dirpath)
    files = list(p.glob("*.json"))
    log.info(f"Found {len(files)} JSON files in {dirpath}")
    total_success = 0
    total_errors = 0
    for f in files:
        s, e = import_file(str(f), default_source, dry_run)
        total_success += s
        total_errors += e
    return total_success, total_errors


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import LLM sessions into Notion Chat_Export_Sessions")
    parser.add_argument("--file", help="Path to a JSON file")
    parser.add_argument("--dir", help="Path to a directory of JSON files")
    parser.add_argument("--source", default="Other", help="Default Source_LLM if not in JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    total_s, total_e = 0, 0
    if args.file:
        s, e = import_file(args.file, args.source, args.dry_run)
        total_s += s
        total_e += e
    if args.dir:
        s, e = import_directory(args.dir, args.source, args.dry_run)
        total_s += s
        total_e += e

    log.info(f"Import complete. Success: {total_s} | Errors: {total_e}")
