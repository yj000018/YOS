import subprocess, json, re, os

PARENT_ID = "37d35e218cf88145ac11c5c082b4290b"

docs = [
    {"file": "Y-OS_Foundational_Principles_v1.md", "title": "Y-OS Foundational Principles v1"},
    {"file": "Y-OS_Continuity_Doctrine.md", "title": "Y-OS Continuity Doctrine"},
    {"file": "Y-OS_Artifact-Centric_Manifesto.md", "title": "Y-OS Artifact-Centric Manifesto"},
    {"file": "Y-OS_Architectural_Inversion.md", "title": "Y-OS Architectural Inversion"},
    {"file": "ADR-0021_Foundational_Operational_Principles.md", "title": "ADR-0021: Foundational Operational Principles"},
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
