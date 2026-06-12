#!/usr/bin/env python3
import json, subprocess

# ID de la page ADR créée précédemment
PAGE_ID = "37d35e218cf881289baae5f4803956d5"

with open("/home/ubuntu/yreg/ADR-0006_Creation_CODO_Role.md", "r") as f:
    content = f.read()

payload = {
    "page_id": PAGE_ID,
    "command": "replace_content",
    "new_str": content
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-update-page",
       "--server", "notion", "--input", json.dumps(payload)]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
out = result.stdout + result.stderr

if "error" in out.lower() and "invalid" in out.lower():
    print(f"Failed to update ADR: {out[-200:]}")
else:
    print("Successfully updated ADR-0006 in Notion.")
