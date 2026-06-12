#!/usr/bin/env python3
import json, subprocess, re, os

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def notion_create(title, content):
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{"properties": {"title": title}, "content": content}]
    }
    
    # Save payload to temp file
    with open("temp_payload.json", "w") as f:
        json.dump(payload, f)
        
    # Use cat to pipe the JSON into the MCP CLI instead of passing as argument
    # Some CLIs support reading from stdin if --input is omitted or set to -
    cmd = f"cat temp_payload.json | manus-mcp-cli tool call notion-create-pages --server notion --input -"
    
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        out = r.stdout + r.stderr
        
        if "Error" in out or "ERR" in out:
            # Try alternative: passing the raw JSON string in single quotes safely
            json_str = json.dumps(payload).replace("'", "'\\''")
            cmd2 = f"manus-mcp-cli tool call notion-create-pages --server notion --input '{json_str}'"
            r = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=60)
            out = r.stdout + r.stderr
            
        m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
        return m.group(0) if m else f"ERR: {out[-100:]}"
    except Exception as e:
        return f"ERR: {str(e)}"

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
