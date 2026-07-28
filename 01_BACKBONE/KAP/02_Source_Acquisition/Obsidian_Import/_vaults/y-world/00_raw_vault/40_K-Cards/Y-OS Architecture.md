---
type: k-card
domain: Y-OS
tags: [yos, architecture, cognitive-os, system]
created: 2026-05-29
status: active
---

# Y-OS Architecture

**Y-OS** (World Operating System) is the cognitive infrastructure layer that connects all tools, agents, spaces, and knowledge in [[Y-WORLD]].

## Layer Model

```
Layer 4 — INTERFACES    : Obsidian, Notion, Voice, Mobile
Layer 3 — AGENTS        : Manus, n8n, Claude, GPT-5
Layer 2 — MEMORY        : Notion Memory Hub, Mem0, GitHub
Layer 1 — ROUTING       : CRT Model Routing, Tool Router
Layer 0 — HARDWARE      : MiniPC, Coral Edge TPU, Starlink
```

## Core Components

- **[[CRT Model Routing]]** — intelligent LLM traffic director
- **[[n8n Cognitive Automation]]** — workflow orchestrator
- **[[Notion Memory Hub]]** — persistent semantic memory
- **[[Manus Operations]]** — primary AI operator interface
- **[[Frigate NVR]]** — physical world sensor layer

## Physical Nodes

| Location | Hardware | Role |
| :--- | :--- | :--- |
| [[CasaTAO]] | MiniPC x2 + Coral TPU | Primary production node |
| [[ARC Anandaz]] | Raspberry Pi 5 | Offline-first backup node |
| Cloud | Vercel + Supabase | Public-facing interfaces |
