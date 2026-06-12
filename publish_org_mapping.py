import json, subprocess, os

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c" # System Architecture

with open("/home/ubuntu/yreg/Y-OS_Organizational_Mapping_v1.md") as f:
    content = f.read()

payload = {
    "parent": {"page_id": PARENT_ID},
    "pages": [
        {
            "properties": {"title": "🏢 Y-OS Organizational Mapping v1"},
            "content": content
        }
    ]
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages", "--server", "notion", "--input", json.dumps(payload)]
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
