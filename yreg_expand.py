#!/usr/bin/env python3
"""
Y-REG Expansion v1.0
Injects all scanned skills + capabilities into Supabase Y-REG.
"""

import json, subprocess, re, glob, os

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def supabase_exec(query):
    """Execute SQL via Supabase MCP, return rows or []."""
    before = set(glob.glob(os.path.expanduser('~/.mcp/tool-results/*supabase_execute_sql*')))
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr

    def extract(text):
        m = re.search(r'Tool execution result:\n(\{.*\})', text, re.DOTALL)
        if m:
            try:
                outer = json.loads(m.group(1))
                result_str = outer.get('result', '')
                m2 = re.search(r'\[.*\]', result_str, re.DOTALL)
                if m2:
                    return json.loads(m2.group())
            except:
                pass
        return []

    rows = extract(output)
    if rows is not None and rows != []:
        return rows

    after = set(glob.glob(os.path.expanduser('~/.mcp/tool-results/*supabase_execute_sql*')))
    new_files = sorted(after - before)
    if new_files:
        with open(new_files[-1]) as f:
            content = f.read()
        rows = extract(content)
        if rows is not None:
            return rows
    return []

def upsert_object(obj):
    """Upsert a single object into yreg_objects."""
    slug = obj['slug'].replace("'", "''")
    name = obj['name'].replace("'", "''")[:200]
    desc = obj.get('description', '').replace("'", "''")[:500]
    use_when = obj.get('use_when', '').replace("'", "''")[:500]
    git_path = obj.get('git_path', '').replace("'", "''")
    module_owner = obj.get('module_owner', '').replace("'", "''")
    tags = obj.get('tags', [])
    tags_sql = "ARRAY[" + ",".join([f"'{t}'" for t in tags]) + "]::text[]" if tags else "ARRAY[]::text[]"

    query = f"""
INSERT INTO yreg_objects (slug, name, type, status, visibility, description, use_when, git_path, module_owner, tags)
VALUES (
    '{slug}', '{name}', 'skill', 'active', 'advanced',
    '{desc}', '{use_when}', '{git_path}', '{module_owner}', {tags_sql}
)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    use_when = EXCLUDED.use_when,
    tags = EXCLUDED.tags,
    updated_at = NOW();
"""
    return supabase_exec(query)

def upsert_capability(cap_slug, cap_name, cap_module, owner_slug, description=""):
    """Upsert a capability into yreg_capabilities."""
    cap_slug_safe = cap_slug.replace("'", "''")
    cap_name_safe = cap_name.replace("'", "''")
    owner_safe = owner_slug.replace("'", "''")
    desc_safe = description.replace("'", "''")[:300]

    query = f"""
INSERT INTO yreg_capabilities (slug, name, description, owner_slug, tags)
VALUES (
    '{cap_slug_safe}', '{cap_name_safe}', '{desc_safe}', '{owner_safe}', ARRAY['{cap_module.lower()}']::text[]
)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = NOW();
"""
    return supabase_exec(query)

def upsert_relation(source_slug, target_slug, relation_type, description=""):
    """Upsert a relation into yreg_relations."""
    src = source_slug.replace("'", "''")
    tgt = target_slug.replace("'", "''")
    rel = relation_type.replace("'", "''")
    desc = description.replace("'", "''")[:300]

    query = f"""
INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)
VALUES ('{src}', '{tgt}', '{rel}', '{desc}')
ON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING;
"""
    return supabase_exec(query)

def main():
    # Load scan results
    with open("/home/ubuntu/yreg/scan_results.json") as f:
        skills = json.load(f)

    print(f"=== PHASE 1: UPSERT {len(skills)} SKILLS ===")
    skill_count = 0
    for skill in skills:
        result = upsert_object(skill)
        skill_count += 1
        if skill_count % 10 == 0:
            print(f"  Progress: {skill_count}/{len(skills)}")
    print(f"  Done: {skill_count} skills upserted")

    print("\n=== PHASE 2: COLLECT ALL UNIQUE CAPABILITIES ===")
    all_caps = {}  # slug -> (name, module, [owner_slugs])
    for skill in skills:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            if cap_slug not in all_caps:
                all_caps[cap_slug] = (cap_name, cap_module, [])
            all_caps[cap_slug][2].append(skill["slug"])

    print(f"  Unique capabilities: {len(all_caps)}")

    print("\n=== PHASE 3: UPSERT CAPABILITIES ===")
    cap_count = 0
    for cap_slug, (cap_name, cap_module, owners) in all_caps.items():
        # Use first owner as primary owner, or module slug
        primary_owner = owners[0] if owners else cap_module.lower()
        desc = f"Capability exposed by {len(owners)} skill(s). Primary module: {cap_module}."
        upsert_capability(cap_slug, cap_name, cap_module, primary_owner, desc)
        cap_count += 1
    print(f"  Done: {cap_count} capabilities upserted")

    print("\n=== PHASE 4: CREATE RELATIONS (skill exposes capability) ===")
    rel_count = 0
    for skill in skills:
        for cap_slug, cap_name, cap_module in skill.get("normalized_capabilities", []):
            upsert_relation(skill["slug"], cap_slug, "exposes",
                          f"{skill['name']} exposes {cap_name}")
            rel_count += 1
    print(f"  Done: {rel_count} 'exposes' relations created")

    print("\n=== PHASE 5: CREATE RELATIONS (skill depends_on skill) ===")
    dep_count = 0
    for skill in skills:
        for dep in skill.get("dependencies", []):
            upsert_relation(skill["slug"], dep, "depends_on",
                          f"{skill['name']} depends on {dep}")
            dep_count += 1
    print(f"  Done: {dep_count} 'depends_on' relations created")

    print("\n=== PHASE 6: LINK CAPABILITIES TO MODULES ===")
    module_map = {
        "Y-MEM": "ymem", "Y-CTX": "yctx", "Y-ORC": "yorc",
        "Y-DEV": "ydev", "Y-CAP": "ycap", "Y-REG": "yreg",
        "Y-LOG": "ylog", "Y-ID": "yid"
    }
    mod_rel_count = 0
    for cap_slug, (cap_name, cap_module, owners) in all_caps.items():
        module_slug = module_map.get(cap_module)
        if module_slug:
            upsert_relation(module_slug, cap_slug, "provides",
                          f"{cap_module} provides {cap_name}")
            mod_rel_count += 1
    print(f"  Done: {mod_rel_count} 'provides' relations created")

    print("\n=== VERIFICATION ===")
    counts = supabase_exec("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as objects,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities,
    (SELECT COUNT(*) FROM yreg_relations) as relations;
""")
    if counts:
        c = counts[0]
        print(f"  Objects:      {c.get('objects','?')}")
        print(f"  Skills:       {c.get('skills','?')}")
        print(f"  Capabilities: {c.get('capabilities','?')}")
        print(f"  Relations:    {c.get('relations','?')}")
    else:
        print("  Could not verify counts")

    # Save capability map for reports
    cap_map_output = {
        "capabilities": {
            slug: {"name": name, "module": module, "owners": owners}
            for slug, (name, module, owners) in all_caps.items()
        },
        "skills_count": len(skills),
        "capabilities_count": len(all_caps)
    }
    with open("/home/ubuntu/yreg/capability_map.json", "w") as f:
        json.dump(cap_map_output, f, indent=2)
    print(f"\n  Capability map saved to capability_map.json")

if __name__ == "__main__":
    main()
