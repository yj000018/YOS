# Y-OS Tool Registry & Architecture Multi-Plateforme

## 1. Inventaire Exhaustif et Analyse OAuth

Nous avons réalisé un scan complet de tous les connecteurs configurés dans Manus. Le résultat montre qu'il existe **87 outils configurés** au total.

L'analyse de la méthode d'authentification révèle une distinction importante :
- **49 outils** utilisent une clé API classique (Custom API Connector ou Built-in)
- **34 outils** sont des MCP "Managed" par Manus. Pour ces outils, l'authentification **n'est pas du vrai OAuth côté utilisateur**. Manus injecte directement un token (souvent une clé API) dans les headers ou l'URL du serveur MCP en arrière-plan.
- **4 outils** utilisent du vrai OAuth géré nativement par Manus (Gmail, Google Calendar, Instagram, Shopify, etc.).

**Conclusion sur les outils manquants :**
Les outils que tu pensais manquants (Slack, Cal.com, Calendly, Linear, Miro, HubSpot, etc.) sont en réalité des **MCP Managed**. Ils sont bien présents et actifs dans Manus, mais leurs clés API ou tokens ne sont pas encore stockés dans 1Password.

## 2. Le Modèle Multi-Plateforme (1Password SSOT)

Pour garantir la cohérence entre Manus, ChatGPT, Claude et les autres systèmes, l'architecture suivante est mise en place :

1. **Single Source of Truth (SSOT) :** 1Password est l'unique source de vérité. TOUT secret, qu'il soit pour une API, un MCP, ou un token OAuth de longue durée, doit y être stocké.
2. **Miroir Local :** Chaque plateforme (Manus, ChatGPT) possède son propre miroir des secrets nécessaires à son fonctionnement.
3. **Tool Fact Sheets :** Chaque outil possède une fiche descriptive (Fact Sheet) documentant précisément comment y accéder depuis chaque plateforme.

## 3. Tool Fact Sheets

J'ai généré **87 Tool Fact Sheets** individuelles pour chaque outil identifié dans Y-OS.
Chaque fiche contient :
- La catégorie et la description
- La méthode d'authentification (`api_key`, `mcp_token`, `oauth`)
- L'endpoint de l'API
- La variable d'environnement associée
- L'item correspondant dans 1Password
- La méthode d'accès spécifique par plateforme (Manus, ChatGPT, Claude)

**Action requise :**
Sur les 87 outils, **39 n'ont pas encore d'entrée dans 1Password** (principalement les MCP Managed). Il faudra créer ces items dans 1Password pour que le miroir puisse les synchroniser à l'avenir.

Les 87 fiches ont été générées dans le dossier `tool_fact_sheets` et seront poussées sur GitHub.
