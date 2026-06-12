#!/usr/bin/env python3
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c" # System Architecture

def create_page(title, icon, content_file):
    with open(content_file, "r") as f:
        content = f.read()
    
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{
            "properties": {"title": title},
            "icon": icon,
            "content": content
        }]
    }
    
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    m = re.search(r'"url"\s*:\s*"([^"]+)"', out)
    if m:
        print(f"Created {title}: {m.group(1)}")
    else:
        print(f"Failed {title}: {out[-200:]}")

print("Publishing CODO documents to Notion...")
create_page("Y-OS Organizational Model v1", "🏢", "/home/ubuntu/yreg/Y-OS_Organizational_Model_v1.md")
create_page("CODO Agent Card — Saraswati", "🦉", "/home/ubuntu/yreg/Saraswati_CODO_Profile.md")
create_page("ADR-000X — Creation of the CODO Role", "🏛️", "/home/ubuntu/yreg/ADR-000X_Creation_CODO_Role.md")
print("Done.")
