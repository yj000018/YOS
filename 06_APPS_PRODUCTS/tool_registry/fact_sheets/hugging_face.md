# Hugging Face - Y-OS Tool Fact Sheet

## Overview
**Category:** AI/ML
**Description:** Model hub & inference API

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api-inference.huggingface.co`
**Environment Variable:** `HUGGING_FACE_API_KEY`

### 1Password Integration
**1Password Item:** `HuggingFace API Key`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `api_key` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Hugging Face.
