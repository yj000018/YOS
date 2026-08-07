---
tool_id: YOT-88
tool_name: "Cloudflare Worker Bindings"
tool_type: "MCP Connector"
category: "Edge Computing"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://developers.cloudflare.com/workers/"
auth_credentials: "OAuth MCP"
tags: ["cloudflare", "workers", "edge", "serverless", "kv", "r2", "d1"]
created_date: "2026-08-07"
---
# 🟢 YOT-88 — Cloudflare Worker Bindings
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Edge Computing |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://developers.cloudflare.com/workers/

## Business Value
Provides direct access to Cloudflare's edge computing primitives, enabling rapid deployment and management of serverless applications, databases, and storage globally. It empowers Y-OS to orchestrate high-performance, low-latency backend services directly at the edge.

## Capabilities
- Manage Cloudflare Workers deployments and configurations.
- Interact with D1 relational databases (SQL execution).
- Manage R2 object storage buckets and objects.
- Access and modify KV (Key-Value) stores.
- Configure Hyperdrive for database connection pooling.

## Dependencies
- Cloudflare account with active Workers/Pages subscription.
- OAuth authorization via MCP.

## Known Limits & Bugs
- D1 database queries may have execution time limits and size constraints.
- R2 operations might require specific bucket configurations for public access.
- Worker deployment sizes are limited by the Cloudflare plan tier.

## Workarounds & Lessons
- For large data operations in D1, batch queries to avoid timeout limits.
- Use KV for read-heavy, infrequently updated data, and D1 for relational data.
- Ensure proper environment variable bindings are set before deploying Workers.
