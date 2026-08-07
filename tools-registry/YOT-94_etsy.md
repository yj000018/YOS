---
tool_id: YOT-94
tool_name: "Etsy"
tool_type: "MCP Connector"
category: "E-commerce Marketplace"
status: "Production"
pricing: "Free"
source_type: "Officiel"
source_url: "https://developers.etsy.com/"
auth_credentials: "OAuth MCP"
tags: ["ecommerce", "marketplace", "api-spec", "etsy"]
created_date: "2026-08-07"
---
# 🟢 YOT-94 — Etsy

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | E-commerce Marketplace |
| **Statut** | Production |
| **Pricing** | Free |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://developers.etsy.com/ |

## Business Value
Permet d'accéder rapidement aux spécifications de l'API Etsy Open API, facilitant l'intégration et le développement d'applications e-commerce liées à la marketplace Etsy. Accélère la recherche de paramètres d'endpoints et de schémas de données.

## Capabilities
- Recherche et consultation des spécifications de l'API Etsy Open API.
- Récupération des paramètres d'endpoints, des schémas de requêtes et de réponses.
- Consultation des exigences d'authentification et des scopes OAuth nécessaires.
- Accès aux informations sur les listings, boutiques, commandes, paiements, expéditions, avis et utilisateurs.

## Dependencies
- Connexion MCP active.
- Accès à la documentation Etsy Open API.

## Known Limits & Bugs
- Outil en lecture seule pour la documentation, ne permet pas d'exécuter directement des requêtes sur l'API Etsy.
- Dépend de la mise à jour des spécifications fournies par Etsy.

## Workarounds & Lessons
- Utiliser cet outil pour préparer les requêtes et comprendre les schémas avant d'implémenter les appels API réels via un client HTTP ou un autre connecteur.
