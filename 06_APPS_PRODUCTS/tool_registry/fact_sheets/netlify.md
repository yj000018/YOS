# Netlify - Y-OS Tool Fact Sheet

## Overview
**Category:** Dev/Deploy
**Description:** Web deployment & serverless

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.netlify.com/api/v1`
**Environment Variable:** `NETLIFY_ACCESS_TOKEN`

### 1Password Integration
**1Password Item:** `Netlify PAT — yOS-Manus`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `oauth` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Netlify.
