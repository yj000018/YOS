# n8n - Y-OS Tool Fact Sheet

## Overview
**Category:** Automation
**Description:** Self-hosted workflow automation

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://your-n8n.io/api/v1`
**Environment Variable:** `N8N_API_KEY`

### 1Password Integration
**1Password Item:** `n8n yOS - API`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `api_key` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP n8n.
