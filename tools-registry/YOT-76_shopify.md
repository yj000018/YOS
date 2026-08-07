---
tool_id: YOT-76
tool_name: "Shopify"
tool_type: "MCP Connector"
category: "E-commerce"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://shopify.dev/docs/api"
auth_credentials: "OAuth MCP"
tags: ["ecommerce", "store", "products", "orders"]
created_date: "2026-08-07"
---
# 🟢 YOT-76 — Shopify
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | E-commerce |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://shopify.dev/docs/api |
## Business Value
Provides comprehensive programmatic control over Shopify storefronts, enabling automated inventory management, order processing, and product catalog updates directly from Y-OS.
## Capabilities
- Manage products, variants, and collections
- Process and fulfill orders
- Create and manage discounts
- Monitor and update inventory levels
## Dependencies
- Shopify Admin API access
- OAuth authentication via MCP
## Known Limits & Bugs
- API rate limits apply based on the Shopify plan
- Strict adherence to Shopify GID format required for all IDs (e.g., 'gid://shopify/<Type>/<numeric_id>')
- Field names must exactly match the schema (no camelCase conversions)
## Workarounds & Lessons
- Always use exact field names as declared in the tool's input schema.
- If a tool call fails, report the error directly rather than falling back to browser or curl/fetch operations.
