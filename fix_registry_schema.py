#!/usr/bin/env python3
"""
Fix Artifact Registry Schema:
1. Add 'Parent Artifact' relation property (self-referencing)
2. Add 'Child Artifacts' relation property (self-referencing)
3. Fix Status options to match the Y-OS state machine
   (Draft, Ready For Review, Accepted, Rejected, Consumed, Superseded, Archived)
4. Add missing date fields: Accepted Date, Consumed Date, Archived Date
5. Add Review Owner select field
"""
import json, subprocess, re

DB_ID = "4ae2fa35-d24f-4c44-be88-dbb808ea14cd"  # collection ID

def mcp_call(tool, payload):
    r = subprocess.run(
        ['manus-mcp-cli', 'tool', 'call', tool, '--server', 'notion', '--input', json.dumps(payload)],
        capture_output=True, text=True, timeout=90
    )
    return r.stdout + r.stderr

# Notion MCP uses SQL DDL for schema updates
# We need to:
# 1. Add date columns (Accepted Date, Consumed Date, Archived Date)
# 2. Add Review Owner select
# 3. Add Parent Artifact (text — Notion MCP doesn't support self-referencing relations via DDL, use text as proxy)
# Note: True Notion Relation properties require the Notion API directly or UI.
# For MVP, we use TEXT fields for Parent/Child and note the limitation.

print("Updating Artifact Registry schema...")

# Add missing fields via ALTER TABLE
ddl_statements = [
    # Date fields for state transition tracking
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Accepted Date" DATE;',
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Consumed Date" DATE;',
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Archived Date" DATE;',
    # Review Owner
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Review Owner" SELECT(\'CEO\':gray, \'Krishna\':blue, \'Ganesha\':green, \'Brahma\':purple, \'Hanuman\':orange, \'Saraswati\':pink, \'Lakshmi\':yellow);',
    # Parent/Child as text (proxy for relation — true Relation not supported via DDL)
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Parent Artifact ID" TEXT;',
    f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Child Artifact IDs" TEXT;',
]

results = []
for ddl in ddl_statements:
    print(f"  Executing: {ddl[:80]}...")
    payload = {"data_source_id": DB_ID, "schema": ddl}
    out = mcp_call('notion-update-data-source', payload)
    # Check for success
    if 'Updated data source' in out or 'updated' in out.lower():
        status = "✅ OK"
    elif 'already exists' in out.lower():
        status = "⚠️ Already exists"
    else:
        status = f"❌ {out[-150:]}"
    results.append((ddl[:60], status))
    print(f"    → {status}")

print("\n=== Schema Update Summary ===")
for ddl, status in results:
    print(f"{status} | {ddl}")

# Now update Status options to match Y-OS state machine
# The current Status is a Notion "status" type which has limited customization via DDL
# We'll add the correct options via a separate DDL
print("\nUpdating Status options...")
status_ddl = (
    f'ALTER TABLE "collection://{DB_ID}" '
    'MODIFY COLUMN "Status" SELECT('
    "'Draft':gray, "
    "'Ready For Review':yellow, "
    "'Accepted':green, "
    "'Rejected':red, "
    "'Consumed':blue, "
    "'Superseded':orange, "
    "'Archived':default"
    ');'
)
payload = {"data_source_id": DB_ID, "schema": status_ddl}
out = mcp_call('notion-update-data-source', payload)
if 'Updated' in out or 'updated' in out.lower():
    print("  ✅ Status options updated")
else:
    print(f"  ⚠️ Status update result: {out[-200:]}")
    print("  Note: Notion 'status' type has fixed groups. Using SELECT type as workaround.")
    # Fallback: add a separate ArtifactStatus select column
    fallback_ddl = (
        f'ALTER TABLE "collection://{DB_ID}" ADD COLUMN "Artifact Status" SELECT('
        "'Draft':gray, "
        "'Ready For Review':yellow, "
        "'Accepted':green, "
        "'Rejected':red, "
        "'Consumed':blue, "
        "'Superseded':orange, "
        "'Archived':default"
        ');'
    )
    payload2 = {"data_source_id": DB_ID, "schema": fallback_ddl}
    out2 = mcp_call('notion-update-data-source', payload2)
    if 'Updated' in out2 or 'already exists' in out2.lower():
        print("  ✅ Artifact Status (SELECT) column added as fallback")
    else:
        print(f"  ❌ Fallback failed: {out2[-150:]}")

print("\nSchema fix complete.")
