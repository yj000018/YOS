# 🔗 Intégration MCP (Model Context Protocol)

Le MCP est le protocole qui permet à Manus de se connecter nativement à tes outils. Voici comment l'intégrer dans ta chaîne.

## 🛠️ Étapes d'Intégration

1.  **Configuration du Serveur MCP** : Manus utilise un fichier `mcp_config.json` pour connaître les serveurs disponibles (Notion, Slack, Gmail, etc.).
2.  **Authentification** : Les tokens (API Keys) sont stockés de manière sécurisée.
3.  **Appel des Outils** : Manus utilise la commande `manus-mcp-cli` pour interagir avec les outils.

## 🚀 Commande Unique d'Activation

Copie-colle cette commande pour configurer et activer l'intégration MCP complète :

```bash
curl -sSL https://raw.githubusercontent.com/yj000018/relevance-ai-workforce/master/setup_mcp.sh | bash
```

## 📊 Flux de Données avec MCP

```
ChatGPT (Intention)
    ↓
Manus (Réflexion)
    ↓
MCP (Action Directe sur Notion/Slack/Gmail)
    ↓
Git (Sauvegarde de la config)
    ↓
CI/CD (Déploiement Relevance AI)
```

## ✅ Avantages

- **Accès Natif** : Plus besoin de scripts personnalisés pour chaque outil.
- **Sécurité** : Authentification centralisée et sécurisée.
- **Vitesse** : Interaction quasi-instantanée avec tes applications.
