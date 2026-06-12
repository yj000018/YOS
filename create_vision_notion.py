#!/usr/bin/env python3
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c" # System Architecture

with open("/home/ubuntu/yreg/Y-OS_Vision_First_Principles.md", "r") as f:
    content = f.read()

payload = {
    "parent": {"page_id": PARENT_ID},
    "pages": [{
        "properties": {"title": "Y-OS Vision & First Principles"},
        "icon": "👁️",
        "content": content
    }]
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
       "--server", "notion", "--input", json.dumps(payload)]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
out = result.stdout + result.stderr
m = re.search(r'"url"\s*:\s*"([^"]+)"', out)
if m:
    print(f"Created: {m.group(1)}")
else:
    print(f"Output: {out[-200:]}")
