#!/usr/bin/env python3
"""
Y-REG Seed v2 Fixed — Add Y-CTX, Y-ID, Y-LOG + relations + capabilities
Uses proper UUID-based IDs consistent with existing schema.
"""
import subprocess, json

def mcp_sql(sql):
    payload = {"project_id": "zcgqqzlxzcxkswwlbxhc", "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    for line in output.split('\n'):
        if '"result"' in line:
            try:
                data = json.loads(line.split('Tool execution result:\n')[-1].strip())
                return data.get('result', line)
            except:
                pass
    return output[-300:]

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Get existing object IDs
# ─────────────────────────────────────────────────────────────────────────────
print("=== Step 1: Get existing IDs ===")
raw = mcp_sql("SELECT id, name, slug FROM yreg_objects ORDER BY name;")
# Parse the JSON result
import re
match = re.search(r'\[.*\]', str(raw), re.DOTALL)
existing = {}
if match:
    try:
        objects = json.loads(match.group())
        for obj in objects:
            existing[obj['name']] = obj['id']
            if obj.get('slug'):
                existing[obj['slug']] = obj['id']
        print(f"  Found {len(objects)} existing objects")
        for o in objects:
            print(f"    {o['name']}: {o['id']}")
    except Exception as e:
        print(f"  Parse error: {e}, raw: {str(raw)[:200]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Insert Y-CTX, Y-ID, Y-LOG with gen_random_uuid()
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 2: Insert Y-CTX, Y-ID, Y-LOG ===")

new_modules = [
    {
        "name": "Y-CTX",
        "slug": "yctx",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Context extraction and assembly module. Produces Context Packs for Y-ORC.",
        "metadata": {"question": "What context is relevant?", "module_owner": "Y-CTX",
                     "equivalent_role": "Analyst, Briefing Officer", "tags": ["core", "context", "deterministic"]}
    },
    {
        "name": "Y-ID",
        "slug": "yid",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Naming, namespaces and identifier management module.",
        "metadata": {"question": "How do we identify things?", "module_owner": "Y-ID",
                     "equivalent_role": "Information Architect", "tags": ["core", "identity", "deterministic"]}
    },
    {
        "name": "Y-LOG",
        "slug": "ylog",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "version": "1.0",
        "description": "Audit trail and operational history module. Records Mission Pack executions.",
        "metadata": {"question": "What happened?", "module_owner": "Y-LOG",
                     "equivalent_role": "Auditor, Operations Recorder", "tags": ["core", "audit", "deterministic"]}
    }
]

new_ids = {}
for m in new_modules:
    meta = json.dumps(m['metadata']).replace("'", "''")
    sql = f"""
INSERT INTO yreg_objects (name, slug, type, status, visibility, version, description, metadata)
VALUES (
    '{m['name']}', '{m['slug']}', '{m['type']}', '{m['status']}',
    '{m['visibility']}', '{m['version']}', '{m['description']}', '{meta}'::jsonb
)
ON CONFLICT (slug) DO UPDATE SET
    description = EXCLUDED.description,
    metadata = EXCLUDED.metadata,
    updated_at = NOW()
RETURNING id, name;
"""
    result = mcp_sql(sql)
    match = re.search(r'\[.*?\]', str(result), re.DOTALL)
    if match:
        try:
            rows = json.loads(match.group())
            if rows:
                new_ids[m['name']] = rows[0]['id']
                print(f"  [{m['name']}] id={rows[0]['id']}")
        except:
            print(f"  [{m['name']}] result: {str(result)[:100]}")
    else:
        print(f"  [{m['name']}] no RETURNING result: {str(result)[:100]}")

# Merge all IDs
all_ids = {**existing, **new_ids}
print(f"\n  Total IDs available: {len(all_ids)}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Insert Relations (using resolved UUIDs)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 3: Insert Relations ===")

# Map friendly names to IDs
def get_id(name):
    return all_ids.get(name) or all_ids.get(name.lower())

relations = [
    ("Y-CTX", "Manus Memory", "reads", "Y-CTX reads Y-MEM to assemble context"),
    ("Y-CTX", "Y-REG", "produces_for", "Y-CTX produces Context Pack consumed by Y-ORC"),
    ("Y-REG", "Y-REG Sync", "triggers", "Y-REG triggers sync workflow on update"),
    ("/YOS", "Y-REG", "reads", "/YOS reads Y-REG for launcher display"),
    ("Y-DEV", "Y-REG", "registers_into", "Y-DEV registers completed objects into Y-REG"),
]

for source_name, target_name, rel_type, desc in relations:
    source_id = get_id(source_name)
    target_id = get_id(target_name)
    if not source_id or not target_id:
        print(f"  SKIP [{source_name} → {target_name}]: ID not found (src={source_id}, tgt={target_id})")
        continue
    sql = f"""
INSERT INTO yreg_relations (source_id, target_id, relation_type, description)
VALUES ('{source_id}', '{target_id}', '{rel_type}', '{desc}')
ON CONFLICT DO NOTHING
RETURNING id;
"""
    result = mcp_sql(sql)
    match = re.search(r'\[.*?\]', str(result), re.DOTALL)
    if match:
        print(f"  OK [{source_name} → {target_name}] ({rel_type})")
    else:
        print(f"  [{source_name} → {target_name}] {str(result)[:80]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Insert Capabilities
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 4: Insert Capabilities ===")

capabilities = [
    ("Y-CTX", "Context Assembly", "Assembles Context Pack from memory for a given situation"),
    ("Y-ID", "Identifier Resolution", "Resolves slugs and names to canonical object IDs"),
    ("Y-LOG", "Audit Logging", "Records append-only execution events and operational history"),
    ("Y-REG", "Registry Lookup", "Returns available capabilities and system objects"),
    ("memory-manager", "Memory Management", "Stores and retrieves persistent memory across sessions"),
]

for owner_name, cap_name, cap_desc in capabilities:
    owner_id = get_id(owner_name)
    if not owner_id:
        print(f"  SKIP [{cap_name}]: owner '{owner_name}' not found")
        continue
    sql = f"""
INSERT INTO yreg_capabilities (object_id, name, description)
VALUES ('{owner_id}', '{cap_name}', '{cap_desc}')
ON CONFLICT DO NOTHING
RETURNING id;
"""
    result = mcp_sql(sql)
    match = re.search(r'\[.*?\]', str(result), re.DOTALL)
    if match:
        print(f"  OK [{cap_name}] owned by {owner_name}")
    else:
        print(f"  [{cap_name}] {str(result)[:80]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Final counts
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 5: Final Counts ===")
result = mcp_sql("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as objects,
    (SELECT COUNT(*) FROM yreg_relations) as relations,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities;
""")
match = re.search(r'\[.*?\]', str(result), re.DOTALL)
if match:
    try:
        rows = json.loads(match.group())
        if rows:
            r = rows[0]
            print(f"  objects={r['objects']}  relations={r['relations']}  capabilities={r['capabilities']}")
    except:
        print(result)
else:
    print(result)

print("\n=== Seed v2 Complete ===")
