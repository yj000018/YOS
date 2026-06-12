#!/usr/bin/env python3
"""Publish Lakshmi v1.1 Addendum deliverables to Notion."""
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
    ('ECO (Lakshmi) Agent Card v1.1 (Patch)', '/home/ubuntu/yreg/Lakshmi_Agent_Card_v1.1_Patch.md'),
    ('Foundational Continuity Principle (Law #11)', '/home/ubuntu/yreg/Foundational_Continuity_Principle.md'),
    ('Y-OS Layer Model v2 (Preview)', '/home/ubuntu/yreg/Y-OS_Layer_Model_v2_Preview.md'),
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

with open("/home/ubuntu/yreg/addendum_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
