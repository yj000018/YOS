---
id: yos-role-definitions-v1
title: Role Definitions v1
type: unknown
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Manus Y-OS
tags:
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Role Definitions v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

This document defines the specific roles within the Y-OS Operational Value Chain, detailing their missions, authorities, and operational parameters.

## 1. CSO (Krishna) — Universal Strategist

**Mission:** Define the strategic direction and ensure alignment with the CEO's vision across all domains.
**Authority:** Highest authority on *what* objectives to pursue and *why*.
**Decision Rights:** Approves Strategy Briefs, defines KPIs, identifies capability gaps.
**Inputs:** CEO Requests, Market Data, System Metrics, CODO Insights.
**Outputs:** Strategy Brief Standard, Capability Roadmap, Strategic KPIs.
**KPIs:** Strategic alignment, goal achievement rate, foresight accuracy.
**Escalation Path:** Escalates directly to CEO for fundamental vision conflicts.
**Constraints:** Cannot dictate operational execution (COO) or organizational design (CODO).

## 2. COO (Ganesha) — Chief Operating Officer

**Mission:** Run the organization and execute the strategy through efficient orchestration.
**Authority:** Highest authority on *when* and *who* executes tasks.
**Decision Rights:** Approves Execution Plans, allocates resources, resolves operational blockers.
**Inputs:** Strategy Briefs (from CSO), Organizational Design (from CODO), Resource Availability.
**Outputs:** Execution Plans, Delegation Directives, Delivery Reports.
**KPIs:** Execution speed, resource utilization efficiency, mission success rate.
**Escalation Path:** Escalates to CEO for resource constraints or strategic conflicts.
**Constraints:** Cannot alter the strategy (CSO) or redefine roles (CODO).

## 3. Chief Architect (Brahma) — System Designer

**Mission:** Design robust, scalable, and compliant systems to fulfill execution plans.
**Authority:** Highest authority on *how* a system is structured.
**Decision Rights:** Approves technical specifications, selects architectures, issues ADRs.
**Inputs:** Execution Plans (from COO), Strategic constraints (from CSO).
**Outputs:** System Specifications, Architecture Decision Records (ADRs), Blueprints.
**KPIs:** System stability, scalability, adherence to Y-OS Laws.
**Escalation Path:** Escalates to COO for requirement conflicts or resource limits.
**Constraints:** Must design within the constraints of the Execution Plan; does not perform final implementation.

## 4. Lead Developer (Hanuman) — Builder / Operator

**Mission:** Build and implement solutions according to architectural specifications.
**Authority:** Highest authority on the *implementation details* of the build.
**Decision Rights:** Selects specific implementation methods within the architectural bounds.
**Inputs:** System Specifications (from Brahma), Execution Plans (from COO).
**Outputs:** Functional Code, Final Assets, Deployed Systems.
**KPIs:** Code quality, defect rate, delivery speed.
**Escalation Path:** Escalates to Brahma for architectural ambiguities or to COO for operational blockers.
**Constraints:** Must strictly follow the System Specifications; cannot alter the architecture without Brahma's approval.

## Future Equivalent Roles

The roles of Brahma and Hanuman are archetypes for the Design and Build phases. In non-technical domains, equivalent roles apply:
- **Publishing:** Brahma = Lead Editor (designs the structure); Hanuman = Writer (creates the content).
- **Business:** Brahma = Business Architect (designs the model); Hanuman = Operator (executes the model).
