#!/usr/bin/env python3
"""
Add backlink to Y-OS Vision & First Principles in all architecture documents.
"""
import json, subprocess, re

VISION_URL = "https://app.notion.com/p/37d35e218cf8814aa50dc5dadb9f20db"
VISION_LINK = f"\n\n---\n\n## Foundational Reference\n\n> This document is governed by [Y-OS Vision & First Principles]({VISION_URL}).\n> Future architectural decisions must remain consistent with that document unless superseded by a formal ADR.\n"

# Pages to update: (page_id, title)
PAGES = [
    ("37c35e218cf88192a428c1f6405999a1", "Y-OS Core Architecture v1"),
    ("37c35e218cf881b3a707d0a4791d4f75", "Y-REG Object Model v1"),
    ("37c35e218cf881a187bedf16944646d4", "Y-REG Technical Architecture v1"),
    ("37c35e218cf881ce9befc037bab5873b", "Y-REG ADR"),
    ("37d35e218cf881728295e1702438fc8c", "Y-ORC Specification v1"),
    ("37d35e218cf8818cb053c2b1b6fa8e2f", "COO Agent Specification v1"),
]

def insert_backlink(page_id, title):
    payload = {
        "page_id": page_id,
        "command": "insert_content",
        "content": VISION_LINK,
        "position": {"type": "end"}
    }
    cmd = ["manus-mcp-cli", "tool", "call", "notion-update-page",
           "--server", "notion", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    if "error" in out.lower() and "success" not in out.lower():
        print(f"  ❌ {title}: {out[-100:]}")
        return False
    else:
        print(f"  ✅ {title}")
        return True

print("Adding Vision backlinks to architecture documents...")
for page_id, title in PAGES:
    insert_backlink(page_id, title)

print("\nDone.")
