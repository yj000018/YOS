#!/usr/bin/env python3
"""Publish Operational Value Chain v1 deliverables to Notion."""
import json, subprocess, re, os

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def notion_create(title, content):
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{"properties": {"title": title}, "content": content}]
    }
    
    with open("/tmp/ovc_payload.json", "w") as f:
        json.dump(payload, f)
        
    cmd = "cat /tmp/ovc_payload.json | manus-mcp-cli tool call notion-create-pages --server notion --input -"
    
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        out = r.stdout + r.stderr
        
        if "Error" in out or "ERR" in out or "error" in out.lower():
            json_str = json.dumps(payload).replace("'", "'\\''")
            cmd2 = f"manus-mcp-cli tool call notion-create-pages --server notion --input '{json_str}'"
            r = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=90)
            out = r.stdout + r.stderr
            
        m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
        return m.group(0) if m else f"ERR: {out[-200:]}"
    except Exception as e:
        return f"ERR: {str(e)}"

BASE = "/home/ubuntu/yreg"

deliverables = [
    ("Y-OS Operational Value Chain v1", f"{BASE}/Y-OS_Operational_Value_Chain_v1.md"),
    ("Role Definitions v1 — OVC", f"{BASE}/Role_Definitions_v1.md"),
    ("Communication Contracts v1 — OVC", f"{BASE}/Communication_Contracts_v1.md"),
    ("Governance Model v1 — OVC", f"{BASE}/Governance_Model_v1.md"),
    ("Strategic-to-Execution Flow v1", f"{BASE}/Strategic_Execution_Flow_v1.md"),
    ("Future Organization Expansion v1", f"{BASE}/Future_Org_Expansion_v1.md"),
    ("ADR-0009: Operational Value Chain", f"{BASE}/ADR-0009_Operational_Value_Chain.md"),
]

urls = {}
for title, path in deliverables:
    print(f"Publishing: {title}...")
    content = read_file(path)
    url = notion_create(title, content)
    urls[title] = url
    print(f"  → {url}")

print("\n=== OVC DELIVERABLES PUBLISHED ===")
for t, u in urls.items():
    print(f"{t[:60]}: {u}")

with open(f"{BASE}/ovc_notion_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
