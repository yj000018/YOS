# 🏢 Y-OS Organizational Mapping v1

**Version:** 1.0
**Status:** Active
**Author:** Manus AI

---

## 1. Core Principle
This document formalizes **Y-OS Law #3**:
> **"Agents use modules. Modules do not replace agents."**

Modules provide deterministic system functions (cognition and operational infrastructure). Agents provide non-deterministic organizational roles (judgment, strategy, and coordination).

---

## 2. Role-to-Module Matrix

This matrix defines which system modules are primarily used by each organizational role. A role may use a module to read data, trigger an action, or consume a service.

| Organizational Role | Primary Modules | Secondary Modules | Core Responsibility |
|---------------------|-----------------|-------------------|---------------------|
| **COO** | `Y-ORC`, `Y-CTX` | `Y-REG`, `Y-MEM` | Operational orchestration, resource mobilization, task prioritization, and exception management. |
| **Architect** | `Y-DEV`, `Y-CTX` | `Y-REG` | System design, architectural integrity, and capability structure. |
| **Strategist** | `Y-CAP`, `Y-CTX` | `Y-MEM` | Capability acquisition, system evolution, and strategic planning. |
| **Developer** | `Y-DEV` | `Y-REG`, `Y-LOG` | Technical implementation, coding, and tool building. |
| **Researcher** | `Y-CTX`, `Y-MEM` | `Y-REG` | Information gathering, analysis, and context building. |
| **PA (Personal Assistant)** | `/YOS`, `Y-MEM` | `Y-CTX` | Daily operations, scheduling, and direct user interaction. |
| **HR** | `Y-REG`, `Y-CAP` | `Y-LOG` | Role definition, agent onboarding, and capability assignment. |
| **CTO** | `Y-DEV`, `Y-REG` | `Y-CAP`, `Y-LOG` | Technical governance, infrastructure oversight, and protocol enforcement. |
| **Manus (Primary Agent)** | `Y-ORC`, `Y-REG` | `Y-MEM`, `Y-CTX` | Primary execution agent, task routing, and tool invocation. |

---

## 3. Responsibility Matrix (RACI)

Mapping of key operational activities to the roles responsible for them, and the system modules they leverage.

| Activity | Responsible Role | System Module Used | Output / Result |
|----------|------------------|--------------------|-----------------|
| **Context Assembly** | Researcher, COO | `Y-CTX`, `Y-MEM` | Context Pack |
| **Execution Routing** | COO, Manus | `Y-ORC`, `Y-REG` | Mission Pack / Action |
| **Capability Registration**| Architect, Developer | `Y-REG`, `Y-DEV` | Updated Registry |
| **System Audit** | CTO, HR | `Y-LOG` | Audit Trail |
| **Knowledge Retrieval** | PA, Researcher | `Y-MEM`, `/YOS` | Answer / Summary |

---

## 4. Architectural Boundaries
- **Strict Separation:** The COO decides *how* to approach a situation; `Y-ORC` executes the routing logic. The COO is not `Y-ORC`.
- **Backend vs Frontend:** The 9 core modules form the backend (Cognition + Infra). The agents form the frontend (Organization + Decision Making).
- **Evolution:** Roles may be added, removed, or reassigned without altering the underlying system modules. Modules are frozen under *Architecture Freeze v1*.
