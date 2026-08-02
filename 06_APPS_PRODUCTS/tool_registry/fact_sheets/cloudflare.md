# Cloudflare - Y-OS Tool Fact Sheet

## Overview
**Category:** Dev/Infra
**Description:** CDN, DNS, Workers, security

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.cloudflare.com/client/v4`
**Environment Variable:** `CLOUDFLARE_API_TOKEN`

### 1Password Integration
**1Password Item:** `Cloudflare API Token`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `builtin_secret + mcp_token` |
| **ChatGPT** | `api_key` |
| **Claude** | `api_key` |

## Notes
Manus built-in + MCP Cloudflare Worker Bindings.
