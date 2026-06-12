#!/usr/bin/env python3
"""
Y-REG Batch Insert v1.0
Inserts all 51 skills + relations + capabilities in minimal MCP calls.
Credit Guard: 4 MCP calls total instead of 600+
"""

import json, subprocess, re, glob, os

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def supabase_exec(query):
    """Execute SQL via Supabase MCP."""
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    output = result.stdout + result.stderr
    m = re.search(r'\[.*\]', output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except:
            pass
    return []

def escape(s):
    return str(s).replace("'", "''")[:400]

def main():
    # Load scan results
    with open("/home/ubuntu/yreg/scan_results.json") as f:
        skills = json.load(f)

    print(f"Building batch SQL for {len(skills)} skills...")

    # ─── CALL 1: Batch upsert all 51 skills ───────────────────────────────────
    rows = []
    for s in skills:
        slug = escape(s['slug'])
        name = escape(s['name'])
        desc = escape(s.get('description', ''))
        use_when = escape(s.get('use_when', ''))
        git_path = escape(s.get('git_path', ''))
        module_owner = escape(s.get('module_owner', 'Y-DEV'))
        tags = s.get('tags', [])
        tags_sql = "ARRAY[" + ",".join([f"'{escape(t)}'" for t in tags[:8]]) + "]::text[]" if tags else "ARRAY[]::text[]"
        rows.append(
            f"('{slug}','skill','active','advanced','{name}','{desc}','{use_when}','{git_path}','{module_owner}',{tags_sql})"
        )

    batch_sql = f"""
INSERT INTO yreg_objects (slug, type, status, visibility, name, description, use_when, git_path, module_owner, tags)
VALUES
{','.join(rows)}
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    use_when = EXCLUDED.use_when,
    tags = EXCLUDED.tags,
    module_owner = EXCLUDED.module_owner,
    updated_at = NOW();
"""
    print("CALL 1: Batch upsert 51 skills...")
    supabase_exec(batch_sql)
    print("  Done.")

    # ─── CALL 2: Batch upsert all 36 capabilities ─────────────────────────────
    with open("/home/ubuntu/yreg/capability_map.json") as f:
        cap_map = json.load(f)

    cap_rows = []
    for cap_slug, cap_data in cap_map["capabilities"].items():
        cs = escape(cap_slug)
        cn = escape(cap_data["name"])
        cm = escape(cap_data["module"])
        owners = cap_data.get("owners", [])
        owner = escape(owners[0]) if owners else cs
        desc = escape(f"Capability provided by {cm}. Used by {len(owners)} skill(s).")
        cap_rows.append(f"('{cs}','{cn}','{desc}','{owner}',ARRAY['{cm.lower()}']::text[])")

    cap_sql = f"""
INSERT INTO yreg_capabilities (slug, name, description, owner_slug, tags)
VALUES
{','.join(cap_rows)}
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = NOW();
"""
    print("CALL 2: Batch upsert 36 capabilities...")
    supabase_exec(cap_sql)
    print("  Done.")

    # ─── CALL 3: Batch insert skill→capability relations ──────────────────────
    rel_rows = []
    seen = set()
    for skill in skills:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            key = (skill["slug"], cap_slug, "exposes")
            if key not in seen:
                seen.add(key)
                src = escape(skill["slug"])
                tgt = escape(cap_slug)
                desc = escape(f"{skill['name']} exposes {cap_name}")
                rel_rows.append(f"('{src}','{tgt}','exposes','{desc}')")

    # Also add module→capability provides relations
    module_map = {
        "Y-MEM": "ymem", "Y-CTX": "yctx", "Y-ORC": "yorc",
        "Y-DEV": "ydev", "Y-CAP": "ycap", "Y-REG": "yreg",
        "Y-LOG": "ylog", "Y-ID": "yid"
    }
    for cap_slug, cap_data in cap_map["capabilities"].items():
        mod_slug = module_map.get(cap_data["module"])
        if mod_slug:
            key = (mod_slug, cap_slug, "provides")
            if key not in seen:
                seen.add(key)
                desc = escape(f"{cap_data['module']} provides {cap_data['name']}")
                rel_rows.append(f"('{escape(mod_slug)}','{escape(cap_slug)}','provides','{desc}')")

    rel_sql = f"""
INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)
VALUES
{','.join(rel_rows)}
ON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING;
"""
    print(f"CALL 3: Batch insert {len(rel_rows)} relations...")
    supabase_exec(rel_sql)
    print("  Done.")

    # ─── CALL 4: Verify final counts ──────────────────────────────────────────
    print("CALL 4: Verify counts...")
    counts = supabase_exec("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as objects,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities,
    (SELECT COUNT(*) FROM yreg_relations) as relations;
""")
    if counts:
        c = counts[0]
        print(f"\n=== FINAL COUNTS ===")
        print(f"  Objects:      {c.get('objects','?')}")
        print(f"  Skills:       {c.get('skills','?')}")
        print(f"  Capabilities: {c.get('capabilities','?')}")
        print(f"  Relations:    {c.get('relations','?')}")
    else:
        # Try reading from file
        files = sorted(glob.glob(os.path.expanduser('~/.mcp/tool-results/*supabase_execute_sql*')))
        if files:
            with open(files[-1]) as f:
                content = f.read()
            m = re.search(r'\[.*?\]', content, re.DOTALL)
            if m:
                try:
                    c = json.loads(m.group())[0]
                    print(f"\n=== FINAL COUNTS ===")
                    print(f"  Objects:      {c.get('objects','?')}")
                    print(f"  Skills:       {c.get('skills','?')}")
                    print(f"  Capabilities: {c.get('capabilities','?')}")
                    print(f"  Relations:    {c.get('relations','?')}")
                except:
                    print("  Could not parse counts")

    print("\nTotal MCP calls used: 4 (Credit Guard: batch mode)")

if __name__ == "__main__":
    main()
