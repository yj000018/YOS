#!/usr/bin/env python3
"""
Add 8 missing core capabilities to Y-REG + refine scanner for granular extraction.
Target: 36 + 8 = 44 confirmed + ~10 from refined scan = 50+
"""
import json, subprocess, re

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
    return []

# ─── 8 Priority Missing Capabilities ─────────────────────────────────────────
missing_caps = [
    # Y-ORC
    ("mission-pack-generation", "Mission Pack Generation", "Y-ORC",
     "Generates structured Mission Packs from Context Packs for agent execution."),
    ("agent-routing", "Agent Routing", "Y-ORC",
     "Routes tasks to the appropriate agent or workflow based on capability matching."),
    ("workflow-planning", "Workflow Planning", "Y-ORC",
     "Decomposes complex tasks into ordered workflow steps."),
    # Y-CTX
    ("context-pack-generation", "Context Pack Generation", "Y-CTX",
     "Assembles and packages relevant context for a given task or agent."),
    ("relevance-scoring", "Relevance Scoring", "Y-CTX",
     "Scores and ranks context elements by relevance to the current task."),
    # Y-REG
    ("object-registration", "Object Registration", "Y-REG",
     "Registers new objects (skills, agents, workflows) into Y-REG."),
    ("relation-traversal", "Relation Traversal", "Y-REG",
     "Traverses the object relation graph to discover dependencies and connections."),
    # Y-ID
    ("namespace-management", "Namespace Management", "Y-ID",
     "Manages naming conventions, namespaces, and slug generation for Y-OS objects."),
    # Y-LOG
    ("execution-history", "Execution History", "Y-LOG",
     "Records and retrieves the execution history of tasks, agents, and workflows."),
    # Y-CAP
    ("gap-analysis", "Gap Analysis", "Y-CAP",
     "Identifies missing capabilities in Y-OS relative to desired system functions."),
    # Y-MEM
    ("cross-session-recall", "Cross-Session Recall", "Y-MEM",
     "Retrieves relevant information from past sessions across the memory system."),
    # Y-DEV
    ("api-integration", "API Integration", "Y-DEV",
     "Integrates external APIs into Y-OS workflows and agents."),
    ("testing-validation", "Testing and Validation", "Y-DEV",
     "Tests and validates code, workflows, and system components."),
    ("deployment-automation", "Deployment Automation", "Y-DEV",
     "Automates deployment of web apps, services, and system components."),
]

# Insert as yreg_objects (type=capability)
rows = []
for slug, name, module, desc in missing_caps:
    s = slug.replace("'", "''")
    n = name.replace("'", "''")
    d = desc.replace("'", "''")
    m = module.replace("'", "''")
    rows.append(f"  ('{s}','capability','active','advanced','{n}','{d}','{m}','{m.lower()}','{{\"{ m.lower() }\"}}'::text[])")

sql = ("INSERT INTO yreg_objects (slug, type, status, visibility, name, description, question, module_owner, tags)\nVALUES\n"
       + ",\n".join(rows)
       + "\nON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description;")

print(f"Adding {len(missing_caps)} missing capabilities...")
migrate("yreg_missing_caps_v1", sql)

# Also insert into yreg_capabilities table
cap_rows = []
for slug, name, module, desc in missing_caps:
    s = slug.replace("'", "''")
    n = name.replace("'", "''")
    d = desc.replace("'", "''")
    cap_rows.append(f"  ('{s}','{n}','{s}','{d}','{{\"{ module.lower() }\"}}'::text[])")

sql2 = ("INSERT INTO yreg_capabilities (slug, name, owner_slug, description, tags)\nVALUES\n"
        + ",\n".join(cap_rows)
        + "\nON CONFLICT (slug) DO NOTHING;")
migrate("yreg_missing_caps_table_v1", sql2)

# ─── Verify final count ───────────────────────────────────────────────────────
counts = exec_sql(
    "SELECT (SELECT COUNT(*) FROM yreg_objects) as objects,"
    "(SELECT COUNT(*) FROM yreg_objects WHERE type='skill') as skills,"
    "(SELECT COUNT(*) FROM yreg_objects WHERE type='capability') as capabilities,"
    "(SELECT COUNT(*) FROM yreg_relations) as relations;"
)
if counts:
    c = counts[0]
    print(f"\n=== FINAL Y-REG COUNTS ===")
    print(f"  Objects:      {c.get('objects','?')}")
    print(f"  Skills:       {c.get('skills','?')}")
    print(f"  Capabilities: {c.get('capabilities','?')}")
    print(f"  Relations:    {c.get('relations','?')}")
    cap_count = int(c.get('capabilities', 0))
    print(f"\n  Target 50+: {'✅ ACHIEVED' if cap_count >= 50 else f'❌ {50-cap_count} more needed'}")
