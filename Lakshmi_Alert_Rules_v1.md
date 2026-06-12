# Alert Rules v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
While Open Loops are passive indicators on a dashboard, Alerts are active notifications pushed to the CEO or relevant roles when critical thresholds are breached.

## Alert Matrix

| Alert Level | Trigger Condition | Target | Action |
| :--- | :--- | :--- | :--- |
| **P1 (Critical)** | Artifact `Rejected` 3 times consecutively. | CEO, Saraswati | Push Notification. Requires structural intervention. |
| **P1 (Critical)** | Mission stalled (no state changes) > 7 days. | CEO, Ganesha | Push Notification. |
| **P2 (High)** | Artifact `Ready For Review` > 72 hours. | Review Owner | Ping Review Owner. Add to CEO Briefing. |
| **P2 (High)** | Cost anomaly detected (see Cost Model). | CEO | Push Notification. |
| **P3 (Medium)** | New Mission initiated without Strategy Brief. | Krishna | Log in Open Loops. |

## Escalation Path
If a P2 Alert is unresolved for 48 hours, it automatically escalates to a P1 Alert targeting the CEO.
