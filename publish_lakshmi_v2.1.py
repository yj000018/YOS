import subprocess, json, re, os

PARENT_ID = "37d35e218cf88145ac11c5c082b4290b"

docs = [
    {"file": "Lakshmi_Runtime_Architecture_v2.1.md", "title": "Lakshmi Runtime Architecture v2.1"},
    {"file": "Lakshmi_Deterministic_Briefing_Design.md", "title": "Deterministic Briefing Design"},
    {"file": "Lakshmi_Mission_Graph_Engine.md", "title": "Mission Graph Engine"},
    {"file": "Lakshmi_Open_Loop_Engine.md", "title": "Open Loop Engine v2.1"},
    {"file": "ADR-0019_Lakshmi_Runtime_v2.1.md", "title": "ADR-0019: Lakshmi Runtime v2.1"},
    {"file": "Validation_Report_Lakshmi_v2.1.md", "title": "Validation Report: Lakshmi Runtime v2.1"},
]

def mcp_call(tool_name, payload):
    cmd = ["manus-mcp-cli", "tool", "call", tool_name, "--server", "notion", "--input", json.dumps(payload)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    return r.stdout + r.stderr

for doc in docs:
    path = f"/home/ubuntu/yreg/{doc['file']}"
    if not os.path.exists(path):
        print(f"⚠️  File not found: {path}")
        continue
    with open(path, 'r') as f:
        content = f.read()
    
    print(f"Publishing {doc['file']}...")
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{
            "properties": {"title": doc['title']},
            "content": content
        }]
    }
    out = mcp_call('notion-create-pages', payload)
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    if m:
        print(f"✅ {doc['title']} -> {m.group(0)}")
    else:
        # Try with data_source_id
        payload2 = {
            "data_source_id": PARENT_ID,
            "pages": [{
                "properties": {"title": doc['title']},
                "content": content
            }]
        }
        out2 = mcp_call('notion-create-pages', payload2)
        m2 = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out2)
        if m2:
            print(f"✅ {doc['title']} -> {m2.group(0)}")
        else:
            print(f"❌ Failed: {out2[:200]}")

print("\nDone.")
