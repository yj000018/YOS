---
tool_id: YOT-93
tool_name: "Dupe"
tool_type: "MCP Connector"
category: "Product Alternative Finder"
status: "Production"
pricing: "Free"
source_type: "Officiel"
source_url: "https://dupe.com/"
auth_credentials: "None"
tags: ["shopping", "alternatives", "furniture", "fashion"]
created_date: "2026-08-07"
---
# 🟢 YOT-93 — Dupe
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Product Alternative Finder |
| **Statut** | Production |
| **Pricing** | Free |
| **Source** | Officiel |
| **Auth** | None |
| **URL** | https://dupe.com/
## Business Value
Dupe provides a fast and efficient way to discover visually similar, affordable product alternatives for furniture and fashion items. It enhances the shopping experience by allowing users to find budget-friendly options without compromising on style.
## Capabilities
- Search for visually similar product alternatives based on category.
- Find affordable dupes for furniture and fashion items.
- Look up products using full product page URLs.
## Dependencies
- No authentication required.
- Requires exact casing for categories (e.g., 'Furniture', 'Fashion').
- URL lookups require the full product page URL passed as a string.
## Known Limits & Bugs
- `search_category` must use exact casing (e.g., 'Furniture', 'Fashion').
- Only supports specific categories like furniture and fashion.
## Workarounds & Lessons
- Always ensure the category string matches the exact casing required by the API.
- When performing URL lookups, verify that the complete product page URL is provided rather than a shortened or partial link.
