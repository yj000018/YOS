#!/usr/bin/env python3
import json, subprocess

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"
payload = {
    "parent": {"page_id": PARENT_ID},
    "pages": [{"properties": {"title": "Test Page"}, "content": "This is a test page."}]
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
       "--server", "notion", "--input", json.dumps(payload)]
r = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)
