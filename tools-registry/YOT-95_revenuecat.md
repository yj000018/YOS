---
tool_id: YOT-95
tool_name: "RevenueCat"
tool_type: "MCP Connector"
category: "Subscription Management"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://www.revenuecat.com/docs/"
auth_credentials: "OAuth MCP"
tags: ["subscription", "monetization", "in-app-purchases", "revenuecat"]
created_date: "2026-08-07"
---
# 🟢 YOT-95 — RevenueCat
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Subscription Management |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://www.revenuecat.com/docs/

## Business Value
RevenueCat centralise et simplifie la gestion des abonnements in-app et des achats intégrés sur toutes les plateformes. Il permet à Y-OS d'automatiser la configuration des paywalls, des offres et des droits d'accès sans nécessiter de code backend complexe.

## Capabilities
- Gérer les applications et les projets d'abonnement.
- Configurer et mettre à jour les produits, les entitlements (droits) et les offres.
- Organiser les packages et les paywalls.
- Récupérer les métadonnées des projets et les détails des applications.

## Dependencies
- Compte RevenueCat actif.
- Authentification OAuth via le connecteur MCP.

## Known Limits & Bugs
- Les modifications de configuration peuvent prendre quelques minutes pour se propager sur tous les appareils.
- Nécessite une compréhension précise de la hiérarchie de RevenueCat (Projets > Apps > Produits > Entitlements).

## Workarounds & Lessons
- Toujours vérifier les relations entre les produits et les entitlements avant de publier une nouvelle offre.
- Utiliser les environnements de test (sandbox) pour valider les configurations de paywall avant le déploiement en production.
