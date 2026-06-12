#!/usr/bin/env python3
import json, subprocess, re

CODO_ADDENDUM = """\n\n---\n\n## Update v1.1 — CODO (Saraswati) Integration\n\nA new executive role has been added to the Y-OS organizational layer:\n\n**CODO (Saraswati) — Chief Organizational Development Officer**\n\nMission: Improve the organization that executes missions.\n\nSee: [CODO Agent Card — Saraswati](https://app.notion.com/p/37d35e218cf8815989cce65ffb125a6f) | [Y-OS Organizational Model v1](https://app.notion.com/p/37d35e218cf881bc9d32f6d64e67310e) | [ADR-000X — Creation of the CODO Role](https://app.notion.com/p/37d35e218cf881289baae5f4803956d5)\n\n**Y-OS Law #7:** The organization itself is a system that must continuously improve. The COO executes missions. The CODO improves the organization that executes missions.\n\n**Updated Build Order:** CODO (Saraswati) → Strategist (Krishna) → Architect (Brahma) → Developer (Hanuman)\n"""

VISION_ADDENDUM = """\n\n---\n\n## Update v1.1 — CODO (Saraswati) Integration\n\nThe organizational layer now includes the CODO role (Saraswati), responsible for improving the organization itself.\n\n**Y-OS Law #7:** The organization itself is a system that must continuously improve.\n\nSee: [Y-OS Organizational Model v1](https://app.notion.com/p/37d35e218cf881bc9d32f6d64e67310e)\n"""

PAGES = [
    # (page_id, title, addendum)
    ("37d35e218cf8818cb053c2b1b6fa8e2f", "COO Agent Specification v1", CODO_ADDENDUM),
    ("37d35e218cf8814aa50dc5dadb9f20db", "Y-OS Vision & First Principles", VISION_ADDENDUM),
    ("37c35e218cf88192a428c1f6405999a1", "Y-OS Core Architecture v1", CODO_ADDENDUM),
]

def update_page(page_id, title, addendum):
    payload = {
        "page_id": page_id,
        "command": "insert_content",
        "content": addendum,
        "position": {"type": "end"}
    }
    cmd = ["manus-mcp-cli", "tool", "call", "notion-update-page",
           "--server", "notion", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    if "error" in out.lower() and "invalid" in out.lower():
        print(f"  ❌ {title}: {out[-100:]}")
    else:
        print(f"  ✅ {title}")

print("Updating existing pages with CODO references...")
for page_id, title, addendum in PAGES:
    update_page(page_id, title, addendum)
print("Done.")
