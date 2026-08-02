# Airtable - Y-OS Tool Fact Sheet

## Overview
**Category:** Data
**Description:** Low-code database platform

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.airtable.com/v0`
**Environment Variable:** `AIRTABLE_API_KEY`

### 1Password Integration
**1Password Item:** `Airtable PAT — yOS-Manus`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `oauth` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Airtable.
