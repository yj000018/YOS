#!/usr/bin/env python3
"""Publish 4 Y-REG reports to Notion under Y-REG parent page."""
import json, subprocess, os

PARENT_ID = "37c35e218cf8812f9e5ae8e5b7f0e3a2"  # Y-REG parent

reports = [
    ("report_capability_graph.md", "📊 Y-REG — Capability Graph v1"),
    ("report_coverage.md", "📋 Y-REG — Capability Coverage Report v1"),
    ("report_duplicates.md", "🔍 Y-REG — Duplicate Detection Report v1"),
    ("report_missing.md", "❓ Y-REG — Missing Capability Report v1"),
]

def create_page(title, content):
    payload = json.dumps({
        "pages": [{
            "parent_id": PARENT_ID,
            "title": title,
            "content": content[:8000]
        }]
    })
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", payload]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    if "url" in out.lower() or "page_id" in out.lower() or "notion.so" in out.lower():
        print(f"  OK: {title}")
    else:
        print(f"  CHECK: {title} — {out[-150:]}")

for filename, title in reports:
    path = f"/home/ubuntu/yreg/{filename}"
    if os.path.exists(path):
        with open(path) as f:
            content = f.read()
        create_page(title, content)
    else:
        print(f"  MISSING: {filename}")
