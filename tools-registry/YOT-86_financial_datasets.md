---
tool_id: YOT-86
tool_name: "Financial Datasets"
tool_type: "MCP Connector"
category: "Financial Market Data"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://financialdatasets.ai/"
auth_credentials: "API Key"
tags: ["finance", "market data", "stocks", "SEC filings"]
created_date: "2026-08-07"
---
# 🟢 YOT-86 — Financial Datasets

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Financial Market Data |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | API Key |
| **URL** | https://financialdatasets.ai/ |

## Business Value
Financial Datasets provides comprehensive and reliable financial market data, enabling Y-OS to perform deep quantitative analysis, algorithmic trading research, and automated investment reporting. It bridges the gap between raw financial data and actionable insights for public companies.

## Capabilities
- Retrieve real-time and historical stock prices.
- Access detailed company financials (income statements, balance sheets, cash flows).
- Fetch and analyze SEC filings.
- Track insider trades and institutional ownership.

## Dependencies
- Financial Datasets API Key configured in the environment.
- Network access to the Financial Datasets API endpoints.

## Known Limits & Bugs
- Rate limits apply based on the freemium tier subscription.
- Historical data depth may be restricted for free accounts.
- Real-time data might have slight delays depending on the exchange and subscription level.

## Workarounds & Lessons
- Implement caching for historical data and SEC filings to minimize API calls and avoid rate limits.
- Use batch requests where possible to optimize credit usage.
- Always verify the timestamp of real-time quotes before executing time-sensitive operations.
