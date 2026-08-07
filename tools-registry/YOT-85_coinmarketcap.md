---
tool_id: YOT-85
tool_name: "CoinMarketCap"
tool_type: "MCP Connector"
category: "Crypto Market Intelligence"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://coinmarketcap.com/api/"
auth_credentials: "API Key"
tags: ["crypto", "market", "finance", "data"]
created_date: "2026-08-07"
---
# 🟢 YOT-85 — CoinMarketCap
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Crypto Market Intelligence |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | API Key |
| **URL** | https://coinmarketcap.com/api/ |
## Business Value
CoinMarketCap provides comprehensive cryptocurrency market intelligence, enabling Y-OS to track live prices, analyze market trends, and retrieve critical on-chain metrics for informed financial decision-making.
## Capabilities
- Live quotes and historical cryptocurrency prices
- Technical analysis (MA/EMA/MACD/RSI/Fibonacci)
- On-chain and derivatives metrics
- Global sentiment (Fear & Greed, BTC dominance, altcoin season)
- Trending narratives, macro events, and crypto news
## Dependencies
- CoinMarketCap API Key
- Active internet connection for real-time data retrieval
## Known Limits & Bugs
- Free tier has strict rate limits and limited historical data access.
- Some advanced technical indicators may require higher-tier subscriptions.
## Workarounds & Lessons
- Implement caching for frequently requested data (like global metrics) to minimize API calls and avoid rate limits.
- Use bulk endpoints where possible to fetch data for multiple assets in a single request.
