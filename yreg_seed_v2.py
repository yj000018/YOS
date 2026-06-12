#!/usr/bin/env python3
"""
Y-REG Seed v2 — Add Y-CTX, Y-ID, Y-LOG + relations + capabilities
"""
import subprocess, json, sys

def mcp_sql(sql):
    payload = {"project_id": "zcgqqzlxzcxkswwlbxhc", "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    # Extract result
    for line in output.split('\n'):
        if 'Tool execution result:' in line:
            return line
    return output[-200:]

print("=== Phase 1: Seed Y-CTX, Y-ID, Y-LOG ===")

new_objects = [
    {
        "id": "protocol--yctx",
        "type": "protocol",
        "name": "Y-CTX",
        "slug": "yctx",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Context extraction and assembly module. Reads Y-MEM and produces Context Packs consumed by Y-ORC.",
        "question": "What context is relevant?",
        "module_owner": "Y-CTX",
        "tags": ["core", "context", "deterministic", "backend"]
    },
    {
        "id": "protocol--yid",
        "type": "protocol",
        "name": "Y-ID",
        "slug": "yid",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Naming, namespaces and identifier management module. Ensures consistent naming across all Y-OS objects.",
        "question": "How do we identify things?",
        "module_owner": "Y-ID",
        "tags": ["core", "identity", "naming", "deterministic", "backend"]
    },
    {
        "id": "protocol--ylog",
        "type": "protocol",
        "name": "Y-LOG",
        "slug": "ylog",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Audit trail and operational history module. Records Mission Pack executions.",
        "question": "What happened?",
        "module_owner": "Y-LOG",
        "tags": ["core", "audit", "logging", "deterministic", "backend"]
    }
]

for obj in new_objects:
    tags_json = json.dumps(obj["tags"]).replace("'", "''")
    sql = f"""
INSERT INTO yreg_objects (id, type, name, slug, status, visibility, version, description, metadata)
VALUES (
    '{obj["id"]}',
    '{obj["type"]}',
    '{obj["name"]}',
    '{obj["slug"]}',
    '{obj["status"]}',
    '{obj["visibility"]}',
    '{obj["version"]}',
    '{obj["description"]}',
    '{{"question": "{obj["question"]}", "module_owner": "{obj["module_owner"]}", "tags": {json.dumps(obj["tags"])}}}'::jsonb
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    metadata = EXCLUDED.metadata,
    updated_at = NOW();
"""
    result = mcp_sql(sql)
    print(f"  [{obj['name']}] {result.strip()[:80]}")

print("\n=== Phase 2: Add Relations ===")

relations = [
    # Y-CTX reads Y-MEM
    ("protocol--yctx", "protocol--ymem", "reads", "Y-CTX reads Y-MEM to assemble context"),
    # Y-CTX feeds Y-ORC
    ("protocol--yctx", "protocol--yorc", "produces_for", "Y-CTX produces Context Pack for Y-ORC"),
    # Y-ORC feeds Y-LOG
    ("protocol--yorc", "protocol--ylog", "emits_to", "Y-ORC emits execution events to Y-LOG"),
    # Y-ID governs Y-REG naming
    ("protocol--yid", "protocol--yreg", "governs", "Y-ID governs naming conventions in Y-REG"),
    # Y-ORC reads Y-REG
    ("protocol--yorc", "protocol--yreg", "reads", "Y-ORC reads Y-REG for available tools"),
    # Y-ORC reads Y-CTX output
    ("protocol--yorc", "protocol--yctx", "consumes", "Y-ORC consumes Context Pack from Y-CTX"),
    # /YOS reads Y-REG
    ("command--yos-launcher", "protocol--yreg", "reads", "/YOS reads Y-REG for display"),
    # Y-DEV registers into Y-REG
    ("protocol--ydev", "protocol--yreg", "registers_into", "Y-DEV registers completed objects into Y-REG"),
    # Y-CAP triggers Y-DEV
    ("protocol--ycap", "protocol--ydev", "triggers", "Y-CAP triggers Y-DEV for custom development"),
]

for source, target, rel_type, desc in relations:
    sql = f"""
INSERT INTO yreg_relations (source_id, target_id, relation_type, description)
VALUES ('{source}', '{target}', '{rel_type}', '{desc}')
ON CONFLICT DO NOTHING;
"""
    result = mcp_sql(sql)
    print(f"  [{source} → {target}] {result.strip()[:60]}")

print("\n=== Phase 3: Add Capabilities ===")

capabilities = [
    ("cap--context-assembly", "protocol--yctx", "Context Assembly", "Assembles Context Pack from Y-MEM for a given situation"),
    ("cap--identifier-resolution", "protocol--yid", "Identifier Resolution", "Resolves slugs and names to canonical object IDs"),
    ("cap--audit-logging", "protocol--ylog", "Audit Logging", "Records append-only execution events and operational history"),
    ("cap--registry-lookup", "protocol--yreg", "Registry Lookup", "Returns available capabilities and system objects"),
    ("cap--workflow-orchestration", "protocol--yorc", "Workflow Orchestration", "Routes and executes workflow plans from Mission Packs"),
]

for cap_id, owner_id, cap_name, cap_desc in capabilities:
    sql = f"""
INSERT INTO yreg_capabilities (id, object_id, name, description)
VALUES ('{cap_id}', '{owner_id}', '{cap_name}', '{cap_desc}')
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;
"""
    result = mcp_sql(sql)
    print(f"  [{cap_name}] {result.strip()[:60]}")

print("\n=== Phase 4: Verification ===")

counts = mcp_sql("SELECT 'objects' as tbl, COUNT(*) as n FROM yreg_objects UNION ALL SELECT 'relations', COUNT(*) FROM yreg_relations UNION ALL SELECT 'capabilities', COUNT(*) FROM yreg_capabilities;")
print(counts)

print("\n=== Done ===")
