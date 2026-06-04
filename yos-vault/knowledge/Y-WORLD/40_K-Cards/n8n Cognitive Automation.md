---
type: k-card
domain: Y-OS
tags: [automation, n8n, workflows, integration]
created: 2026-05-29
status: active
---

# n8n Cognitive Automation

**n8n** is the central nervous system for all cloud-based integrations and workflows in [[Y-WORLD]].

## Core Workflows Deployed

1. **Memory Ingestion**: Captures incoming WhatsApp and Telegram messages, structures them, and pushes them to [[Notion Memory Hub]].
2. **Device Sync**: Mirrors settings and states between [[CasaTAO Dashboard]] and [[ARC Anandaz Dashboard]].
3. **Agent Triggering**: Monitors the [[Manus Task Queue]] and spins up autonomous agents to execute complex tasks.

## Inter-System Topology

- **Input**: Webhooks from Telegram, GitHub, or local Home Assistant.
- **Processor**: n8n node networks utilizing [[CRT Model Routing]] for text classification.
- **Output**: Writes to [[Notion Memory Hub]], updates [[Y-WORLD Dashboard]], or triggers [[Manus Operations]].\n