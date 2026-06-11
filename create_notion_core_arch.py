#!/usr/bin/env python3
import subprocess, json, sys

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

CONTENT = """# Y-OS Core Architecture v1

**Auteur :** Manus AI | **Date :** 11 Juin 2026 | **Statut :** Officiel

---

## 1. Vision Globale

Y-OS est structuré autour d'un noyau de six modules interdépendants. Chaque module répond à une question fondamentale distincte. Cette séparation stricte des responsabilités garantit la scalabilité, la clarté et l'extensibilité du système.

---

## 2. Diagramme Logique

```
/YOS (Launcher)          <- How do I access?
  | lit
Y-REG (Registry)         <- What exists?
  ^ enregistre
Y-DEV (Development)      <- How to develop?
  ^ declenche
Y-CAP (Capabilities)     <- How to acquire?
  ^ delegue
Y-ORC (Orchestrator)     <- What is needed now?
  | lit contexte
Y-MEM (Memory)           <- What is known?
```

---

## 3. Les 6 Composants Fondamentaux

### Y-REG — Registry
**Question :** What exists?

**Purpose :** Registre canonique de tous les objets activables du systeme.

**Responsibilities :** Enregistrer, classer et exposer les objets (Protocols, Skills, Workflows, Agents, Automations, Services, Projects, Commands, Prompts). Gerer leur cycle de vie.

**Non-responsibilities :** Ne stocke pas de donnees metier ni d'historique de conversation. N'execute aucun code.

**Inputs :** Fichiers de definition YAML/Markdown, requetes de decouverte.

**Outputs :** Listes structurees d'objets, statuts, metadonnees, dependances.

**Relationships :** Lu par /YOS et Y-ORC. Alimente en fin de cycle par Y-DEV.

---

### Y-MEM — Memory
**Question :** What is known?

**Purpose :** Memoire et base de connaissances du systeme.

**Responsibilities :** Stocker et restituer les decisions, preferences, historiques de session, documents, contextes de projets et connaissances generales.

**Non-responsibilities :** Ne stocke pas le code source des skills ni les definitions d'infrastructure (role de Y-REG).

**Inputs :** Resumes de sessions, documents utilisateurs, notes, resultats d'execution.

**Outputs :** Contexte injecte, reponses semantiques, historiques.

**Relationships :** Interroge en permanence par Y-ORC pour assembler le contexte avant execution.

---

### Y-ORC — Orchestrator
**Question :** What is needed now?

**Purpose :** Cerveau executif qui assemble le contexte et coordonne l'action.

**Responsibilities :** Routing, orchestration des workflows, assemblage du contexte (depuis Y-MEM), coordination entre agents et LLMs.

**Non-responsibilities :** Ne stocke rien a long terme. Ne developpe pas de nouvelles capacites.

**Inputs :** Requetes utilisateur, triggers temporels ou evenements externes.

**Outputs :** Appels d'API, declenchements de Workflows/Skills, reponses a l'utilisateur.

**Relationships :** Lit Y-REG pour les outils disponibles. Lit Y-MEM pour le contexte. Appelle Y-CAP si un outil manque.

---

### /YOS — Launcher
**Question :** How do I access Y-OS?

**Purpose :** Point d'entree et launcher universel.

**Responsibilities :** Decouverte, navigation, recherche et declenchement initial des objets.

**Non-responsibilities :** N'orchestre pas de workflows complexes. Ne stocke aucune donnee.

**Inputs :** Commandes utilisateur (ex: --advanced, --type skill).

**Outputs :** Menus, listes d'options, requetes transmises a Y-ORC ou execution directe de commandes simples.

**Relationships :** Lit exclusivement Y-REG pour generer son affichage.

---

### Y-CAP — Capabilities
**Question :** How do we acquire new capabilities?

**Purpose :** Pole d'acquisition et d'integration de nouvelles competences.

**Responsibilities :** Decider de la strategie d'acquisition (achat, integration d'API, reutilisation, adaptation, ou developpement custom).

**Non-responsibilities :** Ne gere pas l'execution quotidienne (role de Y-ORC).

**Inputs :** Demande de capacite manquante (souvent issue de Y-ORC).

**Outputs :** Cahier des charges, decision d'integration, ou ticket de developpement.

**Relationships :** Delegue la creation technique a Y-DEV si le developpement custom est choisi.

---

### Y-DEV — Development
**Question :** How do we develop a capability?

**Purpose :** Protocole strict de conception et d'implementation.

**Responsibilities :** Suivre les etapes canoniques : Architecture > Specs > Review > Tool/Code Mining > Build Strategy > Implementation > Review.

**Non-responsibilities :** Ne decide pas si on doit developper (role de Y-CAP).

**Inputs :** Specifications issues de Y-CAP.

**Outputs :** Code teste, documentation, fichier de definition (Markdown/YAML).

**Relationships :** Une fois le developpement valide, l'objet est enregistre dans Y-REG.

---

## 4. Frontieres et Risques de Confusion

**Y-REG vs Y-MEM :** Y-REG est le catalogue des outils (le garage). Y-MEM est le catalogue des souvenirs (la bibliotheque). Y-REG contient la liste des marteaux et des scies. Y-MEM contient les plans de la maison et l'historique des travaux.

**Y-CAP vs Y-DEV :** Y-CAP est le directeur des achats/strategie — il decide s'il faut acheter sur etagere, brancher un SaaS, ou fabriquer en interne. Y-DEV est l'usine de fabrication — il n'intervient que si Y-CAP a decide de fabriquer, et applique un protocole strict.

**/YOS vs Y-REG :** Y-REG est la base de donnees (backend canonique). /YOS est la vitrine (frontend/launcher) qui lit Y-REG pour montrer ce qui est disponible.

**Le role exact de Y-ORC :** Y-ORC est le chef d'orchestre en temps reel. Contrairement a Y-REG (statique) ou Y-MEM (passif), Y-ORC est le moteur dynamique qui prend une requete, cherche le contexte dans Y-MEM, cherche l'outil dans Y-REG, et lance l'execution.

---

## 5. Dependances

1. /YOS depend totalement de Y-REG (si Y-REG est vide, /YOS est vide).
2. Y-ORC depend de Y-REG (outils) et de Y-MEM (contexte).
3. Y-DEV alimente Y-REG (output final).
4. Y-CAP declenche Y-DEV.

---

## 6. Validation Checklist

- Difference Y-REG / Y-MEM : Y-REG = outils, Y-MEM = connaissances.
- Difference Y-CAP / Y-DEV : Y-CAP = decision d'acquisition, Y-DEV = protocole de fabrication.
- Role Y-ORC : orchestration dynamique en temps reel.
- Pourquoi /YOS n'est pas Y-REG : /YOS est une interface, Y-REG est une base de donnees.
- Composants fondamentaux : tous les 6 sont fondamentaux.
- Dependances : /YOS -> Y-REG ; Y-ORC -> Y-REG + Y-MEM ; Y-DEV -> Y-REG ; Y-CAP -> Y-DEV.

---

## 7. Glossaire

- **Agent :** Entite autonome capable de raisonner et d'executer des workflows (ex: Manus).
- **Capability :** Competence atomique exposee par un Skill ou un Agent (ex: Text Generation).
- **Skill :** Composant logiciel encapsulant une logique metier ou une integration specifique.
- **Workflow :** Sequence d'actions orchestrant plusieurs Skills ou Services.
- **Protocol :** Regle de gouvernance (ex: Y-DEV, Y-REG).
- **Source of Truth :** Systeme de stockage canonique (Obsidian+Git pour Y-REG).
"""

payload = {
    "parent": {"page_id": PARENT_ID},
    "pages": [{
        "properties": {"title": "Y-OS Core Architecture v1"},
        "content": CONTENT
    }]
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
       "--server", "notion", "--input", json.dumps(payload)]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
output = result.stdout + result.stderr
print(output[-800:])
