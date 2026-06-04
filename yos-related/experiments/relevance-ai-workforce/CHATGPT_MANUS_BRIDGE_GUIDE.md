# 🤖 Comment utiliser le Pont ChatGPT ↔️ Manus

Une fois que tu as lancé le script `setup_mcp.sh`, voici comment activer la communication.

## 1. Activation dans ChatGPT

Si tu utilises l'application **ChatGPT Desktop** (Mac ou Windows) :
1.  Ouvre les **Paramètres** de ChatGPT.
2.  Va dans la section **MCP**.
3.  Clique sur **"Add Server"**.
4.  Choisis le fichier de configuration : `~/.mcp/config.json`.

ChatGPT va maintenant voir l'outil `manus-bridge`.

## 2. Comment commander Manus depuis ChatGPT

Tu n'as pas besoin de syntaxe spéciale comme "manus:". Parle simplement à ChatGPT naturellement :

> **Toi :** "Utilise Manus pour créer un nouveau repo GitHub nommé 'test-mcp' et ajoute un fichier README."

### Ce qui se passe en coulisses :
1.  ChatGPT voit qu'il a un outil nommé `manus-bridge`.
2.  Il envoie ta demande au serveur `manus-bridge`.
3.  Le pont transmet l'ordre à Manus.
4.  Manus exécute la tâche et renvoie le résultat à ChatGPT.

## 💡 Exemples de commandes

- *"Demande à Manus d'analyser mes derniers emails via Gmail et d'en faire un résumé dans Notion."*
- *"Utilise Manus pour mettre à jour la configuration de mon workforce sur Relevance AI."*
- *"Demande à Manus de chercher les dernières news sur l'IA et de les poster sur Slack."*

## 🔐 Note sur la Sécurité
Le pont utilise ta `MANUS_API_KEY`. Assure-toi qu'elle est bien configurée dans le fichier `~/.mcp/config.json` pour que la connexion soit autorisée.
