#!/usr/bin/env python3
"""Publish Y-OS Org Map v2 deliverables to Notion."""
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
    ('Y-OS Org Map v2 (Master Document)', '/home/ubuntu/yreg/Y-OS_Org_Map_v2.md'),
    ('Executive Structure Diagram', '/home/ubuntu/yreg/Executive_Structure_Diagram.md'),
    ('Layer Architecture Diagram', '/home/ubuntu/yreg/Layer_Architecture_Diagram.md'),
    ('Operational Value Chain Diagram', '/home/ubuntu/yreg/OVC_Diagram.md'),
    ('Artifact Layer Diagram', '/home/ubuntu/yreg/Artifact_Layer_Diagram.md'),
    ('Reporting Relationships Matrix', '/home/ubuntu/yreg/Reporting_Matrix.md'),
    ('Role-to-Layer Matrix', '/home/ubuntu/yreg/Role_Layer_Matrix.md'),
    ('Future Architecture Notes', '/home/ubuntu/yreg/Future_Architecture_Notes.md'),
    ('ADR-0014: Y-OS Organizational Map v2', '/home/ubuntu/yreg/ADR-0014_Y-OS_Org_Map_v2.md'),
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

with open("/home/ubuntu/yreg/org_map_v2_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
