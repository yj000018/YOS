#!/usr/bin/env python3
"""
ART Health Monitor — Phase 1 : Classification des 39 outils par méthode de remédiation.

Méthodes :
  A = API_DIRECT     : L'outil expose une API de management pour créer des tokens programmatiquement
  B = PLAYWRIGHT_AUTO: Playwright peut naviguer et générer le token (login Google + clic)
  C = MANUAL_SIMPLE  : Page simple, 1 clic, token visible → URL directe + copier-coller
  D = MANUAL_COMPLEX : Nécessite création d'une app, validation 2FA, ou processus multi-étapes
"""

TOOLS = [
    # ─── FULLY AUTONOMOUS (API directe) ──────────────────────────────────────
    {
        "name": "Google Maps",
        "priority": "HIGH",
        "method": "A",
        "method_label": "API_DIRECT",
        "rationale": "Google Cloud API — créer une API key via gcloud CLI ou REST API avec le compte Google",
        "api_endpoint": "https://cloudresourcemanager.googleapis.com/v1/projects",
        "env_var": "GOOGLE_MAPS_API_KEY",
        "1p_item": "Google Maps API Key",
        "auto_script": "gcloud_create_maps_key",
    },
    {
        "name": "Tavily",
        "priority": "HIGH",
        "method": "A",
        "method_label": "API_DIRECT",
        "rationale": "Tavily a une API de management — créer un compte et récupérer la clé via API",
        "api_endpoint": "https://api.tavily.com/",
        "env_var": "TAVILY_API_KEY",
        "1p_item": "Tavily API Key",
        "auto_script": "tavily_signup_api",
    },
    {
        "name": "CoinGecko",
        "priority": "MEDIUM",
        "method": "A",
        "method_label": "API_DIRECT",
        "rationale": "CoinGecko API key gratuite — signup + récupération via API REST",
        "api_endpoint": "https://www.coingecko.com/en/developers/dashboard",
        "env_var": "COINGECKO_API_KEY",
        "1p_item": "CoinGecko API Key",
        "auto_script": "coingecko_signup_api",
    },
    {
        "name": "Alpha Vantage",
        "priority": "LOW",
        "method": "A",
        "method_label": "API_DIRECT",
        "rationale": "Alpha Vantage API key gratuite — simple formulaire email → clé envoyée",
        "api_endpoint": "https://www.alphavantage.co/support/#api-key",
        "env_var": "ALPHA_VANTAGE_API_KEY",
        "1p_item": "Alpha Vantage API Key",
        "auto_script": "alphavantage_signup",
    },

    # ─── PLAYWRIGHT AUTONOME (login Google + navigation) ─────────────────────
    {
        "name": "Linear",
        "priority": "HIGH",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → API → Generate key. Flux standard, pas de 2FA attendu.",
        "target_url": "https://linear.app/settings/api",
        "login_method": "google_oauth",
        "env_var": "LINEAR_API_KEY",
        "1p_item": "Linear API Key",
        "playwright_script": "linear_generate_key",
    },
    {
        "name": "ClickUp",
        "priority": "HIGH",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → Apps → API Token. Flux standard.",
        "target_url": "https://app.clickup.com/settings/apps",
        "login_method": "google_oauth",
        "env_var": "CLICKUP_API_TOKEN",
        "1p_item": "ClickUp API Token",
        "playwright_script": "clickup_get_token",
    },
    {
        "name": "Todoist",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → Integrations → Developer → API token visible.",
        "target_url": "https://todoist.com/app/settings/integrations/developer",
        "login_method": "google_oauth",
        "env_var": "TODOIST_API_TOKEN",
        "1p_item": "Todoist API Token",
        "playwright_script": "todoist_get_token",
    },
    {
        "name": "Calendly",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Integrations → API & Webhooks → Personal Access Token.",
        "target_url": "https://calendly.com/integrations/api_webhooks",
        "login_method": "google_oauth",
        "env_var": "CALENDLY_API_KEY",
        "1p_item": "Calendly API Key",
        "playwright_script": "calendly_get_token",
    },
    {
        "name": "Cal.com",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → Developer → API Keys → Add.",
        "target_url": "https://app.cal.com/settings/developer/api-keys",
        "login_method": "google_oauth",
        "env_var": "CALCOM_API_KEY",
        "1p_item": "Cal.com API Key",
        "playwright_script": "calcom_generate_key",
    },
    {
        "name": "Sentry",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → Account → API → Auth Tokens → Create.",
        "target_url": "https://sentry.io/settings/account/api/auth-tokens/",
        "login_method": "google_oauth",
        "env_var": "SENTRY_AUTH_TOKEN",
        "1p_item": "Sentry Auth Token",
        "playwright_script": "sentry_create_token",
    },
    {
        "name": "Fireflies.ai",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → API Key visible.",
        "target_url": "https://app.fireflies.ai/settings",
        "login_method": "google_oauth",
        "env_var": "FIREFLIES_API_KEY",
        "1p_item": "Fireflies API Key",
        "playwright_script": "fireflies_get_key",
    },
    {
        "name": "Fathom",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Settings → API → Generate key.",
        "target_url": "https://fathom.video/settings",
        "login_method": "google_oauth",
        "env_var": "FATHOM_API_KEY",
        "1p_item": "Fathom API Key",
        "playwright_script": "fathom_get_key",
    },
    {
        "name": "Cloudinary",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Console → API Keys visibles directement sur le dashboard.",
        "target_url": "https://cloudinary.com/console",
        "login_method": "google_oauth",
        "env_var": "CLOUDINARY_API_KEY",
        "1p_item": "Cloudinary API Key",
        "playwright_script": "cloudinary_get_keys",
    },
    {
        "name": "MailerLite",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Integrations → API → API key visible.",
        "target_url": "https://dashboard.mailerlite.com/integrations/api",
        "login_method": "google_oauth",
        "env_var": "MAILERLITE_API_KEY",
        "1p_item": "MailerLite API Key",
        "playwright_script": "mailerlite_get_key",
    },
    {
        "name": "monday.com",
        "priority": "MEDIUM",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Profile → Developers → API token visible.",
        "target_url": "https://monday.com/apps/manage/tokens",
        "login_method": "google_oauth",
        "env_var": "MONDAY_API_TOKEN",
        "1p_item": "monday.com API Token",
        "playwright_script": "monday_get_token",
    },
    {
        "name": "Jotform",
        "priority": "LOW",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Account → API → API key visible.",
        "target_url": "https://www.jotform.com/myaccount/api",
        "login_method": "google_oauth",
        "env_var": "JOTFORM_API_KEY",
        "1p_item": "Jotform API Key",
        "playwright_script": "jotform_get_key",
    },
    {
        "name": "Wix",
        "priority": "LOW",
        "method": "B",
        "method_label": "PLAYWRIGHT_AUTO",
        "rationale": "Login Google → Account → API Keys → Generate.",
        "target_url": "https://manage.wix.com/account/api-keys",
        "login_method": "google_oauth",
        "env_var": "WIX_API_KEY",
        "1p_item": "Wix API Key",
        "playwright_script": "wix_generate_key",
    },

    # ─── MANUEL SIMPLE (URL directe + 1 action) ──────────────────────────────
    {
        "name": "Canva",
        "priority": "HIGH",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Canva Developer Portal requiert une validation de compte développeur. 1 clic sur 'Get API Key'.",
        "manual_url": "https://www.canva.com/developers/",
        "manual_instruction": "Clique sur 'Get started' → génère une API key → copie-la",
        "env_var": "CANVA_API_KEY",
        "1p_item": "Canva API Key",
    },
    {
        "name": "Miro",
        "priority": "HIGH",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Miro nécessite de créer une App dans le Developer Portal pour obtenir un token OAuth.",
        "manual_url": "https://miro.com/app/settings/user-profile/apps",
        "manual_instruction": "Clique sur 'Create new app' → copie le 'Access token'",
        "env_var": "MIRO_ACCESS_TOKEN",
        "1p_item": "Miro Access Token",
    },
    {
        "name": "HubSpot",
        "priority": "HIGH",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "HubSpot Private App — nécessite de choisir les scopes manuellement.",
        "manual_url": "https://app.hubspot.com/settings/integrations/private-apps",
        "manual_instruction": "Clique sur 'Create a private app' → nomme-la 'yOS' → sélectionne tous les scopes → copie le token",
        "env_var": "HUBSPOT_API_TOKEN",
        "1p_item": "HubSpot Private App Token",
    },
    {
        "name": "Figma",
        "priority": "MEDIUM",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Figma PAT — page simple, 1 clic sur 'Generate new token'.",
        "manual_url": "https://www.figma.com/settings",
        "manual_instruction": "Scroll jusqu'à 'Personal access tokens' → clique 'Generate new token' → nomme-le 'yOS' → copie-le",
        "env_var": "FIGMA_PAT",
        "1p_item": "Figma PAT",
    },
    {
        "name": "Ahrefs",
        "priority": "HIGH",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Ahrefs API key — requiert un abonnement actif. Page simple.",
        "manual_url": "https://app.ahrefs.com/account/api",
        "manual_instruction": "Copie l'API key affichée (si abonnement actif)",
        "env_var": "AHREFS_API_KEY",
        "1p_item": "Ahrefs API Key",
    },
    {
        "name": "Heptabase",
        "priority": "HIGH",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Heptabase — login email (pas Google), page settings simple.",
        "manual_url": "https://app.heptabase.com/settings",
        "manual_instruction": "Va dans Settings → API → génère ou copie la clé API",
        "env_var": "HEPTABASE_API_KEY",
        "1p_item": "Heptabase API Key",
    },
    {
        "name": "Granola",
        "priority": "MEDIUM",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Granola — login Google, page settings simple.",
        "manual_url": "https://app.granola.ai/settings",
        "manual_instruction": "Va dans Settings → API → copie la clé API",
        "env_var": "GRANOLA_API_KEY",
        "1p_item": "Granola API Key",
    },
    {
        "name": "Webflow",
        "priority": "MEDIUM",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Webflow API token — page settings simple.",
        "manual_url": "https://webflow.com/dashboard/account/integrations",
        "manual_instruction": "Va dans Account → Integrations → API Access → génère un token",
        "env_var": "WEBFLOW_API_TOKEN",
        "1p_item": "Webflow API Token",
    },
    {
        "name": "Sanity",
        "priority": "LOW",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Sanity API token — page Manage simple.",
        "manual_url": "https://www.sanity.io/manage",
        "manual_instruction": "Sélectionne ton projet → API → Tokens → Add API token → nomme-le 'yOS' → copie-le",
        "env_var": "SANITY_API_TOKEN",
        "1p_item": "Sanity API Token",
    },
    {
        "name": "Wrike",
        "priority": "LOW",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Wrike permanent access token — page apps simple.",
        "manual_url": "https://www.wrike.com/frontend/apps/index.html#api",
        "manual_instruction": "Va dans Apps & Integrations → API → génère un permanent access token",
        "env_var": "WRIKE_ACCESS_TOKEN",
        "1p_item": "Wrike Access Token",
    },
    {
        "name": "Klaviyo",
        "priority": "MEDIUM",
        "method": "C",
        "method_label": "MANUAL_SIMPLE",
        "rationale": "Klaviyo — login email uniquement (pas Google). Page simple.",
        "manual_url": "https://www.klaviyo.com/account#api-keys-tab",
        "manual_instruction": "Va dans Account → API Keys → Create Private API Key → nomme-le 'yOS' → copie-le",
        "env_var": "KLAVIYO_API_KEY",
        "1p_item": "Klaviyo Private API Key",
    },

    # ─── MANUEL COMPLEXE (création app, 2FA, multi-étapes) ───────────────────
    {
        "name": "Slack",
        "priority": "HIGH",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Slack nécessite de créer une App avec des scopes OAuth spécifiques. Multi-étapes.",
        "manual_url": "https://api.slack.com/apps?new_app=1",
        "manual_instruction": "1. Clique 'Create New App' → 'From scratch' → nomme 'yOS' → sélectionne ton workspace\n2. Va dans 'OAuth & Permissions' → ajoute les scopes : channels:read, chat:write, files:write, users:read\n3. Clique 'Install to Workspace' → autorise\n4. Copie le 'Bot User OAuth Token' (xoxb-...)",
        "env_var": "SLACK_BOT_TOKEN",
        "1p_item": "Slack Bot Token — yOS",
    },
    {
        "name": "Make (Integromat)",
        "priority": "HIGH",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Make API token — dans le profil, mais nécessite une vérification de compte.",
        "manual_url": "https://www.make.com/en/api-documentation",
        "manual_instruction": "1. Va sur make.com → ton profil (avatar en haut à droite)\n2. API → Generate new token → nomme-le 'yOS'\n3. Copie le token",
        "env_var": "MAKE_API_TOKEN",
        "1p_item": "Make API Token",
    },
    {
        "name": "Zoom",
        "priority": "MEDIUM",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Zoom Server-to-Server OAuth — nécessite de créer une App sur le Marketplace avec Account ID + Client ID + Secret.",
        "manual_url": "https://marketplace.zoom.us/develop/create",
        "manual_instruction": "1. Clique 'Server-to-Server OAuth' → nomme 'yOS'\n2. Active les scopes : meeting:read, recording:read\n3. Copie Account ID + Client ID + Client Secret",
        "env_var": "ZOOM_ACCOUNT_ID",
        "1p_item": "Zoom API — Server-to-Server",
    },
    {
        "name": "Higgsfield",
        "priority": "HIGH",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Higgsfield — plateforme récente, accès API potentiellement en beta/waitlist.",
        "manual_url": "https://higgsfield.ai/dashboard",
        "manual_instruction": "Va dans Dashboard → Settings → API → génère ou copie la clé API",
        "env_var": "HIGGSFIELD_API_KEY",
        "1p_item": "Higgsfield API Key",
    },
    {
        "name": "Magnific",
        "priority": "HIGH",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Magnific — accès API via MCP uniquement pour l'instant, pas d'API publique standard.",
        "manual_url": "https://magnific.ai/dashboard",
        "manual_instruction": "Va dans Dashboard → Settings → API → génère ou copie la clé API (si disponible)",
        "env_var": "MAGNIFIC_API_KEY",
        "1p_item": "Magnific API Key",
    },
    {
        "name": "MiniMax",
        "priority": "HIGH",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "MiniMax — plateforme chinoise, login via email/WeChat, interface en chinois.",
        "manual_url": "https://platform.minimaxi.com/user-center/basic-information/interface-key",
        "manual_instruction": "Connecte-toi → User Center → Interface Key → copie la clé API",
        "env_var": "MINIMAX_API_KEY",
        "1p_item": "MiniMax API Key",
    },
    {
        "name": "Twilio",
        "priority": "MEDIUM",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Twilio — login email (pas Google), 2FA probable, Account SID + Auth Token.",
        "manual_url": "https://console.twilio.com",
        "manual_instruction": "Connecte-toi → Dashboard → copie Account SID + Auth Token affichés directement",
        "env_var": "TWILIO_ACCOUNT_SID",
        "1p_item": "Twilio Account SID + Auth Token",
    },
    {
        "name": "Bright Data",
        "priority": "MEDIUM",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Bright Data — login email, interface complexe, API token dans les settings.",
        "manual_url": "https://brightdata.com/cp/setting",
        "manual_instruction": "Connecte-toi → Settings → API Token → copie le token",
        "env_var": "BRIGHT_DATA_API_TOKEN",
        "1p_item": "Bright Data API Token",
    },
    {
        "name": "Dropbox",
        "priority": "MEDIUM",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Dropbox OAuth — nécessite de créer une App sur le Developer Portal pour obtenir un long-lived token.",
        "manual_url": "https://www.dropbox.com/developers/apps/create",
        "manual_instruction": "1. Crée une app 'Scoped access' → 'Full Dropbox'\n2. Nomme-la 'yOS'\n3. Dans Settings → OAuth 2 → Generated access token → Generate\n4. Copie le token",
        "env_var": "DROPBOX_ACCESS_TOKEN",
        "1p_item": "Dropbox Access Token — yOS",
    },
    {
        "name": "Wolfram Alpha",
        "priority": "LOW",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Wolfram — Wolfram ID propre (pas Google), création d'une App.",
        "manual_url": "https://developer.wolframalpha.com/portal/myapps/",
        "manual_instruction": "Connecte-toi avec ton Wolfram ID → 'Get an AppID' → nomme 'yOS' → copie l'AppID",
        "env_var": "WOLFRAM_APP_ID",
        "1p_item": "Wolfram Alpha App ID",
    },
    {
        "name": "Instagram",
        "priority": "LOW",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Manus gère déjà via OAuth builtin. Stocker le long-lived token après connexion.",
        "manual_url": "https://developers.facebook.com/tools/explorer/",
        "manual_instruction": "Manus gère déjà l'accès. Aucune action requise pour l'instant.",
        "env_var": "INSTAGRAM_ACCESS_TOKEN",
        "1p_item": "Instagram Long-lived Token",
    },
    {
        "name": "Meta Ads Manager",
        "priority": "LOW",
        "method": "D",
        "method_label": "MANUAL_COMPLEX",
        "rationale": "Manus gère déjà via OAuth builtin. Stocker le long-lived token après connexion.",
        "manual_url": "https://developers.facebook.com/tools/explorer/",
        "manual_instruction": "Manus gère déjà l'accès. Aucune action requise pour l'instant.",
        "env_var": "META_ADS_ACCESS_TOKEN",
        "1p_item": "Meta Ads Access Token",
    },
]

# ─── Rapport de classification ─────────────────────────────────────────────────
import json

by_method = {"A": [], "B": [], "C": [], "D": []}
for t in TOOLS:
    by_method[t["method"]].append(t)

print("=" * 80)
print("ART HEALTH MONITOR — CLASSIFICATION DES 39 OUTILS")
print("=" * 80)
print(f"\n  A) API_DIRECT (autonome total)  : {len(by_method['A'])} outils")
print(f"  B) PLAYWRIGHT_AUTO (autonome)   : {len(by_method['B'])} outils")
print(f"  C) MANUAL_SIMPLE (URL + 1 clic) : {len(by_method['C'])} outils")
print(f"  D) MANUAL_COMPLEX (multi-étapes): {len(by_method['D'])} outils")
print(f"\n  → Autonomie totale : {len(by_method['A']) + len(by_method['B'])} outils")
print(f"  → Action manuelle  : {len(by_method['C']) + len(by_method['D'])} outils")

print("\n\n🤖 A) API_DIRECT — Exécution autonome immédiate")
print("-" * 60)
for t in by_method["A"]:
    print(f"  [{t['priority']}] {t['name']} → {t['env_var']}")
    print(f"         {t['rationale']}")

print("\n\n🤖 B) PLAYWRIGHT_AUTO — Exécution autonome via browser")
print("-" * 60)
for t in by_method["B"]:
    print(f"  [{t['priority']}] {t['name']} → {t['env_var']}")
    print(f"         URL: {t['target_url']}")

print("\n\n👤 C) MANUAL_SIMPLE — Action manuelle rapide (1-2 min par outil)")
print("-" * 60)
for t in by_method["C"]:
    print(f"  [{t['priority']}] {t['name']}")
    print(f"         URL: {t['manual_url']}")
    print(f"         Action: {t['manual_instruction']}")
    print()

print("\n\n👤 D) MANUAL_COMPLEX — Action manuelle avec étapes multiples")
print("-" * 60)
for t in by_method["D"]:
    print(f"  [{t['priority']}] {t['name']}")
    print(f"         URL: {t['manual_url']}")
    print(f"         Action: {t['manual_instruction'][:100]}...")
    print()

# Sauvegarder
with open('/tmp/art_classification.json', 'w') as f:
    json.dump(TOOLS, f, indent=2, ensure_ascii=False)
print(f"\nSaved to /tmp/art_classification.json")
