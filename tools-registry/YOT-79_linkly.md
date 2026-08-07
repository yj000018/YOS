---
tool_id: YOT-79
tool_name: "Linkly"
tool_type: "MCP Connector"
category: "URL Shortening & Analytics"
status: "Production"
pricing: "Paid"
source_type: "Officiel"
source_url: "https://linklyhq.com/"
auth_credentials: "OAuth MCP"
tags: ["url-shortener", "analytics", "marketing", "tracking"]
created_date: "2026-08-07"
---
# 🟢 YOT-79 — Linkly
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | URL Shortening & Analytics |
| **Statut** | Production |
| **Pricing** | Paid |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://linklyhq.com/
## Business Value
Linkly provides robust URL shortening and click analytics, enabling precise tracking of marketing campaigns and user engagement within the Y-OS ecosystem. It allows for custom domains and detailed traffic insights to optimize digital strategies.
## Capabilities
- Create, update, and delete short links
- Track click analytics and traffic sources
- Manage custom domains and workspace settings
- Search and list existing links
## Dependencies
- Linkly account with appropriate subscription plan
- OAuth authentication via MCP
## Known Limits & Bugs
- Link IDs are integers and must be retrieved via search_links or list_links before updating or deleting.
- Rate limits may apply depending on the subscription tier.
## Workarounds & Lessons
- Always use `search_links` or `list_links` to find the integer ID of a link before attempting to modify or retrieve its specific details.
