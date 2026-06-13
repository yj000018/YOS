# Y-OS Git Architecture v1

**Date:** 2026-06-13  
**Status:** OPERATIONAL  
**Author:** Manus Y-OS  

---

## Current State — GitHub Repository

| Parameter | Value |
| :--- | :--- |
| Remote URL (SSH) | `git@github.com:yj000018/YOS.git` |
| Clone URL (HTTPS) | `https://github.com/yj000018/YOS` |
| Obsidian clone URL | `git@github.com:yj000018/YOS.git` |
| Doctrine branch | `y-os-doctrine` |
| Operational branch | `main` |
| Doctrine commits | **66** |
| Operational commits | **930** |
| Total markdown files (doctrine) | **301** |
| Total files (doctrine) | **611** |
| Clone verified | ✅ |

---

## Repository Map — `y-os-doctrine` Branch

### Top-Level Structure

```
yj000018/YOS (branch: y-os-doctrine)
├── Y-OS_Constitution_v1.md          ← Constitutional layer (FROZEN)
├── Y-OS_Canonical_Map_v1.md         ← Navigation entry point
├── Y-OS_Governance_Doctrine.md      ← Governance framework
├── Y-OS_Master_Architecture_Atlas_v1_final.md
├── worker_registry.json             ← ART Runtime — capability→worker map
├── model_registry.json              ← CRT Runtime — worker→model map
├── yorc_runtime_v1.py               ← Y-ORC Runtime v1
├── art_runtime_v1.py                ← ART Runtime v1
├── crt_runtime_v1.py                ← CRT Runtime v1
├── context_compiler_v1.py           ← CCR Runtime v1
│
├── mission_001/                     ← Organizational execution validation
├── mission_002/                     ← Real cognitive execution
├── mission_003/                     ← Multi-provider (Anthropic + OpenAI)
├── mission_004/                     ← Failure recovery / CRT fallback
├── mission_005/                     ← Knowledge compounding + ADR-0030
├── mission_005b/                    ← CCR governance patch + ADR-0030v2
├── mission_005c/                    ← Governance determinism + ADR-0033
├── mission_006/                     ← Constitutional elevation + ADR-0034
├── mission_007/                     ← Replacement test
├── mission_008/                     ← Constitutional evolution
├── mission_009/                     ← Executable constitution + ADR-0035
├── mission_010/                     ← Context architecture + ADR-0036
├── mission_010b/                    ← Context ROI validation
├── mission_011/                     ← CCR Runtime v2 design + ADR-0037
├── mission_012/                     ← Session Delta Engine + ADR-0038
├── mission_012a/                    ← Storage audit
├── mission_012b/                    ← Living Memory Pipeline + ADR-0039
│
├── ADR-0006 → ADR-0029              ← Foundation ADRs (top-level)
├── context_packs/                   ← Compiled context packs (YAML)
├── diagrams/                        ← Architecture diagrams (Mermaid/PNG)
└── registry/                        ← Artifact registry data
```

### ADR Register (ADR-0006 → ADR-0039)

| ADR | Title | Status |
| :--- | :--- | :--- |
| ADR-0020 | Y-OS Control Plane | ACCEPTED |
| ADR-0021 | Foundational Doctrine | ACCEPTED |
| ADR-0022 | Theory of Organization | ACCEPTED |
| ADR-0023 | Y-ORC Architecture | ACCEPTED |
| ADR-0024 | Y-OS Constitution | ACCEPTED |
| ADR-0025 | Y-ORC Runtime v1 | ACCEPTED |
| ADR-0026 | ART Runtime v1 | ACCEPTED |
| ADR-0027 | Context Continuity | ACCEPTED |
| ADR-0028 | CRT Runtime v1 | ACCEPTED |
| ADR-0029 | Context Compiler | ACCEPTED |
| ADR-0030 | CCR Runtime v1 + Governance Patch | ACCEPTED |
| ADR-0033 | Governance Determinism | ACCEPTED |
| ADR-0034 | Constitutional Elevation | ACCEPTED |
| ADR-0035 | Executable Constitutional Governance | ACCEPTED |
| ADR-0036 | Context Architecture | ACCEPTED |
| ADR-0037 | CCR Runtime v2 | ACCEPTED |
| ADR-0038 | Session Delta Engine | ACCEPTED |
| ADR-0039 | Living Memory Pipeline | ACCEPTED |

---

## Long-Term Git Architecture — Recommended

### Branch Strategy (within `yj000018/YOS`)

```
yj000018/YOS
├── main                    ← Operational code: apps, automations, scripts
│   ├── yos-apps/
│   ├── yos-automations/
│   ├── yos-governance/     ← Legacy governance artifacts
│   └── plugins/
│
├── y-os-doctrine           ← Y-OS Doctrine corpus (CURRENT — this branch)
│   ├── Constitution/
│   ├── ADRs/
│   ├── Missions/
│   └── Runtime/
│
└── (future) obsidian-vault ← Obsidian-formatted vault (symlinked from doctrine)
```

### Recommended Long-Term Folder Consolidation

| Layer | Current Location | Recommended Target |
| :--- | :--- | :--- |
| **Operational code** | `main` — yos-apps, yos-automations | `main` — unchanged |
| **Y-OS Doctrine** | `y-os-doctrine` — flat root | `y-os-doctrine/doctrine/` — organized |
| **ADRs** | Scattered (root + mission_*/ADR-*) | `y-os-doctrine/adr/` — flat numbered |
| **Missions** | `mission_001/` → `mission_012b/` | `y-os-doctrine/missions/` |
| **Governance** | `mission_005c/`, `mission_006/` | `y-os-doctrine/governance/` |
| **Constitution** | Root level | `y-os-doctrine/constitution/` |
| **Runtime scripts** | Root level | `y-os-doctrine/runtime/` |
| **Obsidian vault** | Not yet configured | Local clone of `y-os-doctrine` |

### Obsidian Integration

```bash
# Clone for Obsidian vault (SSH — recommended)
git clone git@github.com:yj000018/YOS.git --branch y-os-doctrine ~/obsidian/y-os-doctrine

# Or HTTPS (no SSH key needed on local machine)
git clone https://github.com/yj000018/YOS.git --branch y-os-doctrine ~/obsidian/y-os-doctrine
```

Open `~/obsidian/y-os-doctrine` as an Obsidian vault. All 301 `.md` files are immediately navigable.

### Authentication Architecture

| Context | Method | Key |
| :--- | :--- | :--- |
| Manus sandbox → GitHub | SSH ed25519 | `y-os@manus-sandbox` (added to GitHub) |
| Local Mac → GitHub | SSH ed25519 (existing Mac key) | Already configured |
| Obsidian git plugin | SSH (via Mac key) | No additional setup needed |
| CI/CD (future) | Deploy key (read-only) | Generate per-repo |

---

## Clone Commands

```bash
# Full doctrine corpus (SSH — recommended)
git clone git@github.com:yj000018/YOS.git --branch y-os-doctrine

# Full doctrine corpus (HTTPS — no SSH key needed)
git clone https://github.com/yj000018/YOS.git --branch y-os-doctrine

# Obsidian vault (shallow, fast)
git clone git@github.com:yj000018/YOS.git --branch y-os-doctrine --depth 1 ~/obsidian/y-os-doctrine
```

---

## Integrity Verification

| Check | Result |
| :--- | :--- |
| SSH auth | ✅ `Hi yj000018!` |
| Remote `main` untouched | ✅ `87d0b8f` — unchanged |
| `y-os-doctrine` commits | ✅ **66** |
| `y-os-doctrine` HEAD | ✅ `86ad547` — MISSION-012B |
| Fresh clone verified | ✅ 610 files, 300 MD |
| Force push used | ❌ None |
| `main` modified | ❌ None |
| Data loss | ❌ None |
