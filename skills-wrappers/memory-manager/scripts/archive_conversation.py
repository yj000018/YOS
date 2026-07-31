#!/usr/bin/env python3
"""
Archive a conversation to Y-OS Memory (Phase 3 Wrapper)
Replaces Notion writes with yos_memory.SessionStore (Git + Mem0).
"""
import json
import sys
import os
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

def create_conversation_archive(title, summary, toc_items, key_points, decisions, actions, transcript_chapters, tags, related_projects):
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_title = f"📝 [{date_str}] {title}"
    
    # Build Markdown content
    content_parts = []
    content_parts.append("# Résumé Exécutif\n\n")
    content_parts.append(f"{summary}\n\n")
    
    content_parts.append("# Table des Matières\n\n")
    for i, item in enumerate(toc_items, 1):
        content_parts.append(f"{i}. {item}\n")
    content_parts.append("\n")
    
    content_parts.append("# Points Clés\n\n")
    for chapter, points in key_points.items():
        content_parts.append(f"## {chapter}\n\n")
        for point in points:
            content_parts.append(f"- {point}\n")
        content_parts.append("\n")
    
    if decisions:
        content_parts.append("# Décisions Prises\n\n")
        for decision in decisions:
            content_parts.append(f"- {decision}\n")
        content_parts.append("\n")
    
    if actions:
        content_parts.append("# Actions à Suivre\n\n")
        for action in actions:
            content_parts.append(f"- [ ] {action}\n")
        content_parts.append("\n")
    
    content_parts.append("# Transcription Complète\n\n")
    for chapter, transcript in transcript_chapters.items():
        content_parts.append(f"## {chapter}\n\n{transcript}\n\n")
    
    content = "".join(content_parts)
    
    # Archive via yos_memory
    store = SessionStore()
    result = store.archive_session(
        source="Manus_Archive",
        source_id=datetime.now().strftime("%Y%m%d%H%M%S"),
        title=full_title,
        body_markdown=content,
        created_at=datetime.utcnow().isoformat() + "Z",
        tags=tags
    )
    
    print(f"✅ Conversation archivée avec succès : {full_title}")
    print(f"Git Path: {result.get('path')}")
    print(f"Mem0 Status: {result.get('mem0_status')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python archive_conversation.py <json_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    create_conversation_archive(
        title=data['title'],
        summary=data['summary'],
        toc_items=data['toc_items'],
        key_points=data['key_points'],
        decisions=data.get('decisions', []),
        actions=data.get('actions', []),
        transcript_chapters=data['transcript_chapters'],
        tags=data['tags'],
        related_projects=data.get('related_projects', [])
    )
