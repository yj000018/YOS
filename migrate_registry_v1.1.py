import os
import json
import subprocess
import time

def mcp_call(tool_name, payload):
    cmd = [
        "manus-mcp-cli", "tool", "call", tool_name,
        "--server", "notion",
        "--input", json.dumps(payload)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return r.stdout + r.stderr

def fetch_artifacts():
    print("Fetching MISS-E2E-V1 artifacts...")
    payload = {"query": "ART-E2E", "query_type": "internal"}
    out = mcp_call('notion-search', payload)
    
    try:
        json_start = out.find('{"results"')
        if json_start == -1:
            raise ValueError("No JSON found")
        json_str = out[json_start:].split('\nTool execution')[0].strip()
        data = json.loads(json_str)
        
        artifacts = {}
        for r in data.get('results', []):
            title = r.get('title', '')
            if title.startswith('ART-E2E') and '—' not in title:
                art_id = title.split()[0]
                artifacts[art_id] = r.get('id')
        
        return artifacts
    except Exception as e:
        print(f"Error parsing artifacts: {e}")
        return {}

def update_artifact_lineage(page_id, parent_id_str, child_id_strs):
    print(f"Updating lineage for page {page_id}...")
    # Use the correct notion-update-page format: properties is a flat dict of name->value
    properties = {}
    if parent_id_str:
        properties["Parent Artifact ID"] = parent_id_str
    if child_id_strs:
        properties["Child Artifact IDs"] = ", ".join(child_id_strs)
        
    if not properties:
        return
        
    payload = {
        "page_id": page_id,
        "command": "update_properties",
        "properties": properties
    }
    
    out = mcp_call('notion-update-page', payload)
    if "Error" in out and "already" not in out.lower():
        print(f"Error updating page: {out[:200]}")
    else:
        print("Success.")

def main():
    print("Starting Artifact Registry v1.1 Migration...")
    
    # Note: We assume the basic text properties (Parent Artifact ID, Child Artifact IDs) 
    # were already created in the previous step. True relations need UI.
    
    artifacts = fetch_artifacts()
    print(f"Found {len(artifacts)} artifacts.")
    
    if len(artifacts) < 8:
        print("Warning: Did not find all 8 E2E artifacts. Proceeding with what we have.")
        
    lineage_map = {
        "ART-E2E-001": {"parent": None, "children": ["ART-E2E-002"]},
        "ART-E2E-002": {"parent": "ART-E2E-001", "children": ["ART-E2E-003"]},
        "ART-E2E-003": {"parent": "ART-E2E-002", "children": ["ART-E2E-004a", "ART-E2E-004b"]},
        "ART-E2E-004a": {"parent": "ART-E2E-003", "children": []},
        "ART-E2E-004b": {"parent": "ART-E2E-003", "children": ["ART-E2E-005"]},
        "ART-E2E-005": {"parent": "ART-E2E-004b", "children": ["ART-E2E-006", "ART-E2E-007"]},
        "ART-E2E-006": {"parent": "ART-E2E-005", "children": []},
        "ART-E2E-007": {"parent": "ART-E2E-005", "children": []}
    }
    
    for art_id, lineage in lineage_map.items():
        if art_id in artifacts:
            update_artifact_lineage(artifacts[art_id], lineage["parent"], lineage["children"])
            time.sleep(1) # Rate limiting
            
    print("Migration complete.")

if __name__ == "__main__":
    main()
