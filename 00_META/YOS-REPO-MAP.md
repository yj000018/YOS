# YOS Repo Map

> **Version:** 1.0.0 | **Last updated:** 2026-07-05

---

## Canonical Topology

```
YOS/
├── README.md                          ← root entry point
│
├── 00_META/                           ← constitution, registry, maps
│   ├── YOS-CONSTITUTION.md
│   ├── YOS-MODULE-REGISTRY.md
│   ├── YOS-REPO-MAP.md               ← this file
│   ├── YOS-SOURCE-OF-TRUTH.md
│   └── MIGRATION-INDEX.md
│
├── 01_BACKBONE/                       ← core yOS infrastructure modules
│   ├── MPM/                           ← Mega Prompt Manager (inter-LLM orchestration)
│   │   ├── 00_PROTOCOLS/
│   │   ├── 01_SCHEMAS/
│   │   ├── 02_ADAPTERS/
│   │   ├── 03_TEMPLATES/
│   │   ├── 04_QUEUE/  (drafts/ready/running/executed/reviewed/blocked/superseded)
│   │   ├── 05_LEDGER/
│   │   ├── 06_REPORTS/  (awaiting-review/reviewed/archived)
│   │   └── 99_ARCHIVE/
│   ├── KAP/                           ← Knowledge Absorption Pipeline
│   │   ├── 00_PROTOCOLS/
│   │   ├── 01_SCHEMAS/
│   │   ├── 02_PIPELINES/
│   │   ├── 03_GATES/
│   │   ├── 04_REGISTRIES/
│   │   ├── 05_RUNS/
│   │   ├── 06_REPORTS/
│   │   └── 99_ARCHIVE/
│   ├── GOVERNANCE/                    ← ADRs, policies, manifest, standards
│   ├── ROUTING/                       ← LLM & tool routing rules
│   ├── ART/                           ← Autonomous Reasoning Threads (placeholder)
│   ├── CRT/                           ← Continuity & Recovery Threads (placeholder)
│   ├── MEMORY/                        ← Memory system (Mem0, Notion) (placeholder)
│   ├── BUS/                           ← Event/message bus (placeholder)
│   └── SECURITY/                      ← Credentials, secrets policy (placeholder)
│
├── 02_AGENTS/                         ← AI agent definitions and tools
│   ├── manus/
│   ├── chatgpt/
│   ├── claude/
│   ├── gemini/
│   ├── perplexity/
│   └── skills/
│
├── 03_AUTOMATIONS/                    ← Scripts, n8n, playbooks, monitors
│   ├── n8n/
│   ├── scripts/
│   ├── userscripts/
│   ├── playbooks/
│   └── monitors/
│
├── 04_INTERFACES/                     ← Human-facing interfaces
│   ├── cockpit/
│   ├── obsidian/                      ← yos-reader plugin
│   ├── notion/
│   ├── browser/
│   ├── mobile/
│   └── voice-vision/
│
├── 05_KNOWLEDGE_DOMAINS/              ← Semantic knowledge bases
│   ├── Y-WORLD/                       ← Primary Obsidian vault (234 MD files)
│   ├── KOSMOS/
│   ├── ELYSIUM/
│   ├── CasaTAO/
│   ├── YOUniverse/
│   └── Works/
│
├── 06_APPS_PRODUCTS/                  ← Applications and products
│   ├── y-family/
│   ├── daylog/
│   ├── youniverse/
│   └── prototypes/
│
├── 07_SOURCE_CORPUS/                  ← Raw source material (quarantine only)
│   ├── quarantine/
│   ├── inventories/
│   ├── fingerprints/
│   ├── imports/
│   └── source-maps/
│
├── 08_LOGS/                           ← Execution logs, decisions, reports
│   ├── execution/
│   ├── decisions/
│   ├── agent-runs/
│   ├── mpm-reports/
│   ├── kap-runs/
│   ├── migrations/
│   └── errors/
│
└── 99_ARCHIVE/                        ← Archived, superseded, quarantined
    ├── legacy/
    ├── superseded/
    └── quarantined/
```

---

## Legacy → Canonical Mapping

| Legacy Path | Canonical Path | Status |
| :--- | :--- | :--- |
| `yos-agents/` | `02_AGENTS/` | migrating |
| `yos-agents/routing/` | `01_BACKBONE/ROUTING/` | migrating |
| `yos-automations/` | `03_AUTOMATIONS/` | migrating |
| `yos-apps/` | `06_APPS_PRODUCTS/` | migrating |
| `yos-governance/` | `01_BACKBONE/GOVERNANCE/` | migrating |
| `yos-vault/` | `05_KNOWLEDGE_DOMAINS/Y-WORLD/` | migrating |
| `yos-related/experiments/` | `06_APPS_PRODUCTS/prototypes/` | migrating |
| `yos-related/legacy/` | `99_ARCHIVE/legacy/` | deferred |
| `yos-related/undecided/` | defer | deferred |
| `plugins/yos-reader/` | `04_INTERFACES/obsidian/yos-reader/` | migrating |
| `archive/` | `99_ARCHIVE/legacy/` | deferred |

---

*YOS Repo Map v1.0.0 — 2026-07-05*
