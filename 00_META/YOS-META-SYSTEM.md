# Y-OS Meta-System — Architecture d'Auto-Évolution

## Philosophie
Y-OS n'est pas un système statique. C'est un organisme cognitif conçu pour s'améliorer à chaque exécution. Le **Meta-System** est la couche supérieure (au-dessus du Kernel) qui garantit que Y-OS apprend, se documente, et se maintient de manière autonome.

L'objectif est d'atteindre une **friction cognitive zéro** pour l'utilisateur concernant la maintenance du système.

---

## Les 5 Protocoles d'Auto-Évolution

Le Meta-System repose sur 5 protocoles interconnectés :

### 1. Protocole d'Auto-Enrichissement (AEP)
**But** : Capturer les découvertes et les transformer en règles réutilisables.
- **Trigger** : Résolution d'un bug complexe, découverte d'une nouvelle API, ou contournement d'une limitation (ex: bypass Cloudflare via CDP).
- **Action** : 
  1. Extraire la "Lesson Learned".
  2. Mettre à jour `AGENTS.md` (si impact infra) ou créer une Tool Fact Sheet.
  3. Mettre à jour l'ERT (Execution Routing Table) si cela concerne le routage.

### 2. Protocole d'Auto-Documentation (ADP)
**But** : Maintenir la carte du territoire toujours à jour sans intervention humaine.
- **Trigger** : Création d'un nouveau script, module, ou intégration.
- **Action** :
  1. Générer/Mettre à jour le diagramme d'architecture (Excalidraw/Mermaid).
  2. Rédiger le `SKILL.md` selon le *Y-OS Module Standard*.
  3. Mettre à jour le Tools Registry (`02_AGENTS/`).

### 3. Protocole d'Auto-Maintenance (AMP)
**But** : Prévenir la dette technique et nettoyer les scories.
- **Trigger** : Exécution programmée (cron) ou fin de session complexe.
- **Action** :
  1. Purger les locks zombies (`/tmp/yos_locks/`).
  2. Archiver les sessions orphelines (via `delta_manus.py`).
  3. Vérifier l'expiration imminente des tokens (ex: GitHub PAT).

### 4. Protocole d'Auto-Routage (ARP)
**But** : Optimiser le chemin d'exécution en temps réel.
- **Trigger** : Requête d'exécution web ou système.
- **Action** :
  1. Consulter l'ERT (`ERT.md`).
  2. Choisir le nœud optimal (API > CDP > Playwright).
  3. Appliquer les locks nécessaires (ex: `MacLock`).

### 5. Protocole de Notification Unifiée (UNP)
**But** : Informer l'utilisateur uniquement quand c'est nécessaire, via le bon canal.
- **Trigger** : Besoin d'attention ou fin de processus long.
- **Action** :
  1. Router via le module `yos-notif`.
  2. Afficher sur xbar (si Mac) ET envoyer push Telegram.

---

## Intégration dans le Kernel (yos-bootstrap)

Ces protocoles ne sont pas de simples documents ; ils sont câblés comme des **AUTO-TRIGGERS** dans le Kernel Y-OS :

1. **AEP (Enrichissement)** : Trigger `Nouvelle capacité documentée` → Mettre à jour Tools Registry + Lessons Learned.
2. **ADP (Documentation)** : Trigger `Nouveau module créé` → Appliquer Y-OS Module Standard.
3. **ARP (Routage)** : Trigger `Accès web requis` → Appliquer ERT.

## Cycle de Vie d'une Amélioration Y-OS

1. **Friction** : L'agent rencontre un obstacle (ex: cookies chiffrés Brave).
2. **Résolution** : L'agent trouve un contournement (ex: CDP via Terminal GUI).
3. **AEP** : L'agent extrait la leçon et met à jour `AGENTS.md` (Règle Canon).
4. **ADP** : L'agent documente le script d'extraction dans une Tool Fact Sheet.
5. **Session suivante** : L'agent lit `AGENTS.md` (Bootstrap), applique la nouvelle règle, et contourne l'obstacle en 0 seconde.
