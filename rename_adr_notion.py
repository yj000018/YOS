#!/usr/bin/env python3
import json, subprocess

PAGE_ID = "37d35e218cf881289baae5f4803956d5"

payload = {
    "page_id": PAGE_ID,
    "command": "update_properties",
    "properties": {
        "title": "ADR-0006 — Creation of the CODO Role"
    }
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-update-page",
       "--server", "notion", "--input", json.dumps(payload)]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
out = result.stdout + result.stderr

print(out[-200:])
