---
type: protocol
status: active
domain: Y-OS
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Manus Commands

This document records the exact Advanced URI or Local REST API commands that Manus can trigger.

## 🔗 Advanced URI Commands
* **Open HOME**: `obsidian://advanced-uri?vault=Y-WORLD&filepath=01_Cockpit%2FHOME.md`
* **Open Root Map**: `obsidian://advanced-uri?vault=Y-WORLD&filepath=02_Maps%2FY-WORLD%20ROOT%20MAP.md`
* **New K-Card**: `obsidian://advanced-uri?vault=Y-WORLD&command=quickadd%3Acreate-k-card`

## 🌐 Local REST API Commands
* **Read Note**: `GET /files/01_Cockpit/HOME.md`
* **Update Note**: `PUT /files/01_Cockpit/HOME.md`
* **Get Vault Info**: `GET /`
