---
id: yos-y-orc-architecture-v1
title: Y-ORC Architecture v1
type: unknown
status: ACCEPTED
date: '2026-06-13'
version: v1
owner: Manus Y-OS
related_adrs:
- '[[ADR-0024]]'
tags:
- '#accepted'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
implements:
- '[[Context_Pack]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
references:
- '[[ADR-0024]]'
---

# Y-ORC Architecture v1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Type:** Core Architecture  
**Date:** 2026-06-13  

---

## 1. Purpose

Y-ORC (Y-OS Orchestrator) is the execution coordination layer of Y-OS. 

Its purpose is to determine how work moves through the system. While Lakshmi observes and the Control Plane signals, Y-ORC acts. It reads governance signals and triggers the appropriate agent to advance the mission.

---

## 2. Scope & Responsibilities

### Responsibilities
- **Routing:** Determining which agent consumes a specific artifact.
- **Triggering:** Waking up the selected agent and providing the necessary context.
- **State Transitioning:** Moving artifacts through their lifecycle based on agent responses.
- **Exception Handling:** Managing agent failures, timeouts, and rejections.
- **Escalation:** Routing stalled missions to human operators.

### Non-Responsibilities
- **Execution:** Y-ORC does not do the work. It only triggers the workers.
- **Governance:** Y-ORC does not evaluate mission health. It acts on signals from Lakshmi.
- **Storage:** Y-ORC is stateless. All state lives in the Artifact Registry.

---

## 3. Trigger Model

**Question:** What wakes up Y-ORC?

**Canonical Approach: Hybrid (Event-Driven + Polling Fallback)**

1.  **Primary Trigger (Event-Driven):** Y-ORC is triggered by state changes in the Artifact Registry (e.g., an artifact is marked `Accepted` or an Open Loop is generated).
2.  **Fallback Trigger (Polling):** A cron job periodically triggers Y-ORC to catch stalled processes, missed events, or delayed human overrides.

This ensures both immediate responsiveness and guaranteed eventual execution.

---

## 4. Routing Model

```text
Artifact (Accepted) 
→ Y-ORC reads Lineage Rules 
→ Consumer Resolution 
→ Agent Trigger
```

**How is the next consumer determined?**
Consumer resolution is declarative. The Artifact Lineage defines the expected downstream artifact and the required capability. Y-ORC maps the capability to an available agent.

**How are exceptions handled?**
If an agent fails or produces an invalid artifact, Y-ORC transitions the artifact to `Error` state and triggers a retry.

**How are retries handled?**
Y-ORC implements a bounded retry loop (e.g., 3 attempts). After exhaustion, it escalates.

**How are escalations handled?**
Escalations generate an Open Loop and route the artifact to the Human Override queue.

---

## 5. State Machine

The lifecycle of an artifact in relation to Y-ORC:

| State | Owner | Trigger | Validation | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Draft** | Agent | Creation | Format check | Artifact exists |
| **Ready For Review** | Y-ORC | Agent completion | Lineage rules | Awaiting validation |
| **Accepted** | Reviewer | Validation pass | Governance rules | Triggers next step |
| **Consumed** | Downstream Agent | Y-ORC routing | Dependency check | Used as input |
| **Archived** | System | Mission complete | Terminal state | Immutable |

---

## 6. Agent Contract

To ensure agents are entirely pluggable, Y-ORC defines a strict interface.

**Input (Y-ORC → Agent):**
- `Mission ID`
- `Artifact ID`
- `Artifact URI`
- `Context Pack` (Lineage graph subset)
- `Expected Artifact Type`

**Output (Agent → Y-ORC):**
- `New Artifact` (or updated content)
- `Status` (Success/Fail)
- `Notes` (Execution log)
- `Registry Update Payload`

---

## 7. Human Override Model

Y-ORC is designed to run autonomously, but governance requires manual intervention capabilities.

- **CEO Override:** Global halt or reprioritization of missions.
- **Architect Override:** Manual reassignment of agents or capabilities.
- **Manual Routing:** Forcing an artifact to a specific human or agent.
- **Emergency Stop:** Halting all Y-ORC triggers (System Pause).
- **Forced Acceptance/Rejection:** Bypassing automated validation.

*Governance Implication:* Every override must be logged as an artifact in the Registry to maintain traceability.

---

## 8. Control Plane Relationship

| Component | Role | Action |
| :--- | :--- | :--- |
| **Control Plane** | Governance | Observe, Validate, Signal |
| **Y-ORC** | Orchestration | Route, Trigger, Coordinate |

The Control Plane tells the system *what is wrong* or *what is needed*. Y-ORC makes it happen.

---

## 9. Future Runtime Architecture

```text
Registry
   ↓ (State Change)
Control Plane (Lakshmi)
   ↓ (Open Loop / Signal)
Y-ORC
   ↓ (Trigger + Context)
Agents
   ↓ (Execution)
Artifacts
   ↓ (Commit)
Registry
```

---

## 10. Success Criteria Validation

**If every agent is replaced tomorrow:**
Y-ORC will still operate correctly. It will read the Registry, find the `Accepted` artifacts, resolve the required capabilities, and trigger the *new* agents. The organizational behavior and governance guarantees are perfectly preserved because they live in the Registry and Y-ORC's routing logic, not in the agents themselves.

---

## Constitutional Status

> **Constitutional Reference:** Y-ORC operates under Constitutional Principle #5 (*Governance precedes orchestration*) and Principle #8 (*Human override always exists*) from Y-OS Constitution v1 (ADR-0024). Y-ORC is replaceable; its behavioral contract is not.

### Constitutional Hierarchy

```text
Constitution              ← supreme authority (ADR-0024)
        ↓
First Principles
        ↓
Theory of Organization
        ↓
Governance
        ↓
Control Plane
        ↓
Y-ORC                     ← you are here
        ↓
Agents
```


---

## Navigation — Y-OS Canonical Map

> **Foundation frozen.** See [Y-OS Canonical Map v1](Y-OS_Canonical_Map_v1.md) for the complete doctrine index.

```text
Constitution → First Principles → Identity → Operational Cycle
→ Organization → Governance → Control Plane → Orchestration → Execution
```


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[Context_Pack]]
- **references:** [[ADR-0024]]
