#!/usr/bin/env python3
"""Publish the 6 deliverables of the Org Placement Review to Notion."""
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
    ('1. Organizational Placement Review: Design & Build', '/home/ubuntu/yreg/L1_Org_Placement_Review.md'),
    ('2. Recommended Structure', '/home/ubuntu/yreg/L2_Recommended_Structure.md'),
    ('3. Advantages and Risks of the Recommended Structure', '/home/ubuntu/yreg/L3_Advantages_Risks.md'),
    ('4. Updated Organizational Diagram', '/home/ubuntu/yreg/L4_Updated_Org_Diagram.md'),
    ('5. Impact on Operational Value Chain', '/home/ubuntu/yreg/L5_Impact_on_OVC.md'),
    ('6. ADR Amendment Recommendation', '/home/ubuntu/yreg/L6_ADR_Recommendation.md'),
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

with open("/home/ubuntu/yreg/org_review_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
