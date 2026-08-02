#!/usr/bin/env python3
"""
Construit le Y-OS Tool Registry complet
Pour chaque outil : auth method, endpoint, accès par plateforme LLM, credentials 1P
"""

import json

# ─── Auth methods ──────────────────────────────────────────────────────────────
AUTH_API_KEY = "api_key"
AUTH_OAUTH = "oauth"
AUTH_MCP_TOKEN = "mcp_token"  # Token injecté par Manus dans le MCP server
AUTH_BEARER = "bearer"
AUTH_NONE = "none"

# ─── Plateformes LLM ──────────────────────────────────────────────────────────
MANUS = "manus"
CHATGPT = "chatgpt"
CLAUDE = "claude"
GEMINI = "gemini"

# ─── Registre complet ─────────────────────────────────────────────────────────
# Format: {name, category, description, auth_method, auth_note, endpoint,
#          manus_access, chatgpt_access, claude_access, env_var, 1p_item, notes}

TOOL_REGISTRY = [
    # ═══════════════════════════════════════════════════════════════════════════
    # AI / LLM
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "OpenAI", "category": "AI/LLM", "description": "GPT models, DALL-E, Whisper, Embeddings",
     "auth_method": AUTH_API_KEY, "env_var": "OPENAI_API_KEY", "endpoint": "https://api.openai.com/v1",
     "manus_access": "builtin_secret", "chatgpt_access": "native", "claude_access": "api_key",
     "1p_item": "OpenAI API Key", "notes": "Manus built-in. ChatGPT = native. Claude via API."},

    {"name": "Anthropic", "category": "AI/LLM", "description": "Claude models",
     "auth_method": AUTH_API_KEY, "env_var": "ANTHROPIC_API_KEY", "endpoint": "https://api.anthropic.com",
     "manus_access": "builtin_secret", "chatgpt_access": "api_key", "claude_access": "native",
     "1p_item": "Anthropic Claude API Key", "notes": "Manus built-in."},

    {"name": "Google Gemini", "category": "AI/LLM", "description": "Gemini models",
     "auth_method": AUTH_API_KEY, "env_var": "GEMINI_API_KEY", "endpoint": "https://generativelanguage.googleapis.com",
     "manus_access": "builtin_secret", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Google Gemini API Key", "notes": "Manus built-in."},

    {"name": "Grok (xAI)", "category": "AI/LLM", "description": "Grok models by xAI",
     "auth_method": AUTH_API_KEY, "env_var": "XAI_API_KEY", "endpoint": "https://api.x.ai",
     "manus_access": "builtin_secret", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "X.ai API", "notes": "Manus built-in."},

    {"name": "Perplexity", "category": "AI/LLM", "description": "Sonar web-grounded AI search",
     "auth_method": AUTH_API_KEY, "env_var": "SONAR_API_KEY", "endpoint": "https://api.perplexity.ai",
     "manus_access": "builtin_secret", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Perplexity AI + API Key", "notes": "Manus built-in."},

    {"name": "OpenRouter", "category": "AI/LLM", "description": "Unified API for 100+ LLM models",
     "auth_method": AUTH_API_KEY, "env_var": "OPENROUTER_API_KEY", "endpoint": "https://openrouter.ai/api/v1",
     "manus_access": "builtin_secret + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "OpenRouter API Key", "notes": "Manus built-in + MCP connector."},

    {"name": "Groq", "category": "AI/LLM", "description": "Ultra-fast inference (LPU)",
     "auth_method": AUTH_API_KEY, "env_var": "GROQ_API_KEY", "endpoint": "https://api.groq.com/openai/v1",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Groq API", "notes": "Custom API connector créé batch 1."},

    {"name": "DeepSeek", "category": "AI/LLM", "description": "DeepSeek R1/V3 models",
     "auth_method": AUTH_API_KEY, "env_var": "DEEPSEEK_API_KEY", "endpoint": "https://api.deepseek.com",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "DeepSeek API", "notes": "Custom API connector créé batch 1."},

    {"name": "Cohere", "category": "AI/LLM", "description": "Command models, embeddings, rerank",
     "auth_method": AUTH_API_KEY, "env_var": "COHERE_API_KEY", "endpoint": "https://api.cohere.ai/v1",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Cohere API Key", "notes": "Custom API connector créé batch 1."},

    {"name": "Mistral", "category": "AI/LLM", "description": "Mistral models",
     "auth_method": AUTH_API_KEY, "env_var": "MISTRAL_API_KEY", "endpoint": "https://api.mistral.ai/v1",
     "manus_access": "none", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Mistral API Key", "notes": "Pas de connector Manus actif."},

    # ═══════════════════════════════════════════════════════════════════════════
    # AI / Image & Video Generation
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Flux (BFL)", "category": "AI/Image", "description": "FLUX image generation models",
     "auth_method": AUTH_API_KEY, "env_var": "BFL_API_KEY", "endpoint": "https://api.bfl.ai",
     "manus_access": "builtin_secret + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Flux API Key", "notes": "Manus built-in + MCP Flux connector."},

    {"name": "Replicate", "category": "AI/Image", "description": "1000+ AI models (image, video, audio)",
     "auth_method": AUTH_API_KEY, "env_var": "REPLICATE_API_TOKEN", "endpoint": "https://api.replicate.com/v1",
     "manus_access": "custom_api_editable", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Replicate API Key", "notes": "Custom API editable existant."},

    {"name": "Stability AI", "category": "AI/Image", "description": "Stable Diffusion models",
     "auth_method": AUTH_API_KEY, "env_var": "STABILITY_API_KEY", "endpoint": "https://api.stability.ai",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Stability AI API", "notes": "Custom API connector créé batch 1."},

    {"name": "Fal.ai", "category": "AI/Image", "description": "Fast AI inference (image, video)",
     "auth_method": AUTH_API_KEY, "env_var": "FAL_API_KEY", "endpoint": "https://fal.run",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "fal.ai API Key", "notes": "Custom API connector créé batch 1."},

    {"name": "HeyGen", "category": "AI/Video", "description": "AI avatar video generation",
     "auth_method": AUTH_API_KEY, "env_var": "HEYGEN_API_KEY", "endpoint": "https://api.heygen.com/v2",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "HeyGen API Key — yOS-Manus", "notes": "Custom API + MCP HeyGen."},

    {"name": "Higgsfield", "category": "AI/Video", "description": "Cinematic AI video generation",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "HIGGSFIELD_API_KEY", "endpoint": "https://api.higgsfield.ai",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed by Manus. Pas de clé dans 1P."},

    {"name": "Magnific", "category": "AI/Image", "description": "AI image upscaling & generation",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "MAGNIFIC_API_KEY", "endpoint": "https://api.magnific.ai",
     "manus_access": "mcp_token", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": None, "notes": "MCP managed by Manus."},

    {"name": "MiniMax", "category": "AI/Video", "description": "Video, image, music generation",
     "auth_method": AUTH_API_KEY, "env_var": "MINIMAX_API_KEY", "endpoint": "https://api.minimax.chat",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # AI / Audio & Voice
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "ElevenLabs", "category": "AI/Audio", "description": "TTS, voice cloning, dubbing",
     "auth_method": AUTH_API_KEY, "env_var": "ELEVENLABS_API_KEY", "endpoint": "https://api.elevenlabs.io/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "ElevenLabs API Key", "notes": "Custom API + MCP ElevenLabs."},

    {"name": "Hume AI", "category": "AI/Audio", "description": "Expressive TTS, emotional voice",
     "auth_method": AUTH_API_KEY, "env_var": "HUME_API_KEY", "endpoint": "https://api.hume.ai",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Hume API", "notes": "Custom API + MCP Hume."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Search & Web
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Exa", "category": "Search", "description": "Neural web search & content extraction",
     "auth_method": AUTH_API_KEY, "env_var": "EXA_API_KEY", "endpoint": "https://api.exa.ai",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "EXA API Key", "notes": "Custom API + MCP Exa."},

    {"name": "Firecrawl", "category": "Search", "description": "Web scraping with clean markdown",
     "auth_method": AUTH_API_KEY, "env_var": "FIRECRAWL_API_KEY", "endpoint": "https://api.firecrawl.dev/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Firecrawl API key", "notes": "Custom API + MCP Firecrawl."},

    {"name": "Tavily", "category": "Search", "description": "AI-optimized web search",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "TAVILY_API_KEY", "endpoint": "https://api.tavily.com",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Bright Data", "category": "Search", "description": "Web scraping & proxy network",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "BRIGHTDATA_API_KEY", "endpoint": "https://api.brightdata.com",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Apify", "category": "Search", "description": "Web scraping actors platform",
     "auth_method": AUTH_API_KEY, "env_var": "APIFY_API_KEY", "endpoint": "https://api.apify.com/v2",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Apify — yOS-APIFY-MCP-2026-03", "notes": "Custom API + MCP Apify."},

    {"name": "Semrush", "category": "SEO", "description": "SEO, keywords, backlinks, traffic",
     "auth_method": AUTH_API_KEY, "env_var": "SEMRUSH_API_KEY", "endpoint": "https://api.semrush.com",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Semrush", "notes": "Custom API + MCP Semrush."},

    {"name": "Ahrefs", "category": "SEO", "description": "SEO backlinks, keywords, rank tracking",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "AHREFS_API_KEY", "endpoint": "https://api.ahrefs.com/mcp",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Productivity & Notes
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Notion", "category": "Productivity", "description": "Workspace, databases, pages",
     "auth_method": AUTH_API_KEY, "env_var": "NOTION_API_KEY", "endpoint": "https://api.notion.com/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth + api_key", "claude_access": "api_key",
     "1p_item": "Notion API Key", "notes": "Custom API + MCP Notion. ChatGPT via OAuth ou API key."},

    {"name": "Mem0", "category": "Memory", "description": "AI memory layer cross-session",
     "auth_method": AUTH_API_KEY, "env_var": "MEM0_API_KEY", "endpoint": "https://api.mem0.ai",
     "manus_access": "custom_api_editable", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Mem0 — yOS-MEM0-MCP-2026-03", "notes": "Custom API editable existant."},

    {"name": "Raindrop.io", "category": "Productivity", "description": "Bookmark manager",
     "auth_method": AUTH_API_KEY, "env_var": "RAINDROP_API_KEY", "endpoint": "https://api.raindrop.io/rest/v1",
     "manus_access": "custom_api_editable + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Raindrop API", "notes": "Custom API editable + MCP Raindrop."},

    {"name": "Heptabase", "category": "Knowledge", "description": "Visual knowledge base & whiteboards",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "HEPTABASE_API_KEY", "endpoint": "https://api.heptabase.com",
     "manus_access": "mcp_token", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Todoist", "category": "Productivity", "description": "Task management",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "TODOIST_API_KEY", "endpoint": "https://api.todoist.com/rest/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Project Management
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Linear", "category": "Project Management", "description": "Issue tracking for dev teams",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "LINEAR_API_KEY", "endpoint": "https://api.linear.app/graphql",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Asana", "category": "Project Management", "description": "Project & task management",
     "auth_method": AUTH_API_KEY, "env_var": "ASANA_ACCESS_TOKEN", "endpoint": "https://app.asana.com/api/1.0",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Asana PAT — yOS-Manus", "notes": "Custom API + MCP Asana."},

    {"name": "ClickUp", "category": "Project Management", "description": "All-in-one project management",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "CLICKUP_API_KEY", "endpoint": "https://api.clickup.com/api/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "monday.com", "category": "Project Management", "description": "Work OS platform",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "MONDAY_API_KEY", "endpoint": "https://api.monday.com/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Wrike", "category": "Project Management", "description": "Enterprise project management",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "WRIKE_API_KEY", "endpoint": "https://www.wrike.com/api/v4",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Communication & Messaging
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Slack", "category": "Communication", "description": "Team messaging & automation",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "SLACK_BOT_TOKEN", "endpoint": "https://slack.com/api",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Bot token à ajouter dans 1P."},

    {"name": "Telegram", "category": "Communication", "description": "Telegram bot automation",
     "auth_method": AUTH_API_KEY, "env_var": "TELEGRAM_BOT_TOKEN", "endpoint": "https://api.telegram.org",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Telegram Bot — yOS-TELEGRAM-2026-03", "notes": "Custom API connector créé batch 1."},

    {"name": "Twilio", "category": "Communication", "description": "SMS, voice, messaging APIs",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "TWILIO_AUTH_TOKEN", "endpoint": "https://api.twilio.com/2010-04-01",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed (Twilio Documentation). Clé à ajouter dans 1P."},

    {"name": "Resend", "category": "Email", "description": "Transactional email API",
     "auth_method": AUTH_API_KEY, "env_var": "RESEND_API_KEY", "endpoint": "https://api.resend.com",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Resend — yOS-RESEND-MCP-2026-06", "notes": "Custom API + MCP Resend."},

    {"name": "MailerLite", "category": "Email", "description": "Email marketing & automation",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "MAILERLITE_API_KEY", "endpoint": "https://connect.mailerlite.com/api",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # CRM & Sales
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "HubSpot", "category": "CRM", "description": "CRM, marketing, sales hub",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "HUBSPOT_API_KEY", "endpoint": "https://api.hubapi.com",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Klaviyo", "category": "CRM", "description": "Email & SMS marketing platform",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "KLAVIYO_API_KEY", "endpoint": "https://a.klaviyo.com/api",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Developer & Infrastructure
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "GitHub", "category": "Dev", "description": "Code hosting, CI/CD, PRs",
     "auth_method": AUTH_API_KEY, "env_var": "GITHUB_PAT", "endpoint": "https://api.github.com",
     "manus_access": "custom_api_editable + builtin", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "GitHub PAT — yOS-GITHUB-MCP-2026-03", "notes": "Custom API editable + builtin OAuth."},

    {"name": "Vercel", "category": "Dev/Deploy", "description": "Frontend deployment platform",
     "auth_method": AUTH_API_KEY, "env_var": "VERCEL_API_TOKEN", "endpoint": "https://api.vercel.com",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Vercel PAT — yOS-Manus", "notes": "Custom API + MCP Vercel."},

    {"name": "Netlify", "category": "Dev/Deploy", "description": "Web deployment & serverless",
     "auth_method": AUTH_API_KEY, "env_var": "NETLIFY_ACCESS_TOKEN", "endpoint": "https://api.netlify.com/api/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Netlify PAT — yOS-Manus", "notes": "Custom API + MCP Netlify."},

    {"name": "Fly.io", "category": "Dev/Deploy", "description": "App deployment platform",
     "auth_method": AUTH_API_KEY, "env_var": "FLY_API_TOKEN", "endpoint": "https://api.fly.io/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Fly.io — yOS-WEBHOOK-2026-03", "notes": "Custom API + MCP Fly.io."},

    {"name": "Cloudflare", "category": "Dev/Infra", "description": "CDN, DNS, Workers, security",
     "auth_method": AUTH_API_KEY, "env_var": "CLOUDFLARE_API_TOKEN", "endpoint": "https://api.cloudflare.com/client/v4",
     "manus_access": "builtin_secret + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Cloudflare API Token", "notes": "Manus built-in + MCP Cloudflare Worker Bindings."},

    {"name": "Supabase", "category": "Dev/DB", "description": "Open-source Firebase alternative",
     "auth_method": AUTH_API_KEY, "env_var": "SUPABASE_ACCESS_TOKEN", "endpoint": "https://api.supabase.com",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Supabase — yOS-SUPABASE-MCP-2026-03", "notes": "Custom API + MCP Supabase."},

    {"name": "Sentry", "category": "Dev/Monitoring", "description": "Error tracking & performance",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "SENTRY_AUTH_TOKEN", "endpoint": "https://sentry.io/api/0",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Data & Analytics
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Airtable", "category": "Data", "description": "Low-code database platform",
     "auth_method": AUTH_API_KEY, "env_var": "AIRTABLE_API_KEY", "endpoint": "https://api.airtable.com/v0",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Airtable PAT — yOS-Manus", "notes": "Custom API + MCP Airtable."},

    {"name": "Algolia", "category": "Data", "description": "Search-as-a-service",
     "auth_method": AUTH_API_KEY, "env_var": "ALGOLIA_API_KEY", "endpoint": "https://APPID.algolia.net",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Algolia — yOS-ALGOLIA-2026-03", "notes": "Custom API connector créé batch 3."},

    {"name": "Pinecone", "category": "Data/Vector", "description": "Vector database for AI",
     "auth_method": AUTH_API_KEY, "env_var": "PINECONE_API_KEY", "endpoint": "https://api.pinecone.io",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Pinecone RAG - API Key", "notes": "Custom API connector créé batch 1."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Automation
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Zapier", "category": "Automation", "description": "No-code workflow automation",
     "auth_method": AUTH_API_KEY, "env_var": "ZAPIER_API_KEY", "endpoint": "https://api.zapier.com",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Zapier", "notes": "Custom API + MCP Zapier."},

    {"name": "Make (Integromat)", "category": "Automation", "description": "Visual workflow automation",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "MAKE_API_KEY", "endpoint": "https://eu1.make.com/api/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "n8n", "category": "Automation", "description": "Self-hosted workflow automation",
     "auth_method": AUTH_API_KEY, "env_var": "N8N_API_KEY", "endpoint": "https://your-n8n.io/api/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "n8n yOS - API", "notes": "Custom API + MCP n8n."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Design & Creative
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Canva", "category": "Design", "description": "Online design platform",
     "auth_method": AUTH_OAUTH, "env_var": "CANVA_API_KEY", "endpoint": "https://api.canva.com/rest/v1",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "oauth",
     "1p_item": None, "notes": "OAuth principal. MCP managed by Manus. Clé API à ajouter dans 1P."},

    {"name": "Miro", "category": "Design", "description": "Collaborative whiteboard",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "MIRO_ACCESS_TOKEN", "endpoint": "https://api.miro.com/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Token à ajouter dans 1P."},

    {"name": "Figma", "category": "Design", "description": "UI/UX design tool",
     "auth_method": AUTH_API_KEY, "env_var": "FIGMA_API_KEY", "endpoint": "https://api.figma.com/v1",
     "manus_access": "none", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "Pas de connector Manus actif. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Finance & Crypto
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Stripe", "category": "Finance", "description": "Payment processing",
     "auth_method": AUTH_API_KEY, "env_var": "STRIPE_SECRET_KEY", "endpoint": "https://api.stripe.com/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Stripe (Y-media)", "notes": "Custom API + MCP Stripe."},

    {"name": "Crypto.com", "category": "Finance/Crypto", "description": "Crypto exchange API",
     "auth_method": AUTH_API_KEY, "env_var": "CRYPTO_COM_API_KEY", "endpoint": "https://api.crypto.com/exchange/v1",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Crypto.com", "notes": "Custom API + MCP Crypto.com."},

    {"name": "CoinGecko", "category": "Finance/Crypto", "description": "Crypto market data",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "COINGECKO_API_KEY", "endpoint": "https://api.coingecko.com/api/v3",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Alpha Vantage", "category": "Finance", "description": "Stock & financial market data",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "ALPHA_VANTAGE_API_KEY", "endpoint": "https://www.alphavantage.co/query",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Scheduling & Calendar
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Cal.com", "category": "Scheduling", "description": "Open-source scheduling",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "CAL_API_KEY", "endpoint": "https://api.cal.com/v1",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Calendly", "category": "Scheduling", "description": "Meeting scheduling",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "CALENDLY_API_KEY", "endpoint": "https://api.calendly.com",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Zoom", "category": "Scheduling", "description": "Video conferencing & recordings",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "ZOOM_API_KEY", "endpoint": "https://api.zoom.us/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "oauth",
     "1p_item": None, "notes": "MCP managed. OAuth principal."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Meeting Intelligence
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Fireflies.ai", "category": "Meeting", "description": "Meeting transcription & AI notes",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "FIREFLIES_API_KEY", "endpoint": "https://api.fireflies.ai/graphql",
     "manus_access": "mcp_token", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Fathom", "category": "Meeting", "description": "AI meeting notes & summaries",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "FATHOM_API_KEY", "endpoint": "https://fathom.video/api",
     "manus_access": "mcp_token", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Granola", "category": "Meeting", "description": "AI meeting intelligence",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "GRANOLA_API_KEY", "endpoint": "https://api.granola.ai",
     "manus_access": "mcp_token", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Storage & Files
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Dropbox", "category": "Storage", "description": "Cloud file storage",
     "auth_method": AUTH_OAUTH, "env_var": "DROPBOX_ACCESS_TOKEN", "endpoint": "https://api.dropboxapi.com/2",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "oauth", "claude_access": "oauth",
     "1p_item": "Dropbox", "notes": "Custom API + MCP Dropbox. OAuth principal."},

    {"name": "Cloudinary", "category": "Storage", "description": "Media asset management",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "CLOUDINARY_API_KEY", "endpoint": "https://api.cloudinary.com/v1_1",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Web Publishing
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Webflow", "category": "Web", "description": "No-code web design & CMS",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "WEBFLOW_API_KEY", "endpoint": "https://api.webflow.com/v2",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Wix", "category": "Web", "description": "Website builder platform",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "WIX_API_KEY", "endpoint": "https://www.wixapis.com",
     "manus_access": "mcp_token", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Sanity", "category": "Web/CMS", "description": "Headless CMS",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "SANITY_API_KEY", "endpoint": "https://api.sanity.io",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Forms & Surveys
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Tally", "category": "Forms", "description": "No-code form builder",
     "auth_method": AUTH_API_KEY, "env_var": "TALLY_API_KEY", "endpoint": "https://api.tally.so",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Tally API", "notes": "Custom API + MCP Tally."},

    {"name": "Typeform", "category": "Forms", "description": "Conversational forms",
     "auth_method": AUTH_API_KEY, "env_var": "TYPEFORM_API_KEY", "endpoint": "https://api.typeform.com",
     "manus_access": "builtin_secret", "chatgpt_access": "oauth", "claude_access": "api_key",
     "1p_item": "Typeform API Key", "notes": "Manus built-in."},

    {"name": "Jotform", "category": "Forms", "description": "Online form builder",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "JOTFORM_API_KEY", "endpoint": "https://api.jotform.com",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Social & Marketing
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Instagram", "category": "Social", "description": "Instagram publishing & insights",
     "auth_method": AUTH_OAUTH, "env_var": "INSTAGRAM_ACCESS_TOKEN", "endpoint": "https://graph.instagram.com",
     "manus_access": "builtin_oauth", "chatgpt_access": "oauth", "claude_access": "oauth",
     "1p_item": None, "notes": "Manus builtin OAuth. Token à stocker dans 1P après connexion."},

    {"name": "Meta Ads Manager", "category": "Marketing", "description": "Facebook/Instagram ads",
     "auth_method": AUTH_OAUTH, "env_var": "META_ACCESS_TOKEN", "endpoint": "https://graph.facebook.com",
     "manus_access": "builtin_oauth", "chatgpt_access": "oauth", "claude_access": "oauth",
     "1p_item": None, "notes": "Manus builtin OAuth. Token à stocker dans 1P après connexion."},

    {"name": "HARPA AI", "category": "Automation", "description": "Browser automation via HARPA Grid",
     "auth_method": AUTH_API_KEY, "env_var": "HARPA_API_KEY", "endpoint": "https://api.harpa.ai",
     "manus_access": "custom_api_editable", "chatgpt_access": "none", "claude_access": "none",
     "1p_item": "Harpa AI Grid — yOS-HARPA-2026-03", "notes": "Custom API editable existant."},

    # ═══════════════════════════════════════════════════════════════════════════
    # Misc / Utilities
    # ═══════════════════════════════════════════════════════════════════════════
    {"name": "Wolfram Alpha", "category": "Knowledge", "description": "Computational knowledge engine",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "WOLFRAM_ALPHA_APP_ID", "endpoint": "https://api.wolframalpha.com",
     "manus_access": "mcp_token", "chatgpt_access": "native", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. App ID à ajouter dans 1P."},

    {"name": "Google Maps", "category": "Maps", "description": "Maps, places, routes",
     "auth_method": AUTH_MCP_TOKEN, "env_var": "GOOGLE_MAPS_API_KEY", "endpoint": "https://maps.googleapis.com",
     "manus_access": "mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": None, "notes": "MCP managed. Clé à ajouter dans 1P."},

    {"name": "Tana", "category": "Knowledge", "description": "Structured note-taking & supertags",
     "auth_method": AUTH_API_KEY, "env_var": "TANA_API_KEY", "endpoint": "https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "TANA API", "notes": "Custom API connector créé batch 1."},

    {"name": "Hugging Face", "category": "AI/ML", "description": "Model hub & inference API",
     "auth_method": AUTH_API_KEY, "env_var": "HUGGING_FACE_API_KEY", "endpoint": "https://api-inference.huggingface.co",
     "manus_access": "custom_api + mcp_token", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "HuggingFace API Key", "notes": "Custom API + MCP Hugging Face."},

    {"name": "UPSTASH", "category": "Dev/DB", "description": "Serverless Redis & Kafka",
     "auth_method": AUTH_API_KEY, "env_var": "UPSTASH_API_KEY", "endpoint": "https://api.upstash.com",
     "manus_access": "custom_api_editable", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "UPSTASH", "notes": "Custom API editable existant."},

    {"name": "Manus API", "category": "Platform", "description": "Manus task & project management API",
     "auth_method": AUTH_API_KEY, "env_var": "MANUS_API_KEY", "endpoint": "https://api.manus.im",
     "manus_access": "custom_api", "chatgpt_access": "api_key", "claude_access": "api_key",
     "1p_item": "Manus API", "notes": "Custom API connector créé batch 1."},
]

# ─── Générer le JSON ──────────────────────────────────────────────────────────
with open('/tmp/yos_tool_registry.json', 'w') as f:
    json.dump(TOOL_REGISTRY, f, indent=2, ensure_ascii=False)

print(f"Tool Registry: {len(TOOL_REGISTRY)} tools")

# Stats
categories = {}
auth_methods = {}
missing_1p = []
for t in TOOL_REGISTRY:
    c = t['category']
    categories[c] = categories.get(c, 0) + 1
    a = t['auth_method']
    auth_methods[a] = auth_methods.get(a, 0) + 1
    if not t['1p_item']:
        missing_1p.append(t['name'])

print("\nBy category:")
for k, v in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\nBy auth method:")
for k, v in sorted(auth_methods.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print(f"\nMissing 1P entry ({len(missing_1p)}):")
for n in missing_1p:
    print(f"  - {n}")

print(f"\nSaved to /tmp/yos_tool_registry.json")
