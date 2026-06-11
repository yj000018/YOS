#!/usr/bin/env python3
import subprocess, json

PAGE_ID = "37c35e21-8cf8-8192-a428-c1f6405999a1"

CONTENT = """# Y-OS Core Architecture v1

**Auteur :** Manus AI | **Date :** 11 Juin 2026 | **Statut :** Officiel

---

## 1. Vision Globale

Y-OS est structure autour d'un noyau de neuf modules interdependants. Chaque module repond a une question fondamentale distincte. Cette separation stricte des responsabilites garantit la scalabilite, la clarte et l'extensibilite du systeme.

---

## 2. System Modules vs Agent Roles

### Core Principle

Y-OS is built around **system functions**, not around agents.

Agents may change. Models may change. Tools may change. **System functions remain stable.**

Therefore: **Modules are primary. Agents are secondary.**

### Architectural Rule

Modules are system functions. Agents are operational roles. A module may be used by multiple agents. An agent may use multiple modules. A module must continue to exist even if a specific agent disappears.

---

## 3. Updated Core Architecture (9 Modules)

```
/YOS      How do I access?
Y-REG     What exists?
Y-MEM     What is known?
Y-CTX     What context is relevant?
Y-ORC     What should happen now?
Y-CAP     How do I acquire?
Y-DEV     How do I build?
Y-ID      How do I identify?
Y-LOG     What happened?
```

---

## 4. Module Definitions

### /YOS
**Question :** How do I access the system?
**Function :** Universal Launcher.
**Equivalent role :** Front Desk, Command Center.
**Note :** /YOS reads Y-REG.

---

### Y-REG
**Question :** What exists?
**Function :** Registry of capabilities, protocols, workflows, agents and system objects.
**Equivalent role :** Registrar, Librarian, Asset Manager.
**Note :** Stores system objects and capabilities. Does not store memory.

---

### Y-MEM
**Question :** What is known?
**Function :** Memory and knowledge management.
**Equivalent role :** Archivist, Knowledge Officer.
**Note :** Stores memory (decisions, history, documents, preferences).

---

### Y-CTX
**Question :** What context is relevant?
**Function :** Context extraction and assembly.
**Produces :** Context Pack.
**Equivalent role :** Analyst, Briefing Officer.
**Note :** Y-CTX assembles context but does not orchestrate action.

---

### Y-ORC
**Question :** What should happen now?
**Function :** Orchestration, routing, workflow planning and execution coordination.
**Consumes :** Context Pack (from Y-CTX).
**Produces :** Mission Pack.
**Equivalent role :** COO, Chief of Staff, Operations Director.
**Note :** Y-ORC orchestrates action but does not store memory.

---

### Y-CAP
**Question :** How do we acquire new capabilities?
**Function :** Capability acquisition and system evolution.
**Equivalent role :** Strategy Lead, Innovation Lead, Procurement Lead.

---

### Y-DEV
**Question :** How do we build new capabilities?
**Function :** Capability development protocol.
**Equivalent role :** CTO, Engineering Lead.

---

### Y-ID
**Question :** How do we identify things?
**Function :** Naming, namespaces and identifiers.
**Equivalent role :** Information Architect.

---

### Y-LOG
**Question :** What happened?
**Function :** Audit trail and operational history.
**Equivalent role :** Auditor, Operations Recorder.

---

## 5. Critical Boundaries

**Y-CTX vs Y-ORC :** Y-CTX produces Context Packs (situation analysis). Y-ORC consumes them and produces Mission Packs (action plan). Y-CTX does not orchestrate.

**Y-ORC vs Y-MEM :** Y-ORC is the real-time execution engine. It stores no long-term memory. Y-MEM is the exclusive memory store.

**Y-REG vs Y-MEM :** Y-REG stores system objects (tools, protocols). Y-MEM stores memory (knowledge, history).

**/YOS vs Y-REG :** Y-REG is the database (canonical backend). /YOS is the interface (frontend/launcher) that reads Y-REG.

---

## 6. Dependency Map

1. /YOS depends entirely on Y-REG.
2. Y-CTX reads Y-MEM to assemble context.
3. Y-ORC consumes Context Pack from Y-CTX and reads Y-REG for available tools.
4. Y-DEV registers its output into Y-REG.
5. Y-CAP triggers Y-DEV.
6. Y-LOG receives events from Y-ORC.

---

## 7. Glossaire

- **Agent :** Operational role. An entity that uses system modules.
- **Module :** System function. A stable foundational building block.
- **Context Pack :** Assembled context produced by Y-CTX for a given situation.
- **Mission Pack :** Routed action plan produced by Y-ORC.
- **Source of Truth :** Canonical storage system (Obsidian+Git for Y-REG).
"""

payload = {
    "page_id": PAGE_ID,
    "command": "replace_content",
    "new_str": CONTENT
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-update-page",
       "--server", "notion", "--input", json.dumps(payload)]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
output = result.stdout + result.stderr
print(output[-600:])
