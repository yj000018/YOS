---
tool_id: YOT-83
tool_name: "Wireflow"
tool_type: "MCP Connector"
category: "AI Workflow Orchestration"
status: "Production"
pricing: "Paid"
source_type: "Officiel"
source_url: "https://wireflow.ai/"
auth_credentials: "OAuth MCP"
tags: ["ai", "workflow", "orchestration", "image", "video", "audio"]
created_date: "2026-08-07"
---
# 🟢 YOT-83 — Wireflow

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | AI Workflow Orchestration |
| **Statut** | Production |
| **Pricing** | Paid |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://wireflow.ai/ |

## Business Value
Wireflow enables seamless orchestration of complex AI pipelines by chaining image, video, and audio models into unified workflows. It significantly accelerates the production of multi-modal AI assets by automating the transitions between different generation and processing steps.

## Capabilities
- List available AI workflows
- Inspect workflow configurations and required inputs
- Run AI workflows chaining image, video, and audio models
- Retrieve execution status and output URLs

## Dependencies
- Wireflow account and active subscription/credits
- OAuth authentication via MCP

## Known Limits & Bugs
- Only `run_workflow` consumes credits; other tools are read-only.
- Execution is asynchronous; requires polling `get_execution` with the returned executionId until status is complete.

## Workarounds & Lessons
- Implement robust polling mechanisms with appropriate delays when waiting for workflow completion to avoid rate limits.
- Always inspect workflow requirements before running to ensure all necessary inputs are provided.
