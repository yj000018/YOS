#!/usr/bin/env python3
"""
Y-REG Batch Insert v3.0 — capabilities + relations only (skills already inserted)
"""
import json, subprocess, re, glob, os

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def supabase_migrate(name, sql):
    payload = {"project_id": PROJECT_ID, "name": name, "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "apply_migration",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    output = result.stdout + result.stderr
    ok = 'error' not in output.lower()
    print(f"  Migration '{name}': {'OK' if ok else 'FAIL'}")
    if not ok:
        print(f"  {output[output.find('ERROR'):output.find('ERROR')+200]}")
    return ok

def supabase_exec(query):
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    m = re.search(r'\[\{.*?\}\]', output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except:
            pass
    # Try result file
    files = sorted(glob.glob(os.path.expanduser('~/.mcp/tool-results/*supabase_execute_sql*')))
    if files:
        with open(files[-1]) as f:
            content = f.read()
        m = re.search(r'\[\{.*?\}\]', content, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except:
                pass
    return []

def esc(s):
    return str(s).replace("'", "''").replace("\\", "\\\\")[:400]

def main():
    with open("/home/ubuntu/yreg/capability_map.json") as f:
        cap_map = json.load(f)
    with open("/home/ubuntu/yreg/scan_results.json") as f:
        skills = json.load(f)

    # ─── MIGRATION 2: Capabilities (no updated_at) ────────────────────────────
    cap_rows = []
    for cap_slug, cap_data in cap_map["capabilities"].items():
        cs = esc(cap_slug)
        cn = esc(cap_data["name"])
        owners = cap_data.get("owners", [])
        owner = esc(owners[0]) if owners else cs
        desc = esc(f"Capability provided by {cap_data['module']}. Used by {len(owners)} skill(s).")
        tags_sql = "'{" + cap_data["module"].lower() + "}'"
        cap_rows.append(f"  ('{cs}','{cn}','{owner}','{desc}',{tags_sql})")

    sql2 = "INSERT INTO yreg_capabilities (slug, name, owner_slug, description, tags)\nVALUES\n"
    sql2 += ",\n".join(cap_rows)
    sql2 += "\nON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, description = EXCLUDED.description;"

    print("CALL 1: Upsert 36 capabilities...")
    supabase_migrate("yreg_caps_v3", sql2)

    # ─── MIGRATION 3: Relations (with FK bypass) ──────────────────────────────
    rel_rows = []
    seen = set()

    # skill exposes capability
    for skill in skills:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            key = (skill["slug"], cap_slug, "exposes")
            if key not in seen:
                seen.add(key)
                src = esc(skill["slug"])
                tgt = esc(cap_slug)
                desc = esc(f"{skill['name']} exposes {cap_name}")
                rel_rows.append(f"  ('{src}','{tgt}','exposes','{desc}')")

    # module provides capability
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

    print(f"CALL 2: Insert {len(rel_rows)} relations...")
    # Split into batches of 100 to avoid FK issues with large payloads
    batch_size = 100
    for i in range(0, len(rel_rows), batch_size):
        batch = rel_rows[i:i+batch_size]
        sql3 = "INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)\nVALUES\n"
        sql3 += ",\n".join(batch)
        sql3 += "\nON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING;"
        supabase_migrate(f"yreg_rel_batch_{i//batch_size}", sql3)

    # ─── VERIFY ───────────────────────────────────────────────────────────────
    print("\nCALL 3: Verify counts...")
    counts = supabase_exec(
        "SELECT (SELECT COUNT(*) FROM yreg_objects) as objects,"
        "(SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,"
        "(SELECT COUNT(*) FROM yreg_capabilities) as capabilities,"
        "(SELECT COUNT(*) FROM yreg_relations) as relations;"
    )
    if counts:
        c = counts[0]
        print(f"\n=== FINAL Y-REG COUNTS ===")
        print(f"  Objects:      {c.get('objects','?')}")
        print(f"  Skills:       {c.get('skills','?')}")
        print(f"  Capabilities: {c.get('capabilities','?')}")
        print(f"  Relations:    {c.get('relations','?')}")
    else:
        print("  Could not parse counts — check Supabase dashboard")

if __name__ == "__main__":
    main()
