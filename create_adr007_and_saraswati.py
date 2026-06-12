#!/usr/bin/env python3
"""
Create ADR-0007 in Notion + build Saraswati MVP runtime
"""
import json, subprocess, sys

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def notion_create(title, content):
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{"properties": {"title": title}, "content": content}]
    }
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", json.dumps(payload)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = r.stdout + r.stderr
    # extract URL
    import re
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f"created (no URL in: {out[-100:]})"

# ── ADR-0007 ──────────────────────────────────────────────────────────────────
adr007_content = """# ADR-0007 — Continuous Evolution Loop

**Status:** Accepted | **Date:** 2026-06-12
**Related:** ADR-0006 (CODO), Y-OS Vision v2, Y-OS Law #8

## Context

La première version de Y-OS définissait principalement Y-MEM, Y-REG, Y-ORC et Y-COO.
L'évolution récente a montré qu'un système autonome doit aussi améliorer la qualité de ses compétences, ses processus, sa communication interne, sa structure organisationnelle et son propre système d'apprentissage.

## Decision

Y-OS adopte officiellement un modèle de **Continuous Evolution Loop** :

```
Mission → Execution → Feedback → Learning
→ Organizational Improvement → Capability Expansion → Better Execution → Mission
```

Ce cycle est permanent.

## Three Levels of Evolution

| Level | Question | Owner | Output |
|---|---|---|---|
| Level 1 — Knowledge Evolution | What do we know? | Y-MEM | Knowledge |
| Level 2 — Capability Evolution | What can we do? | Y-REG | Capabilities |
| Level 3 — Organizational Evolution | How should we organize? | CODO (Saraswati) | Org improvements |

## Organizational Evolution Domains (CODO)

1. **Capability Expansion** — Ajout de nouveaux outils, skills, agents, intégrations.
2. **Competency Development** — Amélioration de la maîtrise (prompts, qualité, fiabilité, vitesse).
3. **Process Improvement** — Réduction des étapes, élimination des frictions, automatisation.
4. **Communication Improvement** — Mission Packs, Architecture Specs, handoffs, formats standardisés.
5. **Organizational Optimization** — Nouveaux rôles, responsabilités, hiérarchies, équipes.

## Core Distinction

> Y-MEM learns knowledge. Y-REG learns capabilities. CODO learns organization.

## Y-OS Law #8

> The goal is not only to solve problems. The goal is to continuously improve the organization that solves problems.

## Consequences

Toute nouvelle décision d'architecture doit être évaluée selon son impact sur Knowledge Evolution, Capability Evolution et Organizational Evolution. Les trois niveaux doivent progresser simultanément.

## Long-Term Vision

Y-OS évolue vers une Autonomous Evolving Organization capable d'exécuter, d'apprendre, de s'améliorer, d'étendre ses capacités et d'optimiser son organisation — sans reconfiguration manuelle permanente.
"""

print("Creating ADR-0007 in Notion...")
url_adr = notion_create("ADR-0007 — Continuous Evolution Loop", adr007_content)
print(f"ADR-0007: {url_adr}")

# ── Saraswati Agent Card ──────────────────────────────────────────────────────
saraswati_card = """# Saraswati — CODO Agent Card v1

**Role:** Chief Organizational Development Officer (CODO)
**Alias:** Saraswati
**Layer:** Layer 3 — Organization
**Status:** MVP v1.0 | **Date:** 2026-06-12

## Mission

Improve the organization that executes missions.

## Core Principle

COO (Ganesha) runs the organization.
CODO (Saraswati) improves the organization.

## Responsibilities

Saraswati is responsible for five evolution domains:
1. Capability Expansion — acquire new capabilities
2. Competency Development — improve mastery of existing capabilities
3. Process Improvement — improve operational workflows
4. Communication Improvement — improve inter-agent information flow
5. Organizational Optimization — improve structure, roles, responsibilities

## Inputs

- Execution feedback from COO
- Mission results and lessons learned
- Y-REG capability graph
- Y-OS role definitions
- Performance metrics

## Outputs

- Organizational Review Reports
- Role Design Proposals
- Capability Gap Analysis
- Communication Contract Updates
- Training Plans
- KPI Frameworks

## Modules Used

- Y-REG (capability registry)
- Y-MEM (lessons learned, knowledge)
- Y-CTX (context assembly)
- Y-LOG (execution history)

## Ownership

Saraswati owns:
- Agent Registry
- Role Cards
- Organizational Mapping
- Training Plans
- Capability Maps
- Performance Metrics
- Organizational Reviews

## Implementation

File: /home/ubuntu/yreg/saraswati.py
Runtime: Python MVP v1.0
Workflows: Organizational Review, Capability Gap Analysis, Role Design, Org Improvement
"""

print("Creating Saraswati Agent Card in Notion...")
url_sara = notion_create("🌸 Saraswati — CODO Agent Card v1", saraswati_card)
print(f"Saraswati Card: {url_sara}")
