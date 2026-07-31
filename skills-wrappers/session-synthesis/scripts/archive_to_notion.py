#!/usr/bin/env python3
"""
Archive to Y-OS Memory (Phase 3 Wrapper)
Replaces Notion writes with yos_memory.SessionStore (Git + Mem0).
"""
import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Add YOS repo path to sys.path
YOS_REPO = os.environ.get("YOS_REPO_PATH", "/tmp/yos_audit_clone")
PIPELINE_DIR = Path(YOS_REPO) / "yos-automations" / "scripts" / "yos-llm-pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

try:
    from yos_memory.session_store import SessionStore
except ImportError:
    print("ERROR: yos_memory package not found. Ensure YOS_REPO_PATH is correct.")
    sys.exit(1)

CARDS_DIR = Path("/home/ubuntu/manus_pipeline/session_cards")
ARCHIVED_FILE = Path("/home/ubuntu/manus_pipeline/archived_uids.json")

def load_archived():
    if ARCHIVED_FILE.exists():
        return set(json.load(open(ARCHIVED_FILE)))
    return set()

def save_archived(archived_set):
    with open(ARCHIVED_FILE, "w") as f:
        json.dump(list(archived_set), f)

def format_content(card: dict, uid: str) -> str:
    parts = []
    if card.get("exec_summary"):
        parts.append(f"## Executive Summary\n{card['exec_summary']}\n")
    if card.get("reasoning_thread"):
        parts.append("## Reasoning Thread\n")
        for step in card["reasoning_thread"]:
            parts.append(f"- {step}")
        parts.append("\n")
    if card.get("decisions"):
        parts.append("## Decisions\n")
        for d in card["decisions"]:
            parts.append(f"- {d}")
        parts.append("\n")
    if card.get("action_items"):
        parts.append("## Action Items\n")
        for a in card["action_items"]:
            parts.append(f"- [ ] {a}")
        parts.append("\n")
    if card.get("artifacts"):
        parts.append("## Artifacts\n")
        for art in card["artifacts"]:
            parts.append(f"- {art}")
        parts.append("\n")
    return "\n".join(parts)

def archive_session(card_path: Path, archived_set: set) -> tuple:
    uid = card_path.stem.replace("_card", "")[:12]
    if uid in archived_set:
        return "skip", "already_archived"
        
    try:
        card = json.load(open(card_path))
    except Exception as e:
        return "error_read", str(e)
        
    title = (card.get("title") or "Untitled")[:100]
    project = card.get("project") or "UNKNOWN"
    tags = card.get("themes", []) + card.get("subthemes", [])
    content = format_content(card, uid)
    
    store = SessionStore()
    result = store.archive_session(
        source="Manus",
        source_id=uid,
        title=title,
        body_markdown=content,
        created_at=card.get("date", ""),
        project_id=project,
        tags=tags
    )
    
    if result.get("status") in ["success", "skipped_duplicate"]:
        archived_set.add(uid)
        return "ok", card.get("depth", "standard")
    else:
        return "error_api", str(result)

def main():
    print("=" * 65)
    print("Manus Memory — Archive to Git+Mem0 (Phase 3 Wrapper)")
    print("=" * 65)
    
    if not CARDS_DIR.exists():
        print(f"Directory not found: {CARDS_DIR}")
        return
        
    archived_set = load_archived()
    print(f"Already archived: {len(archived_set)}")
    
    card_files = sorted(CARDS_DIR.glob("*_card.json"))
    total = len(card_files)
    print(f"Total cards: {total}")
    
    stats = {"ok": 0, "skip": 0, "error": 0}
    
    for i, card_path in enumerate(card_files):
        status, info = archive_session(card_path, archived_set)
        if status == "ok":
            stats["ok"] += 1
            card = json.load(open(card_path))
            title = card.get("title", "?")[:55]
            print(f"  [{i+1:3d}/{total}] ✅ {info:11s} : {title}")
        elif status == "skip":
            stats["skip"] += 1
        else:
            stats["error"] += 1
            uid = card_path.stem.replace("_card", "")[:12]
            print(f"  [{i+1:3d}/{total}] ❌ {status:12s} : {uid} — {info}")
            
        if (i + 1) % 25 == 0:
            save_archived(archived_set)
            print(f"  --- [{i+1}/{total}] ✅{stats['ok']} ⏭️{stats['skip']} ❌{stats['error']} ---")
            
    save_archived(archived_set)
    print(f"\nARCHIVE COMPLETE — ✅ {stats['ok']}  ⏭️ {stats['skip']}  ❌ {stats['error']}")

if __name__ == "__main__":
    main()
