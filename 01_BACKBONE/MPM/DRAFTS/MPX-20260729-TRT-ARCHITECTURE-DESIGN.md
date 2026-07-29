# MPX-20260729-TRT-ARCHITECTURE-DESIGN
> **Type** : MPX (ChatGPT Architecture Task)
> **Mode** : sprint
> **Status** : ready_for_execution
> **Created** : 2026-07-29
> **Created by** : Manus (Y-OS session)

---

## Context Injection

Tu es l'architecte cognitif de Y-OS (Yannick Operating System), un système d'exploitation cognitif multi-LLM. Voici l'architecture existante que tu dois respecter et enrichir — ne réinvente rien, étends seulement.

### Modules existants (ne pas modifier leur définition)

**ART — Agent Routing Table** (`01_BACKBONE/AGENTS/04_ROUTING/ART/`)
- Lookup table pour router les tâches vers les **agents** selon leurs capacités, niveau de confiance (T0-T5) et disponibilité.
- Schema : `task_type → required_capabilities + required_trust_level → preferred_agent + fallback_agents + routing_policy`
- Submodule de `AGENTS/04_ROUTING`. Pas standalone.
- Utilisé par YARP pour encoder `target_agent` dans les messages `EXECUTE_MP`.

**CRT — Cognitive Routing Table** (`01_BACKBONE/AGENTS/04_ROUTING/CRT/`)
- Lookup table pour router les tâches cognitives vers les **LLMs** selon le type de tâche, la fenêtre de contexte, le coût et la qualité requise.
- Schema : `cognitive_task_type → preferred_model + fallback_model + context_window_required + cost_tier + quality_requirement`
- Submodule de `AGENTS/04_ROUTING`. Pas standalone.
- ART prend la précédence pour les opérations trust-gated. CRT et ART sont consultés ensemble pour les décisions complexes.
- Note : une K-Card existante définit aussi CRT comme "Cost-Routing-Threshold" (intercepte chaque prompt, route vers le modèle le plus cost-efficient satisfaisant le seuil de qualité). Les deux définitions coexistent — CRT est à la fois une table de routing cognitif ET un mécanisme de cost-efficiency.

**MPM — Multi-Prompt Manager** (`01_BACKBONE/MPM/`)
- Protocole de transport inter-LLM. Packets typés : MP (generic), MPM (Manus), MPC (Claude), MPX (ChatGPT), MPG (Gemini), MPP (Perplexity).
- Modes : sprint / run / marathon.
- Pattern coordinator-worker pour les marathons.
- Execution Ledger JSON : tracking des MPMs avec status (draft → running → executed_awaiting_guardian_review → guardian_accepted/rejected).
- Architect & Guardian (A&G) review : ChatGPT joue le rôle d'architecte et de gardien pour valider les outputs critiques.

**YARP** (`01_BACKBONE/YARP/`)
- Artifact Routing Protocol. Encode les décisions de routing ART dans des messages `EXECUTE_MP`.

**BUS** (`01_BACKBONE/BUS/`)
- Bus de communication inter-modules. MPM-BUS bridge protocol.

---

## Ce qui a été créé aujourd'hui (à intégrer)

**TRT — Task Routing Table** (`01_BACKBONE/ROUTING/TASK-ROUTING-TABLE.md`)
- Créé en session Manus 2026-07-29 pour répondre à un besoin non couvert : **décider AVANT l'exécution** où et comment router une tâche (intra-session, inter-session, inter-LLM, inter-outils).
- 7 modes : INLINE, INLINE-CLOSE, NEW SESSION, RESUME, TARGET-LLM, DIRECT, ORCHESTRATED.
- Contient un arbre de décision avec consultation du Task Ledger en étape 0.
- **Problème** : créé sans relire ART/CRT → risque de redondance ou de conflit.

**Task Ledger** (concept, pas encore implémenté proprement)
- Log cross-LLM de toutes les tâches Y-OS (quel LLM, quelle session, quel statut, quel thème).
- Besoin : permettre au TRT de savoir si une tâche similaire a déjà été traitée, dans quel LLM, dans quelle session.
- Différent du MPM Execution Ledger (qui track les MPMs formels) : le Task Ledger track les tâches informelles aussi (conversations, décisions, chantiers).
- Emplacement proposé : `08_LOGS/task-ledger/` (YAML par tâche).

---

## Ta mission

**Objectif** : Concevoir l'architecture propre et cohérente de TRT + Task Ledger dans le contexte existant ART/CRT/MPM/YARP/BUS.

**Questions à résoudre** :

1. **Positionnement de TRT** : TRT opère à un niveau différent de ART et CRT. ART route vers des agents, CRT route vers des LLMs pour des tâches cognitives. TRT décide *si* et *où* créer une nouvelle session. Quelle est la relation exacte entre les trois ? Sont-ils tous des submodules de `AGENTS/04_ROUTING` ? Ou TRT est-il au-dessus ?

2. **Redondance CRT/TRT** : La section "Sélection du LLM cible" dans TRT (quel LLM pour quelle tâche) est-elle redondante avec CRT ? Comment les articuler sans duplication ?

3. **Task Ledger vs MPM Execution Ledger** : Deux ledgers distincts ou un seul ? Le MPM Execution Ledger track les MPMs formels. Le Task Ledger track toutes les tâches (formelles et informelles). Faut-il étendre le MPM Execution Ledger ou créer un Task Ledger séparé ?

4. **Méta-orchestrateur** : Manus a proposé un "Y-OS Orchestration Core" au-dessus de TRT/ART/CRT. Mais ORCH existe déjà dans Y-OS. Faut-il étendre ORCH ? Créer un sous-module ? Ou est-ce que MPM joue déjà ce rôle ?

5. **Routing inter-outils** : TRT a un mode TARGET-LLM pour les contraintes d'outils (connecteur MCP accessible uniquement depuis un LLM spécifique). Ce concept existe-t-il déjà dans ART/CRT ? Où le placer canoniquement ?

**Livrables attendus** :

1. **Diagramme d'architecture** (Mermaid ou ASCII) montrant les relations entre TRT, ART, CRT, MPM, YARP, BUS, Task Ledger, ORCH.
2. **Définition canonique de TRT** : nom complet, rôle précis, scope, ce qu'il fait / ne fait pas, relation avec ART et CRT.
3. **Décision sur le Task Ledger** : structure finale, emplacement, relation avec MPM Execution Ledger.
4. **Révision de TASK-ROUTING-TABLE.md** : corrections à apporter pour supprimer les redondances et aligner avec l'architecture existante.
5. **Note sur le méta-orchestrateur** : ORCH suffit-il ? Que faut-il ajouter/modifier ?

**Contraintes** :
- Ne pas modifier les définitions existantes de ART et CRT.
- Garder le naming `*RT` pour la cohérence (ART, CRT, TRT).
- Garder le Task Ledger comme concept distinct du MPM Execution Ledger si justifié.
- Tout doit être committable dans `YOS/` sur GitHub.

---

## Output Format

Réponds avec :
1. Un bloc `## Architecture Diagram` (Mermaid).
2. Un bloc `## Canonical Definitions` (tableau des 3 modules + Task Ledger).
3. Un bloc `## TASK-ROUTING-TABLE.md — Corrections` (diff ou liste de changements).
4. Un bloc `## Decision Log` (tes décisions et justifications).

Format : Markdown pur, committable directement dans YOS.
