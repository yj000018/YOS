#!/usr/bin/env python3
"""Seed ART-DEMO-001 into the real Notion Artifact Registry."""
import subprocess, json

NOTION_DB_ID = "8cd17557-340e-4346-9850-7291face328e"

payload = {
    "pages": [{
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "title": "ART-DEMO-001 — Y-ORC Runtime v1 Validation",
            "Status": "Not started",
            "Artifact Type": "Execution Plan",
            "Producer": "CEO",
            "Consumer": "System",
            "Mission ID": "MISS-YORC-V1-DEMO",
            "Acceptance Notes": "generate_report",
            "Version": "v1.0"
        },
        "content": (
            "## ART-DEMO-001 — Y-ORC Runtime v1 Validation\n\n"
            "**Purpose:** Validate that Y-ORC Runtime v1 can autonomously detect this artifact, "
            "resolve the `generate_report` capability, invoke Ganesha, and produce ART-DEMO-002.\n\n"
            "**Trigger Conditions:**\n"
            "- Status: Not started\n"
            "- Consumer: System\n"
            "- Capability: generate_report\n\n"
            "**Expected Output:** A new Build Report artifact (ART-DEMO-002) created in the Registry "
            "with this artifact as parent, and this artifact marked Done.\n\n"
            "**Mission:** MISS-YORC-V1-DEMO\n"
        ),
        "icon": "🧪"
    }]
}

r = subprocess.run(
    ["manus-mcp-cli", "tool", "call", "notion-create-pages",
     "--server", "notion", "--input", json.dumps(payload)],
    capture_output=True, text=True
)
print(r.stdout)
