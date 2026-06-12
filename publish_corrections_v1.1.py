#!/usr/bin/env python3
"""Publish Y-OS v1.1 Architectural Corrections to Notion."""
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def read_file(path):
    with open(path) as f: return f.read()

def notion_create_direct(title, content):
    payload = json.dumps({
        'parent': {'page_id': PARENT_ID},
        'pages': [{'properties': {'title': title}, 'content': content}]
    })
    with open('/tmp/p.json','w') as f: f.write(payload)
    r = subprocess.run(
        ['manus-mcp-cli','tool','call','notion-create-pages','--server','notion','--input', payload],
        capture_output=True, text=True, timeout=90
    )
    out = r.stdout + r.stderr
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f'ERR: {out[-300:]}'

files = [
    ('Architectural Correction Review v1.1', '/home/ubuntu/yreg/Architectural_Correction_Review_v1.1.md'),
    ('Capability Layer Correction v1.1', '/home/ubuntu/yreg/Capability_Layer_Correction_v1.1.md'),
    ('Memory Layer Correction v1.1', '/home/ubuntu/yreg/Memory_Layer_Correction_v1.1.md'),
    ('Layer Architecture Diagram v2.1', '/home/ubuntu/yreg/Layer_Architecture_Diagram_v2.1.md'),
    ('Impact Analysis v1.1', '/home/ubuntu/yreg/Impact_Analysis_v1.1.md'),
    ('ADR-0015: Architectural Layer Corrections', '/home/ubuntu/yreg/ADR-0015_Architectural_Layer_Corrections.md'),
]

urls = {}
for title, path in files:
    print(f'Publishing: {title}...')
    url = notion_create_direct(title, read_file(path))
    urls[title] = url
    print(f'  → {url}')

print("\n=== ALL DELIVERABLES PUBLISHED ===")
for t, u in urls.items():
    print(f"{t}: {u}")

with open("/home/ubuntu/yreg/corrections_v1.1_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
