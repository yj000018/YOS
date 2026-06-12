#!/usr/bin/env python3
"""Update Artifact Registry Schema and publish Lakshmi Runtime docs."""
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"
DB_ID = "8cd17557340e434698507291face328e" # Registry DB created previously

def mcp_call(tool, payload):
    r = subprocess.run(
        ['manus-mcp-cli', 'tool', 'call', tool, '--server', 'notion', '--input', json.dumps(payload)],
        capture_output=True, text=True, timeout=90
    )
    return r.stdout + r.stderr

def notion_create_page(title, content):
    payload = {
        'parent': {'page_id': PARENT_ID},
        'pages': [{'properties': {'title': title}, 'content': content}]
    }
    out = mcp_call('notion-create-pages', payload)
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f'ERR: {out[-200:]}'

# Step 1: Update the Database Schema via SQL DDL
# Note: notion-update-data-source tool uses SQL DDL to alter tables
print("Updating Artifact Registry Schema (v1.1 Patch)...")
schema_update = (
    f"ALTER TABLE \"collection://{DB_ID}\" "
    "ADD COLUMN \"Review Owner\" SELECT('CEO':gray, 'Krishna':blue, 'Ganesha':green, 'Brahma':purple, 'Hanuman':orange, 'Saraswati':pink, 'Lakshmi':yellow, 'System':default); "
    f"ALTER TABLE \"collection://{DB_ID}\" ADD COLUMN \"Accepted Date\" DATE; "
    f"ALTER TABLE \"collection://{DB_ID}\" ADD COLUMN \"Consumed Date\" DATE; "
    f"ALTER TABLE \"collection://{DB_ID}\" ADD COLUMN \"Archived Date\" DATE;"
)
update_payload = {
    "data_source_id": DB_ID,
    "schema": schema_update
}
update_result = mcp_call('notion-update-data-source', update_payload)
print(update_result[:300])

# Step 2: Publish all 8 documents
files = [
    ('Artifact Schema v1.1 (Patch)', '/home/ubuntu/yreg/Artifact_Schema_v1.1_Patch.md'),
    ('Lakshmi Runtime Architecture v1', '/home/ubuntu/yreg/Lakshmi_Runtime_Architecture_v1.md'),
    ('Dashboard Data Model v1', '/home/ubuntu/yreg/Lakshmi_Dashboard_Data_Model_v1.md'),
    ('Open Loops Engine v1', '/home/ubuntu/yreg/Lakshmi_Open_Loops_Engine_v1.md'),
    ('CEO Briefing Generator v1', '/home/ubuntu/yreg/Lakshmi_CEO_Briefing_Generator_v1.md'),
    ('Alert Rules v1', '/home/ubuntu/yreg/Lakshmi_Alert_Rules_v1.md'),
    ('Cost Monitoring Model v1', '/home/ubuntu/yreg/Lakshmi_Cost_Monitoring_Model_v1.md'),
    ('ADR-0017: Lakshmi MVP Runtime', '/home/ubuntu/yreg/ADR-0017_Lakshmi_MVP_Runtime.md'),
]

urls = {}
for title, path in files:
    print(f'Publishing: {title}...')
    with open(path) as f: content = f.read()
    url = notion_create_page(title, content)
    urls[title] = url
    print(f'  → {url}')

print("\n=== ALL DELIVERABLES ===")
for t, u in urls.items():
    print(f"{t}: {u}")

with open("/home/ubuntu/yreg/lakshmi_runtime_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
