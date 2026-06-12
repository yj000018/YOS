#!/usr/bin/env python3
"""Publish Lakshmi deliverables to Notion."""
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
    ('ECO (Lakshmi) Agent Card v1', '/home/ubuntu/yreg/Lakshmi_Agent_Card_v1.md'),
    ('ECO (Lakshmi) Operating Framework v1', '/home/ubuntu/yreg/Lakshmi_Operating_Framework_v1.md'),
    ('CEO Briefing Standard v1', '/home/ubuntu/yreg/CEO_Briefing_Standard_v1.md'),
    ('Executive Dashboard Framework v1', '/home/ubuntu/yreg/Executive_Dashboard_Framework_v1.md'),
    ('Organization Health KPI Framework v1', '/home/ubuntu/yreg/Organization_Health_KPI_Framework_v1.md'),
    ('Communication Contracts: Executive Coordination', '/home/ubuntu/yreg/Lakshmi_Communication_Contracts_v1.md'),
    ('Capability Roadmap: ECO (Lakshmi)', '/home/ubuntu/yreg/Lakshmi_Capability_Roadmap_v1.md'),
    ('ADR-0013: Creation of ECO (Lakshmi)', '/home/ubuntu/yreg/ADR-0013_Creation_Lakshmi.md'),
    ('ECO Dashboard Design v1', '/home/ubuntu/yreg/ECO_Dashboard_Design_v1.md'),
    ('Executive Open Loops Register v1', '/home/ubuntu/yreg/Open_Loops_Register_v1.md'),
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

with open("/home/ubuntu/yreg/lakshmi_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
