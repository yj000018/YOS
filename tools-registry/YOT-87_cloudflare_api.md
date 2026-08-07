---
tool_id: YOT-87
tool_name: "Cloudflare API"
tool_type: "MCP Connector"
category: "Web Infrastructure"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://developers.cloudflare.com/"
auth_credentials: "API Token"
tags: ["cloudflare", "dns", "workers", "r2", "security", "infrastructure"]
created_date: "2026-08-07"
---
# 🟢 YOT-87 — Cloudflare API

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Web Infrastructure |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | API Token |
| **URL** | https://developers.cloudflare.com/ |

## Business Value
The Cloudflare API provides programmatic control over web infrastructure, enabling automated deployment, security management, and edge computing. It allows Y-OS to seamlessly orchestrate DNS, serverless functions, and object storage for robust application delivery.

## Capabilities
- Manage DNS records and zones
- Deploy and configure Cloudflare Workers
- Manage R2 object storage buckets
- Configure security settings and WAF rules
- Handle SSL/TLS certificates

## Dependencies
- Cloudflare account
- Valid API Token with appropriate permissions (`CLOUDFLARE_API_TOKEN`)

## Known Limits & Bugs
- API rate limits apply depending on the account tier.
- Some advanced security features require Enterprise plans.

## Workarounds & Lessons
- Ensure the API token has scoped permissions rather than using the Global API Key for better security.
- When managing multiple accounts, explicitly specify the Account ID in API calls.
