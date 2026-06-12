#!/usr/bin/env python3
import json, subprocess, re, os

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def notion_create(title, content):
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{"properties": {"title": title}, "content": content}]
    }
    
    # Save payload to temp file to avoid escaping issues in shell
    with open("temp_payload.json", "w") as f:
        json.dump(payload, f)
        
    # Read back as single string without shell escaping issues
    with open("temp_payload.json", "r") as f:
        payload_str = f.read()
        
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", payload_str]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = r.stdout + r.stderr
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f"ERR: {out[-80:]}"

with open("cso_deliverables_v2.json", "r") as f:
    pages = json.load(f)

urls = {}
for title, content in pages.items():
    print(f"Creating: {title[:50]}...")
    url = notion_create(title, content)
    urls[title] = url
    print(f"  → {url}")

print("\n=== ALL CSO DELIVERABLES PUBLISHED ===")
for t, u in urls.items():
    print(f"{t[:50]}: {u}")

with open("cso_notion_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
