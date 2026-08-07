---
tool_id: YOT-80
tool_name: "GoDaddy"
tool_type: "MCP Connector"
category: "Domain Management"
status: "Production"
pricing: "Paid"
source_type: "Officiel"
source_url: "https://developer.godaddy.com/"
auth_credentials: "API Key"
tags: ["domain", "godaddy", "dns", "search"]
created_date: "2026-08-07"
---
# 🟢 YOT-80 — GoDaddy
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Domain Management |
| **Statut** | Production |
| **Pricing** | Paid |
| **Source** | Officiel |
| **Auth** | API Key |
| **URL** | https://developer.godaddy.com/ |
## Business Value
Permet à Y-OS de rechercher, vérifier la disponibilité et gérer les noms de domaine directement depuis l'interface, facilitant le déploiement rapide de nouveaux projets web.
## Capabilities
- Recherche de noms de domaine
- Vérification de la disponibilité des domaines
- Consultation des suggestions de domaines alternatifs
## Dependencies
- Clé API GoDaddy (API Key & Secret)
- Compte développeur GoDaddy actif
## Known Limits & Bugs
- Les limites de taux (rate limits) de l'API GoDaddy peuvent restreindre les requêtes massives.
- Certains TLDs spécifiques peuvent ne pas être supportés par l'API de recherche standard.
## Workarounds & Lessons
- Implémenter un délai entre les requêtes pour éviter de déclencher les limites de taux de l'API.
- Toujours vérifier les prix de renouvellement en plus du prix d'achat initial.
