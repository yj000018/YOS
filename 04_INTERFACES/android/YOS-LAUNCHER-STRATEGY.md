# Stratégie Launcher Y-OS (Android)

L'interface front-end (launcher) d'un appareil Android Y-OS doit répondre à des critères stricts : puissance, versatilité, contrôle par IA (ADB), et organisation (dossiers/catégories).

## 1. Le problème avec One UI (Launcher natif Samsung)

- **Contrôle ADB** : Très limité. Impossible de créer des dossiers, de déplacer des icônes ou de restaurer un layout proprement via script.
- **Organisation** : Manuelle uniquement. Les nouvelles apps s'empilent à la fin.
- **Verdict** : Bien pour le grand public, insuffisant pour une gestion de flotte "AI-driven" où l'on veut imposer un blueprint.

## 2. Les Alternatives Pro

### Option A : Nova Launcher Prime ⭐ (Recommandé)
- **Puissance** : Le standard absolu depuis 10 ans.
- **Dossiers/Catégories** : Tiroir d'applications organisé par onglets et dossiers (ex: IA, Création, Médias, Outils).
- **Contrôle ADB** : **Excellent**. Nova permet d'exporter sa configuration complète (layout, dossiers, paramètres) dans un fichier `.novabackup`. Ce fichier peut être poussé via ADB et restauré silencieusement.
- **Versatilité** : Gestes (swipe up, double tap) assignables à des actions (ex: lancer un script Tasker/MacroDroid qui parle à Y-OS).

### Option B : Niagara Launcher
- **Concept** : Minimaliste, liste verticale, pas d'icônes en grille.
- **Avantage** : Zéro distraction, extrêmement rapide.
- **Inconvénient** : Pas de dossiers traditionnels (remplacés par des "pop-ups").
- **Contrôle ADB** : Backup/Restore possible mais moins robuste que Nova.

### Option C : Kvaesitso / Olauncher (Open Source)
- **Concept** : Orienté recherche (search-first). On tape pour trouver.
- **Inconvénient** : Trop disruptif pour une tablette de création.

## 3. Implémentation de la stratégie Nova Launcher

Pour avoir une interface "top niveau" contrôlable par l'IA :

1. **Setup manuel initial (1x)** :
   - Installer Nova Launcher Prime sur la Tab S11.
   - Créer l'interface parfaite (dossiers "Y-OS AI", "Création", "Outils", cacher les apps inutiles).
   - Exporter le backup (`yos_blueprint_v1.novabackup`).

2. **Automatisation Y-OS (Pipeline P4)** :
   - Le fichier `.novabackup` est stocké sur le Cloud Computer.
   - Lors du provisioning d'un nouvel appareil (ex: Fold 7), le script `yos-android-provision.sh` :
     1. Installe Nova Launcher via ADB.
     2. Pousse le fichier de backup.
     3. Force la restauration via un intent ADB.
   - Résultat : Le Fold 7 a instantanément les mêmes dossiers, la même disposition et les mêmes apps cachées que la Tab S11.

## 4. Dossiers recommandés (Blueprint Y-OS)

- **🧠 Y-OS Core** : Claude, ChatGPT, Perplexity, Grok, Notion, Obsidian.
- **🛠️ Ops & Infra** : Tailscale, Home Assistant, Termux, Telegram.
- **🎨 Création** : Concepts, LumaFusion, Snapseed, Clip Studio.
- **📺 Médias** : YouTube, Spotify, Netflix.
- **Apps cachées (Tiroir)** : Toutes les apps système (Paramètres, Fichiers, Calculatrice, etc.) pour garder l'interface propre.

## Conclusion

Pour atteindre l'objectif d'une interface "puissance, versatilité, contrôle par AI", **Nova Launcher** est la seule solution viable. Il permet de figer un "Blueprint UI" et de le déployer à l'échelle via ADB.
