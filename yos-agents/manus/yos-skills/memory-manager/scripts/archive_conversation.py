#!/usr/bin/env python3
"""
Archive a conversation to Notion Memory Hub.
Creates a structured conversation archive with summary, ToC, key points, and transcript.
"""

import json
import sys
import subprocess
from datetime import datetime

def create_conversation_archive(title, summary, toc_items, key_points, decisions, actions, transcript_chapters, tags, related_projects):
    """
    Create a conversation archive in Notion.
    
    Args:
        title: Main subject of the conversation
        summary: Executive summary (2-3 sentences)
        toc_items: List of chapter titles for ToC
        key_points: Dict of {chapter: [points]}
        decisions: List of decisions made
        actions: List of action items
        transcript_chapters: Dict of {chapter: transcript_text}
        tags: List of tag names
        related_projects: List of project URLs to mention
    """
    
    # Format date
    date_str = datetime.now().strftime("%Y-%m-%d")
    full_title = f"📝 [{date_str}] {title}"
    
    # Build content
    content_parts = []
    
    # Summary
    content_parts.append("# Résumé Exécutif\\n\\n")
    content_parts.append(f"{summary}\\n\\n")
    content_parts.append("<empty-block/>\\n\\n")
    
    # ToC
    content_parts.append("# Table des Matières\\n\\n")
    for i, item in enumerate(toc_items, 1):
        content_parts.append(f"{i}. {item}\\n")
    content_parts.append("\\n<empty-block/>\\n\\n")
    
    # Key Points by Chapter
    content_parts.append("# Points Clés\\n\\n")
    for chapter, points in key_points.items():
        content_parts.append(f"## {chapter}\\n\\n")
        for point in points:
            content_parts.append(f"- {point}\\n")
        content_parts.append("\\n<empty-block/>\\n\\n")
    
    # Decisions
    if decisions:
        content_parts.append("# Décisions Prises\\n\\n")
        for decision in decisions:
            content_parts.append(f"- {decision}\\n")
        content_parts.append("\\n<empty-block/>\\n\\n")
    
    # Actions
    if actions:
        content_parts.append("# Actions à Suivre\\n\\n")
        for action in actions:
            content_parts.append(f"- [ ] {action}\\n")
        content_parts.append("\\n<empty-block/>\\n\\n")
    
    # Related Projects
    if related_projects:
        content_parts.append("# Projets Liés\\n\\n")
        for project_url in related_projects:
            content_parts.append(f"<mention-page url=\\"{project_url}\\\"/>\\n\\n")
        content_parts.append("<empty-block/>\\n\\n")
    
    # Transcript (in toggles by chapter)
    content_parts.append("# Transcription Complète\\n\\n")
    for chapter, transcript in transcript_chapters.items():
        # Escape special characters in transcript
        escaped_transcript = transcript.replace("\\n", "\\n\\t")
        content_parts.append(f"▶ {chapter}\\n\\t{escaped_transcript}\\n\\n")
    
    content = "".join(content_parts)
    
    # Prepare tags as JSON array
    tags_json = json.dumps(tags)
    
    # Create MCP input
    mcp_input = {
        "parent": {
            "data_source_id": "4ea5d9b7-1919-4ed6-974a-3e73049fe9bf"
        },
        "pages": [{
            "properties": {
                "Name": full_title,
                "Type": "📝 Conversation Archive",
                "Tags": tags_json,
                "Statut": "Actif",
                "Priorité": "Moyenne"
            },
            "content": content
        }]
    }
    
    # Call Notion MCP
    result = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "notion-create-pages", "--server", "notion", "--input", json.dumps(mcp_input)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Conversation archivée avec succès : {full_title}")
        print(result.stdout)
    else:
        print(f"❌ Erreur lors de l'archivage : {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python archive_conversation.py <json_file>")
        print("JSON file should contain: title, summary, toc_items, key_points, decisions, actions, transcript_chapters, tags, related_projects")
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
