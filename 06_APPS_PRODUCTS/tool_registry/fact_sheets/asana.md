# Asana - Y-OS Tool Fact Sheet

## Overview
**Category:** Project Management
**Description:** Project & task management

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://app.asana.com/api/1.0`
**Environment Variable:** `ASANA_ACCESS_TOKEN`

### 1Password Integration
**1Password Item:** `Asana PAT — yOS-Manus`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `oauth` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Asana.
