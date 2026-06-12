#!/usr/bin/env python3
"""Publish Hanuman deliverables to Notion."""
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
    ('Lead Developer (Hanuman) Agent Card v1', '/home/ubuntu/yreg/Hanuman_Agent_Card_v1.md'),
    ('Lead Developer (Hanuman) Operating Framework v1', '/home/ubuntu/yreg/Hanuman_Operating_Framework_v1.md'),
    ('Build Package Standard v1', '/home/ubuntu/yreg/Build_Package_Standard_v1.md'),
    ('Build KPI Framework v1', '/home/ubuntu/yreg/Build_KPI_Framework_v1.md'),
    ('Capability Roadmap: Lead Developer (Hanuman)', '/home/ubuntu/yreg/Hanuman_Capability_Roadmap_v1.md'),
    ('Communication Contracts: Build Phase', '/home/ubuntu/yreg/Hanuman_Communication_Contracts_v1.md'),
    ('ADR-0011: Creation of Lead Developer (Hanuman)', '/home/ubuntu/yreg/ADR-0011_Creation_Hanuman.md'),
    ('Title Recommendation: Hanuman', '/home/ubuntu/yreg/Hanuman_Title_Recommendation.md'),
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

with open("/home/ubuntu/yreg/hanuman_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
