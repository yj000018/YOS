# Plan d'action — 39 outils sans entrée 1Password

## Réponse à ta question

**Non, le mot de passe Google ne suffit pas pour aucun de ces 39 outils.**

La distinction est importante :
- **Connexion UI** (se connecter au site web) → Google OAuth suffit pour la plupart
- **Accès API/MCP** (accès programmatique depuis Manus, ChatGPT, etc.) → **toujours une clé API ou un token séparé**, même si tu t'es connecté via Google

Le pattern est systématique : tu te connectes au dashboard via Google → tu vas dans Settings → API → tu génères une clé → tu la stockes dans 1Password.

## Résumé

| Type | Nombre | Explication |
|------|--------|-------------|
| **Google + API key** | 28 | Connexion initiale via Google, mais API key séparée à créer dans les settings |
| **OAuth propre + API key** | 9 | Pas de Google OAuth, compte propre + API key/token à créer |
| **Meta OAuth (Manus gère)** | 2 | Instagram + Meta Ads — Manus gère déjà, juste stocker le token dans 1P |

---

## 🔴 PRIORITÉ HIGH (13 outils — à faire maintenant)

| Outil | URL pour créer la clé | Item 1Password |
|-------|----------------------|----------------|
| **Canva** | [canva.com/developers](https://www.canva.com/developers/) | `Canva API Key` |
| **Miro** | [miro.com/app/settings/user-profile/apps](https://miro.com/app/settings/user-profile/apps) | `Miro Access Token` |
| **Slack** | [api.slack.com/apps](https://api.slack.com/apps) → Bot Token | `Slack Bot Token — yOS` |
| **Linear** | [linear.app/settings/api](https://linear.app/settings/api) | `Linear API Key` |
| **ClickUp** | [app.clickup.com/settings/apps](https://app.clickup.com/settings/apps) | `ClickUp API Token` |
| **HubSpot** | [app.hubspot.com → Private Apps](https://app.hubspot.com/settings/integrations/private-apps) | `HubSpot Private App Token` |
| **Make** | [make.com → Profile → API token](https://www.make.com/en/api-documentation) | `Make API Token` |
| **Heptabase** | [app.heptabase.com/settings](https://app.heptabase.com/settings) | `Heptabase API Key` |
| **Ahrefs** | [app.ahrefs.com/account/api](https://app.ahrefs.com/account/api) | `Ahrefs API Key` |
| **Tavily** | [app.tavily.com/home](https://app.tavily.com/home) | `Tavily API Key` |
| **Google Maps** | [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) | `Google Maps API Key` |
| **Higgsfield** | [higgsfield.ai/dashboard](https://higgsfield.ai/dashboard) | `Higgsfield API Key` |
| **Magnific** | [magnific.ai/dashboard](https://magnific.ai/dashboard) | `Magnific API Key` |
| **MiniMax** | [platform.minimaxi.com/user-center](https://platform.minimaxi.com/user-center/basic-information/interface-key) | `MiniMax API Key` |

---

## 🟡 PRIORITÉ MEDIUM (18 outils)

| Outil | URL pour créer la clé | Item 1Password |
|-------|----------------------|----------------|
| **Figma** | [figma.com/settings → Personal access tokens](https://www.figma.com/settings) | `Figma PAT` |
| **Zoom** | [marketplace.zoom.us → Server-to-Server OAuth](https://marketplace.zoom.us/develop/create) | `Zoom API — Server-to-Server` |
| **Calendly** | [calendly.com/integrations/api_webhooks](https://calendly.com/integrations/api_webhooks) | `Calendly API Key` |
| **Cal.com** | [app.cal.com/settings/developer/api-keys](https://app.cal.com/settings/developer/api-keys) | `Cal.com API Key` |
| **monday.com** | [monday.com/apps/manage/tokens](https://monday.com/apps/manage/tokens) | `monday.com API Token` |
| **Klaviyo** | [klaviyo.com/account#api-keys-tab](https://www.klaviyo.com/account#api-keys-tab) | `Klaviyo Private API Key` |
| **Sentry** | [sentry.io/settings/account/api/auth-tokens](https://sentry.io/settings/account/api/auth-tokens/) | `Sentry Auth Token` |
| **Todoist** | [todoist.com/app/settings/integrations/developer](https://todoist.com/app/settings/integrations/developer) | `Todoist API Token` |
| **Webflow** | [webflow.com/dashboard/account/integrations](https://webflow.com/dashboard/account/integrations) | `Webflow API Token` |
| **Fireflies.ai** | [app.fireflies.ai/settings → API](https://app.fireflies.ai/settings) | `Fireflies API Key` |
| **Fathom** | [fathom.video/settings → API](https://fathom.video/settings) | `Fathom API Key` |
| **Granola** | [app.granola.ai/settings → API](https://app.granola.ai/settings) | `Granola API Key` |
| **Cloudinary** | [cloudinary.com/console → API Keys](https://cloudinary.com/console) | `Cloudinary API Key` |
| **MailerLite** | [dashboard.mailerlite.com/integrations/api](https://dashboard.mailerlite.com/integrations/api) | `MailerLite API Key` |
| **Twilio** | [console.twilio.com → API Keys](https://console.twilio.com/us1/account/keys-credentials/api-keys) | `Twilio Account SID + Auth Token` |
| **Bright Data** | [brightdata.com/cp/setting → API Token](https://brightdata.com/cp/setting) | `Bright Data API Token` |
| **CoinGecko** | [coingecko.com/en/developers/dashboard](https://www.coingecko.com/en/developers/dashboard) | `CoinGecko API Key` |
| **Dropbox** | [dropbox.com/developers/apps](https://www.dropbox.com/developers/apps) | `Dropbox Access Token — yOS` |

---

## 🟢 PRIORITÉ LOW (8 outils)

| Outil | URL pour créer la clé | Item 1Password |
|-------|----------------------|----------------|
| **Wrike** | [wrike.com/frontend/apps](https://www.wrike.com/frontend/apps/index.html#api) | `Wrike Access Token` |
| **Wix** | [manage.wix.com/account/api-keys](https://manage.wix.com/account/api-keys) | `Wix API Key` |
| **Sanity** | [sanity.io/manage → API → Tokens](https://www.sanity.io/manage) | `Sanity API Token` |
| **Jotform** | [jotform.com/myaccount/api](https://www.jotform.com/myaccount/api) | `Jotform API Key` |
| **Alpha Vantage** | [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key) | `Alpha Vantage API Key` |
| **Wolfram Alpha** | [developer.wolframalpha.com/portal/myapps](https://developer.wolframalpha.com/portal/myapps/) | `Wolfram Alpha App ID` |
| **Instagram** | Manus gère déjà via OAuth — stocker le token après connexion | `Instagram Long-lived Token` |
| **Meta Ads Manager** | Manus gère déjà via OAuth — stocker le token après connexion | `Meta Ads Access Token` |

---

## Workflow recommandé

Pour chaque outil :
1. Va sur l'URL indiquée
2. Connecte-toi (via Google si disponible)
3. Génère/copie la clé API ou le token
4. Crée un item dans 1Password → catégorie **API Credential**
5. Nomme-le exactement comme indiqué dans la colonne "Item 1Password"
6. Le script `sync_1p_to_manus.py` le poussera automatiquement dans Manus

> **Note Slack :** Slack est le seul outil qui nécessite de créer une "App" (bot) avant d'avoir un token. C'est 5 min sur api.slack.com/apps.
