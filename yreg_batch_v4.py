#!/usr/bin/env python3
"""
Y-REG Batch Insert v4.0
Option A: capabilities inserted into yreg_objects (type=capability) so FK is satisfied.
3 migrations total.
"""
import json, subprocess, re, glob, os

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def migrate(name, sql):
    payload = {"project_id": PROJECT_ID, "name": name, "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "apply_migration",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    out = result.stdout + result.stderr
    ok = 'error' not in out.lower()
    print(f"  {name}: {'OK' if ok else 'FAIL'}")
    if not ok:
        idx = out.lower().find('error')
        print(f"  {out[idx:idx+200]}")
    return ok

def exec_sql(query):
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    m = re.search(r'\[\{.*?\}\]', out, re.DOTALL)
    if m:
        try: return json.loads(m.group())
        except: pass
    files = sorted(glob.glob(os.path.expanduser('~/.mcp/tool-results/*execute_sql*')))
    if files:
        with open(files[-1]) as f: content = f.read()
        m = re.search(r'\[\{.*?\}\]', content, re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
    return []

def esc(s):
    return str(s).replace("'", "''").replace("\\", "\\\\")[:400]

def main():
    with open("/home/ubuntu/yreg/capability_map.json") as f:
        cap_map = json.load(f)
    with open("/home/ubuntu/yreg/scan_results.json") as f:
        skills = json.load(f)

    module_map = {
        "Y-MEM": "ymem", "Y-CTX": "yctx", "Y-ORC": "yorc",
        "Y-DEV": "ydev", "Y-CAP": "ycap", "Y-REG": "yreg",
        "Y-LOG": "ylog", "Y-ID": "yid"
    }

    # ─── MIGRATION A: Insert capabilities as yreg_objects (type=capability) ──
    cap_obj_rows = []
    for cap_slug, cap_data in cap_map["capabilities"].items():
        cs = esc(cap_slug)
        cn = esc(cap_data["name"])
        cm = esc(cap_data["module"])
        owners = cap_data.get("owners", [])
        owner = esc(owners[0]) if owners else cs
        desc = esc(f"Capability provided by {cap_data['module']}. Used by {len(owners)} skill(s).")
        tags_sql = "'{" + cap_data["module"].lower() + "}'"
        cap_obj_rows.append(
            f"  ('{cs}','capability','active','advanced','{cn}','{desc}','{cm}','{owner}',{tags_sql})"
        )

    sql_a = ("INSERT INTO yreg_objects "
             "(slug, type, status, visibility, name, description, question, module_owner, tags)\nVALUES\n"
             + ",\n".join(cap_obj_rows)
             + "\nON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description;")

    print(f"MIGRATION A: Insert {len(cap_obj_rows)} capabilities as objects...")
    migrate("yreg_caps_as_objects_v4", sql_a)

    # ─── MIGRATION B: Relations (skill→capability + module→capability) ────────
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

    for cap_slug, cap_data in cap_map["capabilities"].items():
        mod_slug = module_map.get(cap_data["module"])
        if mod_slug:
            key = (mod_slug, cap_slug, "provides")
            if key not in seen:
                seen.add(key)
                desc = esc(f"{cap_data['module']} provides {cap_data['name']}")
                rel_rows.append(f"  ('{esc(mod_slug)}','{esc(cap_slug)}','provides','{desc}')")

    print(f"MIGRATION B: Insert {len(rel_rows)} relations in batches...")
    batch_size = 150
    ok_count = 0
    for i in range(0, len(rel_rows), batch_size):
        batch = rel_rows[i:i+batch_size]
        sql_b = ("INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)\nVALUES\n"
                 + ",\n".join(batch)
                 + "\nON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING;")
        if migrate(f"yreg_rel_v4_{i//batch_size}", sql_b):
            ok_count += len(batch)
    print(f"  {ok_count}/{len(rel_rows)} relations inserted")

    # ─── VERIFY ───────────────────────────────────────────────────────────────
    print("\nVERIFY:")
    counts = exec_sql(
        "SELECT (SELECT COUNT(*) FROM yreg_objects) as objects,"
        "(SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,"
        "(SELECT COUNT(*) FROM yreg_objects WHERE type='capability') as capabilities,"
        "(SELECT COUNT(*) FROM yreg_relations) as relations;"
    )
    if counts:
        c = counts[0]
        print(f"  Objects:      {c.get('objects','?')}")
        print(f"  Skills:       {c.get('skills','?')}")
        print(f"  Capabilities: {c.get('capabilities','?')}")
        print(f"  Relations:    {c.get('relations','?')}")
    else:
        print("  Check Supabase dashboard for counts")

if __name__ == "__main__":
    main()
