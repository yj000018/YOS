#!/usr/bin/env python3.11
"""
Add merge fields to Knowledge database via Notion REST API.
Run once after initial setup.
"""
import os
import json
import subprocess
import requests

# Get Notion token from MCP config
def get_notion_token():
    """Extract Notion token from MCP config."""
    try:
        result = subprocess.run(
            ["manus-mcp-cli", "tool", "call", "notion-get-users", "--server", "notion",
             "--input", "{}"],
            capture_output=True, text=True, timeout=30
        )
        # Token is in environment or MCP config — use the API via subprocess
        return None
    except Exception:
        return None

KNOWLEDGE_DB_ID = "1895910b-b8d4-4773-85b6-300d01a8d53d"

# New properties to add
NEW_PROPERTIES = {
    "Canonical_Key": {
        "rich_text": {}
    },
    "Evidence_Count": {
        "number": {"format": "number"}
    },
    "First_Seen": {
        "date": {}
    },
    "Last_Seen": {
        "date": {}
    },
    "Validity": {
        "select": {
            "options": [
                {"name": "active", "color": "green"},
                {"name": "superseded", "color": "gray"},
                {"name": "tentative", "color": "yellow"},
                {"name": "archived", "color": "red"}
            ]
        }
    },
    "Merge_Status": {
        "select": {
            "options": [
                {"name": "new", "color": "blue"},
                {"name": "merged", "color": "green"},
                {"name": "updated", "color": "yellow"},
                {"name": "conflicted", "color": "red"}
            ]
        }
    },
    "Conflict_Flag": {
        "checkbox": {}
    }
}

def add_properties_via_mcp():
    """Use notion-update-data-source with one column at a time."""
    ds_id = KNOWLEDGE_DB_ID
    
    columns = [
        ("Canonical_Key", "RICH_TEXT"),
        ("Evidence_Count", "NUMBER"),
        ("First_Seen", "DATE"),
        ("Last_Seen", "DATE"),
        ("Validity", "SELECT('active':green, 'superseded':gray, 'tentative':yellow, 'archived':red)"),
        ("Merge_Status", "SELECT('new':blue, 'merged':green, 'updated':yellow, 'conflicted':red)"),
        ("Conflict_Flag", "CHECKBOX"),
    ]
    
    for col_name, col_type in columns:
        schema = f'ALTER TABLE "Knowledge" ADD COLUMN "{col_name}" {col_type}'
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-update-data-source",
            "--server", "notion",
            "--input", json.dumps({
                "data_source_id": ds_id,
                "schema": schema
            })
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✓ Added: {col_name}")
        else:
            print(f"✗ Failed: {col_name} — {result.stderr[:200]}")

if __name__ == "__main__":
    print("Adding merge fields to Knowledge database...")
    add_properties_via_mcp()
    print("Done.")
