import os
import json
import subprocess
import time

PARENT_PAGE_ID = "37635e218cf8817e8781fb0a43b48146"  # System Architecture page

def mcp_call(tool_name, payload):
    cmd = [
        "manus-mcp-cli", "tool", "call", tool_name,
        "--server", "notion",
        "--input", json.dumps(payload)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return r.stdout + r.stderr

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def publish_page(title, content):
    payload = {
        "parent_id": PARENT_PAGE_ID,
        "title": title,
        "content": content
    }
    out = mcp_call('notion-create-pages', payload)
    try:
        json_start = out.find('{"results"')
        if json_start == -1:
            json_start = out.find('[{"id"')
        if json_start == -1:
            json_start = out.find('{"id"')
        if json_start != -1:
            data = json.loads(out[json_start:].split('\nTool')[0].strip())
            if isinstance(data, list) and data:
                url = data[0].get('url', 'N/A')
            elif isinstance(data, dict):
                url = data.get('url', 'N/A')
            else:
                url = 'N/A'
            print(f"Published: {title} -> {url}")
            return url
    except Exception as e:
        print(f"Error parsing result for {title}: {e}")
    print(f"Published: {title} (URL not parsed)")
    return 'N/A'

def update_notion_db_schema():
    print("Updating Notion DB schema for v1.1...")
    DB_ID = "4ae2fa35-d24f-4c44-be88-dbb808ea14cd"
    
    # Add new properties via DDL
    new_props = """
ALTER TABLE "collection://4ae2fa35-d24f-4c44-be88-dbb808ea14cd"
ADD COLUMN "Mission Name" TEXT;
ADD COLUMN "Ready For Review Date" DATE;
ADD COLUMN "Open Loop Flag" CHECKBOX;
ADD COLUMN "Blocking Issue" TEXT;
ADD COLUMN "Related ADRs" TEXT;
ADD COLUMN "Related Laws" TEXT;
"""
    payload = {
        "data_source_id": DB_ID,
        "operations": [
            {"type": "add_property", "name": "Mission Name", "property_type": "text"},
            {"type": "add_property", "name": "Ready For Review Date", "property_type": "date"},
            {"type": "add_property", "name": "Open Loop Flag", "property_type": "checkbox"},
            {"type": "add_property", "name": "Blocking Issue", "property_type": "text"},
            {"type": "add_property", "name": "Related ADRs", "property_type": "text"},
            {"type": "add_property", "name": "Related Laws", "property_type": "text"}
        ]
    }
    out = mcp_call('notion-update-data-source', payload)
    if "Error" in out and "already exists" not in out.lower():
        print(f"Schema update warning: {out[:300]}")
    else:
        print("Schema update: OK")

def main():
    print("=== ARTIFACT REGISTRY v1.1 — PUBLICATION START ===")
    
    # 1. Update DB schema
    update_notion_db_schema()
    time.sleep(2)
    
    # 2. Publish all 8 deliverables
    deliverables = [
        ("Artifact Lineage Model v1", "/home/ubuntu/yreg/Artifact_Lineage_Model_v1.md"),
        ("Registry Schema v1.1", "/home/ubuntu/yreg/Registry_Schema_v1.1.md"),
        ("Notion Database Update Plan", "/home/ubuntu/yreg/Notion_Database_Update_Plan.md"),
        ("Artifact Lineage Views", "/home/ubuntu/yreg/Artifact_Lineage_Views.md"),
        ("Runtime Query Model", "/home/ubuntu/yreg/Runtime_Query_Model.md"),
        ("Validation Rules", "/home/ubuntu/yreg/Validation_Rules.md"),
        ("Migration Plan: MISS-E2E-V1", "/home/ubuntu/yreg/Migration_Plan.md"),
        ("ADR-0017: Artifact Lineage & Registry v1.1", "/home/ubuntu/yreg/ADR-0017_Artifact_Lineage_Registry_v1.1.md"),
    ]
    
    for title, path in deliverables:
        content = read_file(path)
        publish_page(title, content)
        time.sleep(1)
    
    print("=== PUBLICATION COMPLETE ===")

if __name__ == "__main__":
    main()
