#!/usr/bin/env python3
"""Create the Y-OS Artifact Registry Notion Database and publish all 8 docs."""
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

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

# Step 1: Create the Database using correct SQL syntax with single quotes
schema = (
    "CREATE TABLE \"Y-OS Artifact Registry\" ("
    "\"Name\" TITLE, "
    "\"Artifact Type\" SELECT('Strategy Brief':blue, 'Execution Plan':green, 'Architecture Package':purple, 'Build Artifact':orange, 'Build Report':orange, 'Delivery Report':red, 'Learning Report':yellow), "
    "\"Mission ID\" RICH_TEXT, "
    "\"Producer\" SELECT('CEO':gray, 'Krishna':blue, 'Ganesha':green, 'Brahma':purple, 'Hanuman':orange, 'Saraswati':pink, 'Lakshmi':yellow), "
    "\"Consumer\" SELECT('CEO':gray, 'Krishna':blue, 'Ganesha':green, 'Brahma':purple, 'Hanuman':orange, 'Saraswati':pink, 'Lakshmi':yellow, 'System':default), "
    "\"Status\" STATUS, "
    "\"Version\" RICH_TEXT, "
    "\"URI\" URL, "
    "\"Acceptance Notes\" RICH_TEXT, "
    "\"Rejection Notes\" RICH_TEXT"
    ")"
)

print("Creating Artifact Registry Database...")
db_payload = {
    "parent": {"page_id": PARENT_ID},
    "title": "Y-OS Artifact Registry",
    "schema": schema
}
db_result = mcp_call('notion-create-database', db_payload)
print(db_result[:500])

# Extract DB URL
m = re.search(r'https://app\.notion\.com/[^\s\)]+', db_result)
db_url = m.group(0) if m else "DB URL not found"
print(f"DB URL: {db_url}")

# Step 2: Publish all 8 design documents
files = [
    ('Artifact Registry Architecture v1', '/home/ubuntu/yreg/Artifact_Registry_Architecture_v1.md'),
    ('Artifact Schema v1', '/home/ubuntu/yreg/Artifact_Schema_v1.md'),
    ('Artifact State Machine v1', '/home/ubuntu/yreg/Artifact_State_Machine_v1.md'),
    ('Notion Database Design v1', '/home/ubuntu/yreg/Notion_Database_Design_v1.md'),
    ('Artifact API Model v1', '/home/ubuntu/yreg/Artifact_API_Model_v1.md'),
    ('Artifact Query Model v1', '/home/ubuntu/yreg/Artifact_Query_Model_v1.md'),
    ('Artifact Lifecycle Operations v1', '/home/ubuntu/yreg/Artifact_Lifecycle_Operations_v1.md'),
    ('ADR-0016: Artifact Registry', '/home/ubuntu/yreg/ADR-0016_Artifact_Registry.md'),
]

urls = {'DB': db_url}
for title, path in files:
    print(f'Publishing: {title}...')
    with open(path) as f: content = f.read()
    url = notion_create_page(title, content)
    urls[title] = url
    print(f'  → {url}')

print("\n=== ALL DELIVERABLES ===")
for t, u in urls.items():
    print(f"{t}: {u}")

with open("/home/ubuntu/yreg/artifact_registry_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
