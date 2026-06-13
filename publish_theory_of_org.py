#!/usr/bin/env python3
"""Publish Y-OS Theory of Organization docs to Notion."""
import subprocess
import json
import time

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def publish(title, content, icon="📐"):
    payload = {
        "pages": [
            {
                "properties": {"title": title},
                "content": content,
                "icon": icon
            }
        ]
    }
    result = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "notion-create-pages",
         "--server", "notion", "--input", json.dumps(payload)],
        capture_output=True, text=True
    )
    print(f"\n=== {title} ===")
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-200:])
    return result.returncode == 0

docs = [
    ("Y-OS Theory of Organization v1", "/home/ubuntu/yreg/Y-OS_Theory_of_Organization_v1.md", "🏛️"),
    ("ADR-0022: Y-OS Theory of Organization", "/home/ubuntu/yreg/ADR-0022_Y-OS_Theory_of_Organization.md", "📋"),
    ("Y-OS Organizational Model — Executive Summary", "/home/ubuntu/yreg/Y-OS_Organizational_Model_Executive_Summary.md", "📄"),
]

for title, path, icon in docs:
    content = read_file(path)
    # Strip the H1 title line from content (Notion adds it from properties)
    lines = content.split('\n')
    # Remove first H1 if present
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
        # Remove leading blank lines
        while lines and lines[0].strip() == '':
            lines = lines[1:]
        content = '\n'.join(lines)
    ok = publish(title, content, icon)
    print("OK" if ok else "FAILED")
    time.sleep(2)

print("\nDone.")
