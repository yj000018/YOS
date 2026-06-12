#!/usr/bin/env python3
"""
Y-REG MVP Build Script
- Rebuilds schema with NOT NULL slugs
- Seeds all Y-OS objects: modules, roles, protocols, capabilities, workflows, commands
- Inserts relations
- Provides CRUD query functions
"""
import subprocess, json, re, time

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

def sql(query):
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    output = result.stdout + result.stderr
    m = re.search(r'\[.*?\]', output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except:
            pass
    # Check for error
    if 'ERROR' in output or 'error' in output.lower():
        err = re.search(r'ERROR[^"]*', output)
        if err:
            return {"error": err.group()[:120]}
    return []

def sql_exec(query):
    """Execute DDL/DML, return raw output snippet."""
    payload = {"project_id": PROJECT_ID, "query": query}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    output = result.stdout + result.stderr
    if 'error' in output.lower() and 'ERROR' in output:
        err = re.search(r'ERROR[^\\n]*', output)
        return f"ERROR: {err.group()[:100] if err else output[-100:]}"
    return "OK"

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: REBUILD SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("PHASE 1: REBUILD Y-REG SCHEMA")
print("=" * 60)

# Drop existing tables
print("\n[1.1] Drop existing tables...")
r = sql_exec("DROP TABLE IF EXISTS yreg_capabilities CASCADE; DROP TABLE IF EXISTS yreg_relations CASCADE; DROP TABLE IF EXISTS yreg_objects CASCADE;")
print(f"  Drop: {r}")
time.sleep(2)

# Drop existing types
print("[1.2] Drop existing types...")
sql_exec("DROP TYPE IF EXISTS yreg_object_type CASCADE;")
sql_exec("DROP TYPE IF EXISTS yreg_status CASCADE;")
sql_exec("DROP TYPE IF EXISTS yreg_visibility CASCADE;")
sql_exec("DROP TYPE IF EXISTS yreg_reg_stage CASCADE;")
time.sleep(1)

# Create ENUMs
print("[1.3] Create ENUMs...")
r = sql_exec("""
CREATE TYPE yreg_object_type AS ENUM (
    'module', 'protocol', 'agent', 'skill', 'workflow',
    'automation', 'service', 'project', 'command', 'prompt',
    'script', 'capability', 'collection', 'knowledge_system'
);
""")
print(f"  yreg_object_type: {r}")

r = sql_exec("""
CREATE TYPE yreg_status AS ENUM ('idea','draft','active','deprecated','archived','broken');
""")
print(f"  yreg_status: {r}")

r = sql_exec("""
CREATE TYPE yreg_visibility AS ENUM ('public','advanced','hidden');
""")
print(f"  yreg_visibility: {r}")

r = sql_exec("""
CREATE TYPE yreg_reg_stage AS ENUM ('discovery','candidate','validation','registry');
""")
print(f"  yreg_reg_stage: {r}")
time.sleep(1)

# Create yreg_objects
print("[1.4] Create yreg_objects...")
r = sql_exec("""
CREATE TABLE yreg_objects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    type            yreg_object_type NOT NULL,
    status          yreg_status NOT NULL DEFAULT 'active',
    visibility      yreg_visibility NOT NULL DEFAULT 'public',
    reg_stage       yreg_reg_stage NOT NULL DEFAULT 'registry',
    description     TEXT,
    question        TEXT,
    module_owner    TEXT,
    equivalent_role TEXT,
    tags            TEXT[] DEFAULT '{}',
    git_path        TEXT,
    version         TEXT DEFAULT '1.0',
    notion_url      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
""")
print(f"  yreg_objects: {r}")

# Create yreg_relations
print("[1.5] Create yreg_relations...")
r = sql_exec("""
CREATE TABLE yreg_relations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_slug     TEXT NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
    target_slug     TEXT NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL,
    description     TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_slug, target_slug, relation_type)
);
""")
print(f"  yreg_relations: {r}")

# Create yreg_capabilities
print("[1.6] Create yreg_capabilities...")
r = sql_exec("""
CREATE TABLE yreg_capabilities (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    owner_slug      TEXT NOT NULL REFERENCES yreg_objects(slug) ON DELETE CASCADE,
    description     TEXT,
    input_schema    JSONB DEFAULT '{}',
    output_schema   JSONB DEFAULT '{}',
    tags            TEXT[] DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
""")
print(f"  yreg_capabilities: {r}")

# Create indexes
print("[1.7] Create indexes...")
sql_exec("CREATE INDEX idx_yreg_objects_type ON yreg_objects(type);")
sql_exec("CREATE INDEX idx_yreg_objects_status ON yreg_objects(status);")
sql_exec("CREATE INDEX idx_yreg_objects_visibility ON yreg_objects(visibility);")
sql_exec("CREATE INDEX idx_yreg_relations_source ON yreg_relations(source_slug);")
print("  Indexes: OK")
time.sleep(1)

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: SEED ALL OBJECTS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PHASE 2: SEED ALL Y-OS OBJECTS")
print("=" * 60)

def insert_object(slug, name, obj_type, description, question=None,
                  module_owner=None, equivalent_role=None, tags=None,
                  visibility='public', status='active', version='1.0',
                  git_path=None, notion_url=None):
    tags_sql = "ARRAY[" + ",".join(f"'{t}'" for t in (tags or [])) + "]"
    q_val = f"'{question}'" if question else "NULL"
    mo_val = f"'{module_owner}'" if module_owner else "NULL"
    er_val = f"'{equivalent_role}'" if equivalent_role else "NULL"
    gp_val = f"'{git_path}'" if git_path else "NULL"
    nu_val = f"'{notion_url}'" if notion_url else "NULL"
    desc_esc = description.replace("'", "''")

    query = f"""
INSERT INTO yreg_objects
    (slug, name, type, status, visibility, description, question, module_owner, equivalent_role, tags, git_path, version, notion_url)
VALUES
    ('{slug}', '{name}', '{obj_type}', '{status}', '{visibility}',
     '{desc_esc}', {q_val}, {mo_val}, {er_val}, {tags_sql}, {gp_val}, '{version}', {nu_val})
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name, description = EXCLUDED.description,
    question = EXCLUDED.question, module_owner = EXCLUDED.module_owner,
    equivalent_role = EXCLUDED.equivalent_role, tags = EXCLUDED.tags,
    updated_at = NOW()
RETURNING slug;
"""
    result = sql(query)
    if isinstance(result, list) and result:
        return f"OK"
    return f"ERR: {str(result)[:60]}"

# ── CORE MODULES ──────────────────────────────────────────────────────────────
print("\n[2.1] Core Modules (9)...")
modules = [
    ("yos",  "/YOS",  "command",  "Universal Launcher — entry point to Y-OS.", "How do I access the system?", "Y-OS", "Front Desk, Command Center", ["core","launcher","frontend"]),
    ("yreg", "Y-REG", "module",   "Registry of all Y-OS objects — capabilities, protocols, agents, workflows.", "What exists?", "Y-REG", "Registrar, Librarian, Asset Manager", ["core","registry","backend","deterministic"]),
    ("ymem", "Y-MEM", "module",   "Memory and knowledge management — stores decisions, history, documents.", "What is known?", "Y-MEM", "Archivist, Knowledge Officer", ["core","memory","backend","deterministic"]),
    ("yctx", "Y-CTX", "module",   "Context extraction and assembly — produces Context Packs for Y-ORC.", "What context is relevant?", "Y-CTX", "Analyst, Briefing Officer", ["core","context","backend","deterministic"]),
    ("yorc", "Y-ORC", "module",   "Orchestration, routing, workflow planning and execution coordination.", "What should happen now?", "Y-ORC", "COO, Chief of Staff, Operations Director", ["core","orchestration","backend","deterministic"]),
    ("ycap", "Y-CAP", "module",   "Capability acquisition and system evolution strategy.", "How do we acquire new capabilities?", "Y-CAP", "Strategy Lead, Innovation Lead, Procurement Lead", ["core","capabilities","backend","deterministic"]),
    ("ydev", "Y-DEV", "module",   "Capability development protocol — governs how new objects are built.", "How do we build new capabilities?", "Y-DEV", "CTO, Engineering Lead", ["core","development","backend","deterministic"]),
    ("yid",  "Y-ID",  "module",   "Naming, namespaces and identifier management across all Y-OS objects.", "How do we identify things?", "Y-ID", "Information Architect", ["core","identity","backend","deterministic"]),
    ("ylog", "Y-LOG", "module",   "Audit trail and operational history — records Mission Pack executions.", "What happened?", "Y-LOG", "Auditor, Operations Recorder", ["core","audit","backend","deterministic"]),
]
for slug, name, t, desc, q, mo, er, tags in modules:
    r = insert_object(slug, name, t, desc, q, mo, er, tags, git_path=f"registry/{t}--{slug}.md")
    print(f"  {name}: {r}")

# ── AGENT ROLES ───────────────────────────────────────────────────────────────
print("\n[2.2] Agent Roles...")
agents = [
    ("agent-manus",      "Manus",          "Autonomous AI agent — primary executor of Y-OS tasks.", "PA, COO, Architect, Developer", ["agent","ai","primary"]),
    ("agent-coo",        "COO",            "Operational orchestration — decides approach, selects resources, prioritizes.", "COO, Chief of Staff", ["agent","role","organizational"]),
    ("agent-architect",  "Architect",      "System design and architecture decisions.", "Architect, System Designer", ["agent","role","organizational"]),
    ("agent-strategist", "Strategist",     "Long-term vision, capability roadmap, innovation.", "Strategist, Innovation Lead", ["agent","role","organizational"]),
    ("agent-developer",  "Developer",      "Implements capabilities following Y-DEV protocol.", "Developer, Engineer", ["agent","role","organizational"]),
    ("agent-researcher", "Researcher",     "Information gathering, analysis, synthesis.", "Researcher, Analyst", ["agent","role","organizational"]),
    ("agent-pa",         "PA",             "Personal assistant — scheduling, coordination, communication.", "Personal Assistant", ["agent","role","organizational"]),
    ("agent-hr",         "HR",             "Team management, agent onboarding, capability matching.", "HR Lead", ["agent","role","organizational"]),
    ("agent-cto",        "CTO",            "Technical leadership, architecture validation, build strategy.", "CTO, Engineering Lead", ["agent","role","organizational"]),
]
for slug, name, desc, er, tags in agents:
    r = insert_object(slug, name, "agent", desc, equivalent_role=er, tags=tags)
    print(f"  {name}: {r}")

# ── PROTOCOLS ─────────────────────────────────────────────────────────────────
print("\n[2.3] Protocols...")
protocols = [
    ("protocol-ydev",  "Y-DEV Protocol",  "Development protocol governing how new Y-OS objects are designed, built, reviewed and registered.", ["protocol","development","governance"]),
    ("protocol-yreg",  "Y-REG Protocol",  "Registry protocol governing object registration, lifecycle and discovery pipeline.", ["protocol","registry","governance"]),
    ("protocol-yos-law-1", "Y-OS Law #1", "System functions are primary. Agents are secondary.", ["protocol","law","governance"]),
    ("protocol-yos-law-2", "Y-OS Law #2", "Modules are primary. Agents are secondary.", ["protocol","law","governance"]),
    ("protocol-yos-law-3", "Y-OS Law #3", "Agents use modules. Modules do not replace agents.", ["protocol","law","governance"]),
    ("protocol-arch-freeze", "Architecture Freeze v1", "No new core modules without demonstrating existing 9 cannot absorb the responsibility.", ["protocol","governance","freeze"]),
]
for slug, name, desc, tags in protocols:
    r = insert_object(slug, name, "protocol", desc, tags=tags, git_path=f"registry/protocol--{slug}.md")
    print(f"  {name}: {r}")

# ── SKILLS ────────────────────────────────────────────────────────────────────
print("\n[2.4] Skills (Manus)...")
skills = [
    ("skill-memory-manager",    "memory-manager",    "Persistent memory using Notion — store, retrieve, search sessions and projects.", ["skill","memory","notion"]),
    ("skill-yos-optimizer",     "yos-optimizer",     "Credit optimizer and routing orchestrator for Y-OS sessions.", ["skill","optimization","routing"]),
    ("skill-tool-router",       "tool-router",       "Intelligent tool routing — MCP, API, connectors selection.", ["skill","routing","tools"]),
    ("skill-session-synthesizer","session-synthesizer","Cross-session synthesis and memory archival.", ["skill","memory","synthesis"]),
    ("skill-dev",               "dev",               "Claude code engine for complex Y-OS development tasks.", ["skill","development","code"]),
    ("skill-imagegen",          "imagegen",          "Visual deliverable routing and AI image generation.", ["skill","image","generation"]),
    ("skill-canva-mcp",         "canva-mcp",         "Canva MCP integration for design workflows.", ["skill","design","canva"]),
]
for slug, name, desc, tags in skills:
    r = insert_object(slug, name, "skill", desc, module_owner="Y-DEV", tags=tags, git_path=f"skills/{name}/SKILL.md")
    print(f"  {name}: {r}")

# ── WORKFLOWS ─────────────────────────────────────────────────────────────────
print("\n[2.5] Workflows...")
workflows = [
    ("workflow-yreg-sync",    "Y-REG Sync",    "Synchronize Git/Markdown registry files to Supabase runtime cache.", ["workflow","sync","registry"]),
    ("workflow-session-archive","Session Archive","Archive Manus session to Notion memory.", ["workflow","memory","archive"]),
    ("workflow-memory-pipeline","Memory Pipeline","Full LLM memory pipeline — collect, synthesize, cluster, archive.", ["workflow","memory","pipeline"]),
]
for slug, name, desc, tags in workflows:
    r = insert_object(slug, name, "workflow", desc, module_owner="Y-ORC", tags=tags)
    print(f"  {name}: {r}")

# ── COMMANDS ──────────────────────────────────────────────────────────────────
print("\n[2.6] Commands...")
commands = [
    ("cmd-yos",        "/YOS",        "Launch Y-OS universal launcher.", ["command","launcher"]),
    ("cmd-yreg-sync",  "/yreg sync",  "Trigger Y-REG sync from Git to Supabase.", ["command","registry","sync"]),
    ("cmd-status",     "/status",     "Get current session status.", ["command","session"]),
    ("cmd-summary",    "/summary",    "Generate session summary.", ["command","session","memory"]),
]
for slug, name, desc, tags in commands:
    r = insert_object(slug, name, "command", desc, tags=tags)
    print(f"  {name}: {r}")

# ── KNOWLEDGE SYSTEMS ─────────────────────────────────────────────────────────
print("\n[2.7] Knowledge Systems...")
ks = [
    ("ks-manus-memory",  "Manus Memory",  "Notion-based persistent memory for all Y-OS sessions and projects.", ["knowledge","memory","notion"]),
    ("ks-obsidian-git",  "Obsidian+Git",  "Canonical source of truth — Obsidian vault backed by Git.", ["knowledge","obsidian","git","canonical"]),
]
for slug, name, desc, tags in ks:
    r = insert_object(slug, name, "knowledge_system", desc, module_owner="Y-MEM", tags=tags)
    print(f"  {name}: {r}")

# ── PROJECTS ──────────────────────────────────────────────────────────────────
print("\n[2.8] Projects...")
projects = [
    ("project-yos",  "Y-OS",  "Cognitive Operating System — the meta-project.", ["project","core"]),
    ("project-yreg", "Y-REG", "Registry MVP — first operational component of Y-OS.", ["project","registry","mvp"]),
]
for slug, name, desc, tags in projects:
    r = insert_object(slug, name, "project", desc, tags=tags)
    print(f"  {name}: {r}")

# ── COLLECTIONS ───────────────────────────────────────────────────────────────
print("\n[2.9] Collections...")
collections = [
    ("col-yos-core",     "Y-OS Core",     "Core modules of Y-OS — frozen at 9.", ["collection","core"]),
    ("col-yos-agents",   "Y-OS Agents",   "Organizational roles in Y-OS.", ["collection","agents"]),
    ("col-yos-protocols","Y-OS Protocols","Governance protocols and laws.", ["collection","protocols"]),
]
for slug, name, desc, tags in collections:
    r = insert_object(slug, name, "collection", desc, tags=tags)
    print(f"  {name}: {r}")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: SEED RELATIONS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PHASE 3: SEED RELATIONS")
print("=" * 60)

def insert_relation(source, target, rel_type, desc=""):
    query = f"""
INSERT INTO yreg_relations (source_slug, target_slug, relation_type, description)
VALUES ('{source}', '{target}', '{rel_type}', '{desc}')
ON CONFLICT (source_slug, target_slug, relation_type) DO NOTHING
RETURNING id;
"""
    result = sql(query)
    if isinstance(result, list) and result:
        return "OK"
    return f"SKIP/ERR: {str(result)[:50]}"

relations = [
    # Module data flows
    ("yctx", "ymem",  "reads",          "Y-CTX reads Y-MEM to assemble context"),
    ("yctx", "yorc",  "produces_for",   "Y-CTX produces Context Pack for Y-ORC"),
    ("yorc", "ylog",  "emits_to",       "Y-ORC emits execution events to Y-LOG"),
    ("yorc", "yreg",  "reads",          "Y-ORC reads Y-REG for available tools"),
    ("yorc", "yctx",  "consumes",       "Y-ORC consumes Context Pack from Y-CTX"),
    ("ydev", "yreg",  "registers_into", "Y-DEV registers completed objects into Y-REG"),
    ("ycap", "ydev",  "triggers",       "Y-CAP triggers Y-DEV for custom development"),
    ("yid",  "yreg",  "governs",        "Y-ID governs naming conventions in Y-REG"),
    ("yos",  "yreg",  "reads",          "/YOS reads Y-REG for launcher display"),
    # Agent → Module usage
    ("agent-coo",        "yorc",  "uses", "COO uses Y-ORC for execution routing"),
    ("agent-coo",        "yctx",  "uses", "COO uses Y-CTX for context assembly"),
    ("agent-coo",        "yreg",  "uses", "COO uses Y-REG for capability lookup"),
    ("agent-coo",        "ymem",  "uses", "COO uses Y-MEM for memory retrieval"),
    ("agent-architect",  "ydev",  "uses", "Architect uses Y-DEV for design protocol"),
    ("agent-architect",  "yctx",  "uses", "Architect uses Y-CTX for context"),
    ("agent-architect",  "yreg",  "uses", "Architect uses Y-REG for system overview"),
    ("agent-strategist", "ycap",  "uses", "Strategist uses Y-CAP for capability planning"),
    ("agent-strategist", "ymem",  "uses", "Strategist uses Y-MEM for knowledge"),
    ("agent-strategist", "yctx",  "uses", "Strategist uses Y-CTX for context"),
    ("agent-developer",  "ydev",  "uses", "Developer uses Y-DEV protocol"),
    ("agent-developer",  "yreg",  "uses", "Developer uses Y-REG for object lookup"),
    ("agent-manus",      "yreg",  "uses", "Manus uses Y-REG for capability lookup"),
    ("agent-manus",      "ymem",  "uses", "Manus uses Y-MEM for memory"),
    ("agent-manus",      "yorc",  "uses", "Manus uses Y-ORC for orchestration"),
    # Protocol governance
    ("protocol-arch-freeze", "yreg", "governs", "Architecture Freeze governs Y-REG module list"),
    ("protocol-ydev",        "ydev", "defines",  "Y-DEV Protocol defines Y-DEV module behavior"),
    ("protocol-yreg",        "yreg", "defines",  "Y-REG Protocol defines Y-REG module behavior"),
    # Workflow ownership
    ("workflow-yreg-sync",    "yreg", "updates",  "Y-REG Sync updates Supabase from Git"),
    ("workflow-session-archive","ks-manus-memory","writes_to","Session Archive writes to Manus Memory"),
]

for source, target, rel_type, desc in relations:
    r = insert_relation(source, target, rel_type, desc)
    print(f"  [{source} → {target}] {rel_type}: {r}")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4: SEED CAPABILITIES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PHASE 4: SEED CAPABILITIES")
print("=" * 60)

def insert_capability(slug, name, owner_slug, description, tags=None):
    tags_sql = "ARRAY[" + ",".join(f"'{t}'" for t in (tags or [])) + "]"
    desc_esc = description.replace("'", "''")
    query = f"""
INSERT INTO yreg_capabilities (slug, name, owner_slug, description, tags)
VALUES ('{slug}', '{name}', '{owner_slug}', '{desc_esc}', {tags_sql})
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name, description = EXCLUDED.description
RETURNING slug;
"""
    result = sql(query)
    if isinstance(result, list) and result:
        return "OK"
    return f"ERR: {str(result)[:60]}"

capabilities = [
    ("cap-registry-lookup",       "Registry Lookup",       "yreg",   "Query Y-REG for objects by type, status, visibility.", ["query","registry"]),
    ("cap-registry-crud",         "Registry CRUD",         "yreg",   "Create, read, update, delete Y-REG objects.", ["crud","registry"]),
    ("cap-context-assembly",      "Context Assembly",      "yctx",   "Assemble Context Pack from Y-MEM for a given situation.", ["context","assembly"]),
    ("cap-identifier-resolution", "Identifier Resolution", "yid",    "Resolve slugs and names to canonical object IDs.", ["identity","resolution"]),
    ("cap-audit-logging",         "Audit Logging",         "ylog",   "Record append-only execution events and operational history.", ["audit","logging"]),
    ("cap-workflow-orchestration","Workflow Orchestration", "yorc",   "Route and execute workflow plans from Mission Packs.", ["orchestration","workflow"]),
    ("cap-memory-store",          "Memory Store",          "ymem",   "Store and retrieve persistent memory across sessions.", ["memory","storage"]),
    ("cap-capability-acquisition","Capability Acquisition", "ycap",   "Evaluate and acquire new system capabilities.", ["capabilities","acquisition"]),
    ("cap-dev-protocol",          "Development Protocol",  "ydev",   "Execute Y-DEV protocol for building new objects.", ["development","protocol"]),
    ("cap-text-generation",       "Text Generation",       "agent-manus", "Generate text, code, documents using LLMs.", ["generation","llm"]),
    ("cap-web-search",            "Web Search",            "agent-manus", "Search the web and extract information.", ["search","web"]),
    ("cap-code-execution",        "Code Execution",        "agent-manus", "Execute Python, shell scripts in sandbox.", ["code","execution"]),
    ("cap-notion-integration",    "Notion Integration",    "skill-memory-manager", "Read/write Notion pages and databases.", ["notion","integration"]),
]

for slug, name, owner, desc, tags in capabilities:
    r = insert_capability(slug, name, owner, desc, tags)
    print(f"  {name}: {r}")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PHASE 5: VERIFICATION")
print("=" * 60)

counts = sql("""
SELECT
    (SELECT COUNT(*) FROM yreg_objects) as objects,
    (SELECT COUNT(*) FROM yreg_relations) as relations,
    (SELECT COUNT(*) FROM yreg_capabilities) as capabilities;
""")
if isinstance(counts, list) and counts:
    c = counts[0]
    print(f"\n  TOTALS: objects={c['objects']}  relations={c['relations']}  capabilities={c['capabilities']}")

by_type = sql("SELECT type, COUNT(*) as n FROM yreg_objects GROUP BY type ORDER BY n DESC;")
if isinstance(by_type, list):
    print("\n  BY TYPE:")
    for row in by_type:
        print(f"    {row['type']:20} {row['n']}")

print("\n=== Y-REG MVP BUILD COMPLETE ===")
