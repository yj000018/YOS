#!/usr/bin/env python3
"""Publish Artifact Layer deliverables to Notion."""
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
    ('Artifact Layer v1', '/home/ubuntu/yreg/Artifact_Layer_v1.md'),
    ('Artifact Catalog v1', '/home/ubuntu/yreg/Artifact_Catalog_v1.md'),
    ('Artifact Status Framework v1', '/home/ubuntu/yreg/Artifact_Status_Framework_v1.md'),
    ('Accept / Reject Framework v1', '/home/ubuntu/yreg/Accept_Reject_Framework_v1.md'),
    ('Artifact Lifecycle Model v1', '/home/ubuntu/yreg/Artifact_Lifecycle_Model_v1.md'),
    ('Artifact-Centric Routing Model v1', '/home/ubuntu/yreg/Artifact_Routing_Model_v1.md'),
    ('ADR-0012: Formalization of the Artifact Layer', '/home/ubuntu/yreg/ADR-0012_Artifact_Layer.md'),
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

with open("/home/ubuntu/yreg/artifact_layer_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
