---
type: world-node
status: active
domain: Y-WORLD
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Automation Safety Rules

To protect the integrity of Y-WORLD, all automation scripts, agents (including Manus), and external APIs must comply with these safety rules.

## 1. Core Safety Rules
* **Rule 1 (No Blind Deletion)**: Never delete markdown files, attachments, or system folders without explicit, double-confirmed human instructions.
* **Rule 2 (No Config Tampering)**: Never modify the `.obsidian/` folder, community plugin settings, or hotkeys without creating a backup first.
* **Rule 3 (Local REST Security)**: The Local REST API must be configured with a secure, non-exposed token. Never commit API keys or tokens into markdown notes.
* **Rule 4 (Git as Truth)**: Ensure Git auto-backup is active. Before running any bulk automation script, perform a manual Git commit.
* **Rule 5 (Fallback Paths)**: Every automated workflow (e.g., n8n, Local REST API, Shell Commands) must have a fallback manual execution path documented.

## 2. Execution Guardrails
* Limit API call loops to a maximum of 3 iterations.
* If a network error or API timeout occurs, retry twice immediately, then wait 1 minute, then 5 minutes, then escalate to the user.
