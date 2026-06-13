import os
import json
import subprocess
import time

def publish_to_notion(title, content_path):
    print(f"Publishing {content_path}...")
    
    with open(content_path, 'r') as f:
        content = f.read()
        
    payload = {
        "title": title,
        "content": content
    }
    
    input_str = json.dumps(payload)
    
    cmd = [
        "manus-mcp-cli",
        "tool",
        "call",
        "notion-create-page",
        "--server",
        "notion",
        "--input",
        input_str
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Check if the output contains a URL
        for line in result.stdout.split('\n'):
            if "url" in line.lower() or "https://app.notion.com" in line:
                print(f"✅ {title} -> Published successfully")
                return True
        print(f"✅ {title} -> Published (URL not parsed from output)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to publish {title}")
        print(f"Error: {e.stderr}")
        return False

documents = [
    ("Y-OS First Principles v1", "/home/ubuntu/yreg/Y-OS_First_Principles_v1.md"),
    ("Y-OS Definition v1", "/home/ubuntu/yreg/Y-OS_Definition_v1.md"),
    ("Y-OS Continuity Doctrine", "/home/ubuntu/yreg/Y-OS_Continuity_Doctrine_v2.md"),
    ("Y-OS Artifact-Centric Manifesto", "/home/ubuntu/yreg/Y-OS_Artifact-Centric_Manifesto_v2.md"),
    ("Y-OS Operational Cycle v1", "/home/ubuntu/yreg/Y-OS_Operational_Cycle_v1.md"),
    ("Y-OS Layer Model v1", "/home/ubuntu/yreg/Y-OS_Layer_Model_v1.md"),
    ("Y-OS Governance Doctrine", "/home/ubuntu/yreg/Y-OS_Governance_Doctrine.md"),
    ("ADR-0021: Foundational Doctrine", "/home/ubuntu/yreg/ADR-0021_Foundational_Doctrine.md")
]

for title, path in documents:
    if os.path.exists(path):
        publish_to_notion(title, path)
        time.sleep(2)  # Rate limiting
    else:
        print(f"⚠️ File not found: {path}")

print("Done.")
