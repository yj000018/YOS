#!/usr/bin/env python3
"""
Y-REG Seed v3 — Correct schema:
  yreg_objects: id(uuid), slug, name, type, status, visibility, registration_stage, description, tags[], git_path, version
  yreg_relations: id(uuid), source_slug, target_slug, relation_type
  yreg_capabilities: id(uuid), slug, name, input_schema, output_schema, implemented_by[]
"""
import subprocess, json, re

def mcp_sql(sql):
    payload = {"project_id": "zcgqqzlxzcxkswwlbxhc", "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    match = re.search(r'\[.*?\]', output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return output[-200:]

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Insert Y-CTX, Y-ID, Y-LOG
# ─────────────────────────────────────────────────────────────────────────────
print("=== Step 1: Seed Y-CTX, Y-ID, Y-LOG ===")

new_modules = [
    {
        "slug": "yctx",
        "name": "Y-CTX",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "registration_stage": "registry",
        "description": "Context extraction and assembly module. Produces Context Packs for Y-ORC.",
        "tags": ["core", "context", "deterministic", "backend"],
        "git_path": "registry/protocol--yctx.md",
        "version": "1.0"
    },
    {
        "slug": "yid",
        "name": "Y-ID",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "registration_stage": "registry",
        "description": "Naming, namespaces and identifier management module.",
        "tags": ["core", "identity", "naming", "deterministic", "backend"],
        "git_path": "registry/protocol--yid.md",
        "version": "1.0"
    },
    {
        "slug": "ylog",
        "name": "Y-LOG",
        "type": "protocol",
        "status": "active",
        "visibility": "public",
        "registration_stage": "registry",
        "description": "Audit trail and operational history module. Records Mission Pack executions.",
        "tags": ["core", "audit", "logging", "deterministic", "backend"],
        "git_path": "registry/protocol--ylog.md",
        "version": "1.0"
    }
]

for m in new_modules:
    tags_sql = "ARRAY[" + ",".join(f"'{t}'" for t in m['tags']) + "]"
    sql = f"""
INSERT INTO yreg_objects (slug, name, type, status, visibility, registration_stage, description, tags, git_path, version)
VALUES (
    '{m['slug']}', '{m['name']}', '{m['type']}', '{m['status']}',
    '{m['visibility']}', '{m['registration_stage']}', '{m['description']}',
    {tags_sql}, '{m['git_path']}', '{m['version']}'
)
ON CONFLICT (slug) DO UPDATE SET
    description = EXCLUDED.description,
    tags = EXCLUDED.tags,
    updated_at = NOW()
RETURNING id, slug, name;
"""
    result = mcp_sql(sql)
    if isinstance(result, list) and result:
        print(f"  OK [{m['name']}] id={result[0].get('id', '?')}")
    else:
        print(f"  [{m['name']}] {str(result)[:100]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Insert Relations (using slugs)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 2: Insert Relations ===")

relations = [
    # Y-CTX reads Y-MEM (manus-memory slug)
    ("yctx", "manus-memory", "reads", "Y-CTX reads Y-MEM to assemble context"),
    # Y-CTX produces for Y-ORC (yreg slug)
    ("yctx", "yreg", "produces_for", "Y-CTX produces Context Pack consumed by Y-ORC"),
    # Y-ORC emits to Y-LOG
    ("yorc", "ylog", "emits_to", "Y-ORC emits execution events to Y-LOG"),
    # Y-ID governs Y-REG naming
    ("yid", "yreg", "governs", "Y-ID governs naming conventions in Y-REG"),
    # /YOS reads Y-REG
    ("yos", "yreg", "reads", "/YOS reads Y-REG for launcher display"),
    # Y-DEV registers into Y-REG
    ("ydev", "yreg", "registers_into", "Y-DEV registers completed objects into Y-REG"),
    # Y-CAP triggers Y-DEV
    ("ycap", "ydev", "triggers", "Y-CAP triggers Y-DEV for custom development"),
]

# First get all slugs to validate
all_slugs_result = mcp_sql("SELECT slug FROM yreg_objects;")
all_slugs = set()
if isinstance(all_slugs_result, list):
    all_slugs = {r['slug'] for r in all_slugs_result if r.get('slug')}
print(f"  Available slugs: {sorted(all_slugs)}")

for source_slug, target_slug, rel_type, desc in relations:
    if source_slug not in all_slugs:
        print(f"  SKIP [{source_slug} → {target_slug}]: source slug not found")
        continue
    if target_slug not in all_slugs:
        print(f"  SKIP [{source_slug} → {target_slug}]: target slug '{target_slug}' not found")
        continue
    sql = f"""
INSERT INTO yreg_relations (source_slug, target_slug, relation_type)
VALUES ('{source_slug}', '{target_slug}', '{rel_type}')
ON CONFLICT DO NOTHING
RETURNING id;
"""
    result = mcp_sql(sql)
    if isinstance(result, list) and result:
        print(f"  OK [{source_slug} → {target_slug}] ({rel_type})")
    else:
        print(f"  [{source_slug} → {target_slug}] {str(result)[:80]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Insert Capabilities
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 3: Insert Capabilities ===")

capabilities = [
    ("cap-context-assembly", "yctx", "Context Assembly",
     '{"situation": "string", "intent": "string"}',
     '{"context_pack": "object"}',
     ["yctx"]),
    ("cap-identifier-resolution", "yid", "Identifier Resolution",
     '{"name_or_slug": "string"}',
     '{"canonical_id": "uuid", "object": "object"}',
     ["yid"]),
    ("cap-audit-logging", "ylog", "Audit Logging",
     '{"event": "object", "mission_pack_id": "uuid"}',
     '{"log_id": "uuid"}',
     ["ylog"]),
    ("cap-registry-lookup", "yreg", "Registry Lookup",
     '{"type": "string", "status": "string", "visibility": "string"}',
     '{"objects": "array"}',
     ["yreg"]),
    ("cap-text-generation", "manus", "Text Generation",
     '{"prompt": "string", "context": "object"}',
     '{"text": "string"}',
     ["manus"]),
]

for cap_slug, owner_slug, cap_name, input_schema, output_schema, impl_by in capabilities:
    if owner_slug not in all_slugs:
        print(f"  SKIP [{cap_name}]: owner '{owner_slug}' not in registry")
        continue
    impl_sql = "ARRAY[" + ",".join(f"'{s}'" for s in impl_by) + "]"
    sql = f"""
INSERT INTO yreg_capabilities (slug, name, input_schema, output_schema, implemented_by)
VALUES (
    '{cap_slug}', '{cap_name}',
    '{input_schema}'::jsonb, '{output_schema}'::jsonb,
    {impl_sql}
)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    input_schema = EXCLUDED.input_schema,
    output_schema = EXCLUDED.output_schema
RETURNING id;
"""
    result = mcp_sql(sql)
    if isinstance(result, list) and result:
        print(f"  OK [{cap_name}]")
    else:
        print(f"  [{cap_name}] {str(result)[:100]}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Final counts
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Step 4: Final Counts ===")
result = mcp_sql("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as objects,
    (SELECT COUNT(*) FROM yreg_relations) as relations,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities;
""")
if isinstance(result, list) and result:
    r = result[0]
    print(f"  objects={r['objects']}  relations={r['relations']}  capabilities={r['capabilities']}")
else:
    print(result)

print("\n=== Seed v3 Complete ===")
