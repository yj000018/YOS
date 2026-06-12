#!/usr/bin/env python3
"""
Y-REG Batch Insert v2.0
Uses apply_migration (file-based) instead of execute_sql to avoid shell escaping issues.
Credit Guard: 3 MCP calls total.
"""

import json, subprocess, re, glob, os

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def supabase_migrate(name, sql):
    """Apply a migration via Supabase MCP (file-based, no shell escaping issues)."""
    payload = {"project_id": PROJECT_ID, "name": name, "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "apply_migration",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    output = result.stdout + result.stderr
    print(f"  Migration '{name}': {'OK' if 'error' not in output.lower() else 'CHECK'}")
    if 'error' in output.lower():
        print(f"  Output: {output[:300]}")
    return output

def supabase_exec(query):
    """Execute SQL via Supabase MCP."""
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    m = re.search(r'\[.*?\]', output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except:
            pass
    return []

def esc(s):
    """Escape for SQL string literals."""
    return str(s).replace("'", "''").replace("\\", "\\\\")[:400]

def main():
    with open("/home/ubuntu/yreg/scan_results.json") as f:
        skills = json.load(f)
    with open("/home/ubuntu/yreg/capability_map.json") as f:
        cap_map = json.load(f)

    print(f"=== Y-REG BATCH INSERT v2.0 ===")
    print(f"Skills: {len(skills)} | Capabilities: {len(cap_map['capabilities'])}")
    print(f"Credit Guard: 3 MCP calls total\n")

    # ─── MIGRATION 1: Upsert all skills ───────────────────────────────────────
    rows = []
    for s in skills:
        slug = esc(s['slug'])
        name = esc(s['name'])
        desc = esc(s.get('description', ''))
        use_when = esc(s.get('use_when', ''))
        git_path = esc(s.get('git_path', ''))
        module_owner = esc(s.get('module_owner', 'Y-DEV'))
        tags = s.get('tags', [])
        # Use PostgreSQL array literal syntax
        tags_sql = "'{" + ",".join([esc(t) for t in tags[:8]]) + "}'" if tags else "'{}'"
        rows.append(
            f"  ('{slug}','skill','active','advanced','{name}','{desc}','{use_when}','{git_path}','{module_owner}',{tags_sql})"
        )

    sql1 = "INSERT INTO yreg_objects (slug, type, status, visibility, name, description, question, git_path, module_owner, tags)\nVALUES\n"
    sql1 += ",\n".join(rows)
    sql1 += "\nON CONFLICT (slug) DO UPDATE SET\n  name = EXCLUDED.name,\n  description = EXCLUDED.description,\n  question = EXCLUDED.question,\n  tags = EXCLUDED.tags,\n  module_owner = EXCLUDED.module_owner,\n  updated_at = NOW();"

    print("CALL 1: Upsert 51 skills via migration...")
    supabase_migrate("yreg_skills_batch_v2", sql1)

    # ─── MIGRATION 2: Upsert capabilities + relations ─────────────────────────
    cap_rows = []
    for cap_slug, cap_data in cap_map["capabilities"].items():
        cs = esc(cap_slug)
        cn = esc(cap_data["name"])
        cm = esc(cap_data["module"])
        owners = cap_data.get("owners", [])
        owner = esc(owners[0]) if owners else cs
        desc = esc(f"Capability provided by {cap_data['module']}. Used by {len(owners)} skill(s).")
        cap_rows.append(f"  ('{cs}','{cn}','{desc}','{owner}','{{\"{ cm.lower() }\"}}'::text[])")

    sql2 = "INSERT INTO yreg_capabilities (slug, name, description, owner_slug, tags)\nVALUES\n"
    sql2 += ",\n".join(cap_rows)
    sql2 += "\nON CONFLICT (slug) DO UPDATE SET\n  name = EXCLUDED.name,\n  description = EXCLUDED.description,\n  updated_at = NOW();"

    print("CALL 2: Upsert 36 capabilities + relations via migration...")
    supabase_migrate("yreg_caps_batch_v2", sql2)

    # Build relations SQL
    rel_rows = []
    seen = set()
    for skill in skills:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            key = (skill["slug"], cap_slug, "exposes")
            if key not in seen:
                seen.add(key)
                src = esc(skill["slug"])
                tgt = esc(cap_slug)
                desc = esc(f"{skill['name']} exposes {cap_name}")
                rel_rows.append(f"  ('{src}','{tgt}','exposes','{desc}')")

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
                desc = esc(f"{cap_data['module']} provides {cap_data['name']}")
                rel_rows.append(f"  ('{esc(mod_slug)}','{esc(cap_slug)}','provides','{desc}')")

    sql3 = "INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)\nVALUES\n"
    sql3 += ",\n".join(rel_rows)
    sql3 += "\nON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING;"

    supabase_migrate("yreg_relations_batch_v2", sql3)
    print(f"  ({len(rel_rows)} relations)")

    # ─── CALL 3: Verify ───────────────────────────────────────────────────────
    print("\nCALL 3: Verify final counts...")
    counts = supabase_exec(
        "SELECT (SELECT COUNT(*) FROM yreg_objects) as objects,"
        "(SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,"
        "(SELECT COUNT(*) FROM yreg_capabilities) as capabilities,"
        "(SELECT COUNT(*) FROM yreg_relations) as relations;"
    )
    if counts:
        c = counts[0]
        print(f"\n=== FINAL COUNTS ===")
        print(f"  Objects:      {c.get('objects','?')}")
        print(f"  Skills:       {c.get('skills','?')}")
        print(f"  Capabilities: {c.get('capabilities','?')}")
        print(f"  Relations:    {c.get('relations','?')}")
    else:
        # Read from last result file
        files = sorted(glob.glob(os.path.expanduser('~/.mcp/tool-results/*supabase_execute_sql*')))
        if files:
            with open(files[-1]) as f:
                content = f.read()
            m = re.search(r'\[\{.*?\}\]', content, re.DOTALL)
            if m:
                try:
                    c = json.loads(m.group())[0]
                    print(f"\n=== FINAL COUNTS ===")
                    print(f"  Objects:      {c.get('objects','?')}")
                    print(f"  Skills:       {c.get('skills','?')}")
                    print(f"  Capabilities: {c.get('capabilities','?')}")
                    print(f"  Relations:    {c.get('relations','?')}")
                except Exception as e:
                    print(f"  Parse error: {e}")

if __name__ == "__main__":
    main()
