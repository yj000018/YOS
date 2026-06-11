#!/usr/bin/env python3
import subprocess, json

PAGE_ID = "37c35e21-8cf8-8192-a428-c1f6405999a1"

CONTENT = """# Y-OS Core Architecture v1

**Auteur :** Manus AI | **Date :** 12 Juin 2026 | **Statut :** Officiel

---

## 1. Vision Globale

Y-OS (Cognitive Operating System) est structure autour d'un noyau de neuf modules interdependants. Chaque module repond a une question fondamentale distincte. Cette separation stricte des responsabilites garantit la scalabilite, la clarte et l'extensibilite du systeme.

---

## 2. System Functions vs Organizational Roles

### Core Principle

Y-OS is built around **system functions**, not around agents.

Agents may change. Models may change. Tools may change. **System functions remain stable.**

Therefore: **Modules are primary. Agents are secondary.**

### Core Rule

System Modules are **deterministic**. Agents are **non-deterministic**.

---

## 3. System Modules

Modules provide system functions. Their mission is not to think. Their mission is to provide stable functions.

**Characteristics:** deterministic, testable, predictable, reusable, composable, replaceable.

*Modules execute functions. Modules do not exercise judgment.*

---

## 4. Agents

Agents are organizational roles. Their mission is to think, decide and coordinate.

**Characteristics:** adaptive, interpretive, strategic, context-sensitive, non-deterministic.

**Examples:** PA, COO, Architect, Strategist, HR, CTO, Researcher, Developer, Knowledge Officer.

*Agents exercise judgment.*

---

## 5. COO vs Y-ORC

**Y-ORC** is system orchestration: routing, planning, workflow execution logic, mission pack construction.

**COO** is operational orchestration: deciding approach, selecting resources/agents/tools, prioritizing, managing exceptions.

Y-ORC is a system function. COO is an organizational role. **The COO uses Y-ORC. The COO is not Y-ORC.**

---

## 6. Backend vs Frontend

**Backend = Cognition + Operational Infrastructure**

Includes: Y-REG, Y-MEM, Y-CTX, Y-ORC, Y-DEV, Y-CAP, Y-ID, Y-LOG.

**Frontend = Organization + Decision Making**

Includes: PA, COO, Architect, Strategist, HR, CTO, Specialists.

Roles consume modules. Modules never replace roles.

Y-OS is not an agent system. Y-OS is a **Cognitive Operating System**.

Agents are replaceable. Models are replaceable. Tools are replaceable. **Cognitive functions are foundational.**

---

## 7. Y-OS Law #3

**Agents use modules. Modules do not replace agents.**

Modules provide cognitive and operational functions. Agents provide judgment, strategy and coordination.

---

## 8. Architecture Freeze v1

> **No new core modules may be created without demonstrating that the responsibility cannot be assigned to one of the existing 9 modules.**

Current Core Modules (frozen):

<table header-row="true">
<tr>
<td>Module</td>
<td>Question</td>
</tr>
<tr>
<td>/YOS</td>
<td>How do I access?</td>
</tr>
<tr>
<td>Y-REG</td>
<td>What exists?</td>
</tr>
<tr>
<td>Y-MEM</td>
<td>What is known?</td>
</tr>
<tr>
<td>Y-CTX</td>
<td>What context is relevant?</td>
</tr>
<tr>
<td>Y-ORC</td>
<td>What should happen now?</td>
</tr>
<tr>
<td>Y-CAP</td>
<td>How do I acquire?</td>
</tr>
<tr>
<td>Y-DEV</td>
<td>How do I build?</td>
</tr>
<tr>
<td>Y-ID</td>
<td>How do I identify?</td>
</tr>
<tr>
<td>Y-LOG</td>
<td>What happened?</td>
</tr>
</table>

Any proposed new module must be submitted with a written justification demonstrating that none of the 9 existing modules can absorb the responsibility. The burden of proof is on the proposer.

---

## 9. Updated Core Architecture

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

## 10. Module Definitions

### /YOS
**Question:** How do I access the system?
**Function:** Universal Launcher.
**Equivalent role:** Front Desk, Command Center.

### Y-REG
**Question:** What exists?
**Function:** Registry of capabilities, protocols, workflows, agents and system objects.
**Equivalent role:** Registrar, Librarian, Asset Manager.

### Y-MEM
**Question:** What is known?
**Function:** Memory and knowledge management.
**Equivalent role:** Archivist, Knowledge Officer.

### Y-CTX
**Question:** What context is relevant?
**Function:** Context extraction and assembly. Produces Context Pack.
**Equivalent role:** Analyst, Briefing Officer.
**Note:** Y-CTX does not orchestrate.

### Y-ORC
**Question:** What should happen now?
**Function:** Orchestration, routing, workflow planning and execution coordination.
**Consumes:** Context Pack. **Produces:** Mission Pack.
**Equivalent role:** COO, Chief of Staff, Operations Director.
**Note:** Y-ORC does not store memory.

### Y-CAP
**Question:** How do we acquire new capabilities?
**Function:** Capability acquisition and system evolution.
**Equivalent role:** Strategy Lead, Innovation Lead, Procurement Lead.

### Y-DEV
**Question:** How do we build new capabilities?
**Function:** Capability development protocol.
**Equivalent role:** CTO, Engineering Lead.

### Y-ID
**Question:** How do we identify things?
**Function:** Naming, namespaces and identifiers.
**Equivalent role:** Information Architect.

### Y-LOG
**Question:** What happened?
**Function:** Audit trail and operational history.
**Equivalent role:** Auditor, Operations Recorder.

---

## 11. Critical Boundaries

**Y-CTX vs Y-ORC:** Y-CTX produces Context Packs. Y-ORC consumes them and produces Mission Packs. Y-CTX does not orchestrate.

**Y-ORC vs Y-MEM:** Y-ORC is the real-time execution engine. Y-MEM is the exclusive memory store.

**Y-REG vs Y-MEM:** Y-REG stores system objects. Y-MEM stores memory and knowledge.

**/YOS vs Y-REG:** Y-REG is the database (canonical backend). /YOS is the interface (frontend/launcher).

**COO vs Y-ORC:** COO decides strategy and selects resources. Y-ORC executes routing and workflow logic.

---

## 12. Glossaire

- **Module:** System function. Deterministic, stable, foundational building block.
- **Agent:** Organizational role. Non-deterministic entity that thinks, decides, and coordinates using modules.
- **Context Pack:** Assembled context produced by Y-CTX for a given situation.
- **Mission Pack:** Routed action plan produced by Y-ORC.
- **Source of Truth:** Canonical storage system (Obsidian+Git for Y-REG).
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
print(output[-400:])
