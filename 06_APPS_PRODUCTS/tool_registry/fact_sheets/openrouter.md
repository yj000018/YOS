# OpenRouter - Y-OS Tool Fact Sheet

## Overview
**Category:** AI/LLM
**Description:** Unified API for 100+ LLM models

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://openrouter.ai/api/v1`
**Environment Variable:** `OPENROUTER_API_KEY`

### 1Password Integration
**1Password Item:** `OpenRouter API Key`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `builtin_secret + mcp_token` |
| **ChatGPT** | `api_key` |
| **Claude** | `api_key` |

## Notes
Manus built-in + MCP connector.
