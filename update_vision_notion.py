#!/usr/bin/env python3
import json, subprocess

PAGE_ID = "37d35e218cf8814aa50dc5dadb9f20db"

with open("/home/ubuntu/yreg/Y-OS_Vision_First_Principles_v2.md", "r") as f:
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
    print(f"Failed to update Vision: {out[-200:]}")
else:
    print("Successfully updated Vision in Notion.")
