#!/usr/bin/env python3
"""
/YOS Launcher MVP v2.0
Dynamic launcher reading Y-REG (Supabase runtime cache).
Fallback: Git/Markdown if Supabase unavailable.

Usage:
    python3 yos_launcher.py                    # Full launcher (public objects)
    python3 yos_launcher.py --advanced         # Include advanced visibility
    python3 yos_launcher.py --type module      # Filter by type
    python3 yos_launcher.py --search "memory"  # Search by name/description
    python3 yos_launcher.py --lookup yreg      # Lookup single object by slug
    python3 yos_launcher.py --relations yreg   # Show relations for object
    python3 yos_launcher.py --status           # Registry status
"""

import subprocess, json, re, sys, os, glob
from datetime import datetime

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER — Supabase with Git fallback
# ─────────────────────────────────────────────────────────────────────────────

def supabase_query(query):
    """Execute SQL via Supabase MCP. Returns list of dicts or None on failure."""
    try:
        import time
        mcp_dir = os.path.expanduser('~/.mcp/tool-results')
        # Snapshot existing files before call
        before = set(glob.glob(os.path.join(mcp_dir, '*supabase_execute_sql*'))) if os.path.exists(mcp_dir) else set()

        payload = {"project_id": PROJECT_ID, "query": query}
        cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
               "--server", "supabase", "--input", json.dumps(payload)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr

        def extract_rows(text):
            """Extract JSON array from MCP output (handles escaped JSON)."""
            # Try: parse outer JSON wrapper {"result": "..."} then extract array
            m_outer = re.search(r'Tool execution result:\n(\{.*\})', text, re.DOTALL)
            if m_outer:
                try:
                    outer = json.loads(m_outer.group(1))
                    result_str = outer.get('result', '')
                    # Find array in the result string
                    m_arr = re.search(r'\[.*\]', result_str, re.DOTALL)
                    if m_arr:
                        return json.loads(m_arr.group())
                except:
                    pass
            # Fallback: direct array search
            m_arr = re.search(r'\[.*\]', text, re.DOTALL)
            if m_arr:
                try:
                    return json.loads(m_arr.group())
                except:
                    pass
            return None

        # Try stdout first
        rows = extract_rows(output)
        if rows is not None:
            return rows

        # Find the NEW file created by this call
        after = set(glob.glob(os.path.join(mcp_dir, '*supabase_execute_sql*')))
        new_files = sorted(after - before)
        if new_files:
            with open(new_files[-1]) as f:
                content = f.read()
            rows = extract_rows(content)
            if rows is not None:
                return rows
    except Exception:
        pass
    return None

def git_fallback_load():
    """Load objects from Git/Markdown files as fallback."""
    objects = []
    registry_dir = os.path.join(os.path.dirname(__file__), "registry")
    if not os.path.exists(registry_dir):
        return objects
    for filepath in glob.glob(os.path.join(registry_dir, "*.md")):
        try:
            with open(filepath) as f:
                content = f.read()
            # Parse YAML frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    fm = {}
                    for line in parts[1].strip().split("\n"):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            fm[k.strip()] = v.strip().strip('"')
                    objects.append({
                        "slug": fm.get("slug", os.path.basename(filepath).replace(".md", "")),
                        "name": fm.get("name", "Unknown"),
                        "type": fm.get("type", "unknown"),
                        "status": fm.get("status", "active"),
                        "visibility": fm.get("visibility", "public"),
                        "description": fm.get("description", ""),
                        "question": fm.get("question", ""),
                        "module_owner": fm.get("module_owner", ""),
                        "source": "git"
                    })
        except Exception:
            pass
    return objects

def get_objects(obj_type=None, visibility_filter=None, search=None, status="active"):
    """Fetch objects from Supabase or Git fallback."""
    conditions = [f"status = '{status}'"]
    if obj_type:
        conditions.append(f"type = '{obj_type}'")
    if visibility_filter:
        vis_list = "','".join(visibility_filter)
        conditions.append(f"visibility IN ('{vis_list}')")
    if search:
        s = search.replace("'", "''")
        conditions.append(f"(name ILIKE '%{s}%' OR description ILIKE '%{s}%' OR slug ILIKE '%{s}%')")

    where = " AND ".join(conditions)
    query = f"SELECT slug, name, type, status, visibility, description, question, module_owner, equivalent_role, tags FROM yreg_objects WHERE {where} ORDER BY type, name;"

    result = supabase_query(query)
    if result is not None:
        for obj in result:
            obj["source"] = "supabase"
        return result, "supabase"

    # Fallback to Git
    objects = git_fallback_load()
    if obj_type:
        objects = [o for o in objects if o.get("type") == obj_type]
    if search:
        sl = search.lower()
        objects = [o for o in objects if sl in o.get("name","").lower() or sl in o.get("description","").lower()]
    return objects, "git"

def get_object(slug):
    """Fetch single object by slug."""
    result = supabase_query(f"SELECT * FROM yreg_objects WHERE slug = '{slug}' LIMIT 1;")
    if result and len(result) > 0:
        return result[0], "supabase"
    # Git fallback
    objects, _ = get_objects()
    for obj in objects:
        if obj.get("slug") == slug:
            return obj, "git"
    return None, None

def get_relations(slug):
    """Fetch relations for an object."""
    query = f"""
SELECT
    r.relation_type,
    r.source_slug,
    r.target_slug,
    r.description,
    CASE WHEN r.source_slug = '{slug}' THEN 'outbound' ELSE 'inbound' END as direction,
    CASE WHEN r.source_slug = '{slug}' THEN o2.name ELSE o1.name END as other_name,
    CASE WHEN r.source_slug = '{slug}' THEN r.target_slug ELSE r.source_slug END as other_slug
FROM yreg_relations r
LEFT JOIN yreg_objects o1 ON o1.slug = r.source_slug
LEFT JOIN yreg_objects o2 ON o2.slug = r.target_slug
WHERE r.source_slug = '{slug}' OR r.target_slug = '{slug}'
ORDER BY direction, r.relation_type;
"""
    return supabase_query(query) or []

def get_capabilities(owner_slug=None):
    """Fetch capabilities, optionally filtered by owner."""
    if owner_slug:
        query = f"SELECT slug, name, description, tags FROM yreg_capabilities WHERE owner_slug = '{owner_slug}' ORDER BY name;"
    else:
        query = "SELECT c.slug, c.name, c.description, c.owner_slug, o.name as owner_name FROM yreg_capabilities c LEFT JOIN yreg_objects o ON o.slug = c.owner_slug ORDER BY o.name, c.name;"
    return supabase_query(query) or []

def get_registry_status():
    """Get registry statistics."""
    result = supabase_query("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as total_objects,
    (SELECT COUNT(*) FROM yreg_objects WHERE status='active') as active,
    (SELECT COUNT(*) FROM yreg_relations) as relations,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='module') as modules,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='agent') as agents,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,
    (SELECT COUNT(*) FROM yreg_objects WHERE type='workflow') as workflows;
""")
    return result[0] if result else {}

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY LAYER
# ─────────────────────────────────────────────────────────────────────────────

TYPE_ICONS = {
    "module":         "⚙️ ",
    "agent":          "🤖",
    "skill":          "🧠",
    "workflow":       "🔄",
    "protocol":       "📜",
    "command":        "⌨️ ",
    "knowledge_system":"📚",
    "project":        "📁",
    "collection":     "📦",
    "capability":     "⚡",
    "service":        "🔌",
    "automation":     "🤖",
    "prompt":         "💬",
    "script":         "📝",
}

SECTION_ORDER = [
    ("module",         "MODULES"),
    ("agent",          "AGENTS"),
    ("capability",     "CAPABILITIES"),
    ("workflow",       "WORKFLOWS"),
    ("skill",          "SKILLS"),
    ("protocol",       "PROTOCOLS"),
    ("command",        "COMMANDS"),
    ("knowledge_system","KNOWLEDGE SYSTEMS"),
    ("project",        "PROJECTS"),
    ("collection",     "COLLECTIONS"),
]

def icon(obj_type):
    return TYPE_ICONS.get(obj_type, "▪️ ")

def header(source="supabase"):
    src_label = "Supabase" if source == "supabase" else "⚠️  Git/Markdown (fallback)"
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              /YOS — Y-OS Launcher v2.0                      ║")
    print(f"║  Source: {src_label:<52}║")
    print(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M'):<60}║")
    print("╚══════════════════════════════════════════════════════════════╝")

def print_section(title, objects):
    if not objects:
        return
    print(f"\n  ── {title} {'─' * (48 - len(title))}")
    for obj in objects:
        ic = icon(obj.get("type",""))
        name = obj.get("name", "?")
        desc = obj.get("description", "")
        slug = obj.get("slug", "")
        # Truncate description
        if len(desc) > 55:
            desc = desc[:52] + "..."
        print(f"  {ic}  {name:<22}  {slug:<22}")
        if desc:
            print(f"       {'':22}  {desc}")

def print_object_detail(obj, source, relations=None, capabilities=None):
    print()
    print(f"  ┌─ {obj.get('name','?')} ({'slug: ' + obj.get('slug','?')})")
    print(f"  │  Type:        {obj.get('type','?')}")
    print(f"  │  Status:      {obj.get('status','?')}  │  Visibility: {obj.get('visibility','?')}")
    if obj.get("question"):
        print(f"  │  Question:    {obj['question']}")
    if obj.get("module_owner"):
        print(f"  │  Module:      {obj['module_owner']}")
    if obj.get("equivalent_role"):
        print(f"  │  Role equiv:  {obj['equivalent_role']}")
    if obj.get("description"):
        print(f"  │  Description: {obj['description']}")
    tags = obj.get("tags") or []
    if tags and isinstance(tags, list):
        print(f"  │  Tags:        {', '.join(tags)}")
    if obj.get("git_path"):
        print(f"  │  Git:         {obj['git_path']}")
    if obj.get("notion_url"):
        print(f"  │  Notion:      {obj['notion_url']}")

    if relations:
        print(f"  │")
        print(f"  │  RELATIONS ({len(relations)}):")
        for r in relations:
            direction = "→" if r.get("direction") == "outbound" else "←"
            print(f"  │    {direction} {r.get('other_name','?'):20} [{r.get('relation_type','?')}]")
            if r.get("description"):
                print(f"  │      {r['description']}")

    if capabilities:
        print(f"  │")
        print(f"  │  CAPABILITIES ({len(capabilities)}):")
        for c in capabilities:
            print(f"  │    ⚡ {c.get('name','?')}: {c.get('description','')[:60]}")

    print(f"  └─ source: {source}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # Parse flags
    show_advanced = "--advanced" in args
    filter_type   = None
    search_term   = None
    lookup_slug   = None
    show_relations = None
    show_status   = "--status" in args

    i = 0
    while i < len(args):
        if args[i] == "--type" and i+1 < len(args):
            filter_type = args[i+1]; i += 2
        elif args[i] == "--search" and i+1 < len(args):
            search_term = args[i+1]; i += 2
        elif args[i] == "--lookup" and i+1 < len(args):
            lookup_slug = args[i+1]; i += 2
        elif args[i] == "--relations" and i+1 < len(args):
            show_relations = args[i+1]; i += 2
        else:
            i += 1

    # ── STATUS MODE ──────────────────────────────────────────────────────────
    if show_status:
        stats = get_registry_status()
        print()
        print("  Y-REG Registry Status")
        print("  ─────────────────────────────────────────────")
        if stats:
            print(f"  Total objects:    {stats.get('total_objects','?')}")
            print(f"  Active:           {stats.get('active','?')}")
            print(f"  Relations:        {stats.get('relations','?')}")
            print(f"  Capabilities:     {stats.get('capabilities','?')}")
            print(f"  ─────────────────────────────────────────────")
            print(f"  Modules:          {stats.get('modules','?')}")
            print(f"  Agents:           {stats.get('agents','?')}")
            print(f"  Skills:           {stats.get('skills','?')}")
            print(f"  Workflows:        {stats.get('workflows','?')}")
        else:
            print("  ⚠️  Could not reach Supabase")
        return

    # ── LOOKUP MODE ──────────────────────────────────────────────────────────
    if lookup_slug:
        obj, source = get_object(lookup_slug)
        if not obj:
            print(f"\n  ⚠️  Object '{lookup_slug}' not found in Y-REG.")
            return
        rels = get_relations(lookup_slug)
        caps = get_capabilities(lookup_slug)
        header(source)
        print_object_detail(obj, source, rels, caps)
        return

    # ── RELATIONS MODE ───────────────────────────────────────────────────────
    if show_relations:
        obj, source = get_object(show_relations)
        rels = get_relations(show_relations)
        header(source)
        if obj:
            print(f"\n  Relations for: {obj.get('name','?')} ({show_relations})")
        print(f"\n  {'Direction':<10} {'Other Object':<25} {'Relation Type':<25} Description")
        print(f"  {'─'*9} {'─'*24} {'─'*24} {'─'*30}")
        for r in rels:
            direction = "→ outbound" if r.get("direction") == "outbound" else "← inbound "
            print(f"  {direction:<10} {r.get('other_name','?'):<25} {r.get('relation_type','?'):<25} {r.get('description','')[:40]}")
        if not rels:
            print("  No relations found.")
        return

    # ── MAIN LAUNCHER ────────────────────────────────────────────────────────
    vis_filter = ["public", "advanced"] if show_advanced else ["public"]

    if filter_type or search_term:
        objects, source = get_objects(
            obj_type=filter_type,
            visibility_filter=vis_filter,
            search=search_term
        )
        header(source)
        if search_term:
            print(f"\n  Search: '{search_term}' — {len(objects)} result(s)")
        by_type = {}
        for obj in objects:
            t = obj.get("type","unknown")
            by_type.setdefault(t, []).append(obj)
        for obj_type, section_name in SECTION_ORDER:
            if obj_type in by_type:
                print_section(section_name, by_type[obj_type])
        return

    # Full launcher — all sections
    all_objects, source = get_objects(visibility_filter=vis_filter)
    header(source)

    if not all_objects:
        print("\n  ⚠️  Y-REG is empty or unreachable.")
        print("  Run: python3 yreg_build_mvp.py to seed the registry.")
        return

    # Group by type
    by_type = {}
    for obj in all_objects:
        t = obj.get("type","unknown")
        by_type.setdefault(t, []).append(obj)

    total = len(all_objects)
    print(f"\n  {total} objects registered  │  {'advanced mode' if show_advanced else 'public view'}")

    for obj_type, section_name in SECTION_ORDER:
        if obj_type in by_type:
            print_section(section_name, by_type[obj_type])

    print()
    print("  ─────────────────────────────────────────────────────────────")
    print("  Commands: --lookup <slug>  --relations <slug>  --search <q>")
    print("            --type <type>   --advanced           --status")
    print()

if __name__ == "__main__":
    main()
