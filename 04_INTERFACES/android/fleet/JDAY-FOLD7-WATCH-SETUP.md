---
title: Procédure J-Day — Déballage Fold 7 + Appairing Watch Ultra 2
devices: AND-002 (Fold 7) + AND-003 (Watch Ultra 2)
estimated_time: 30-45 min
decision: Baseline légère (Tailscale + ADB + HA) — No MDM/Knox
last_updated: 2026-08-07
---

# J-Day — Fold 7 + Watch Ultra 2 Setup

> **Avant de commencer** : dire à Manus "Fold 7 reçu" → Manus prend le relais depuis le CC pour tout ce qui est automatisable.

---

## Phase 1 — Fold 7 : OOBE (15 min)

### Ce que tu fais manuellement

1. **Allumer** le Fold 7
2. **WiFi** : connecter au réseau habituel
3. **Compte Google** : connecter ton compte principal
4. **Compte Samsung** : connecter (même compte que Tab S11)
5. **Restauration** : **NE PAS restaurer depuis iPhone** — repartir propre ⚠️
   - Si proposé "Copier depuis iPhone" → ignorer/passer
   - Partir d'un setup Android natif
6. **Biométrie** : configurer empreinte + PIN robuste
7. **Mises à jour** : laisser se faire (One UI, Google Play)

### Ce que Manus fait depuis le CC (après que tu dises "OOBE terminé")

```bash
# Manus exécute automatiquement :
# 1. Attendre que Tailscale soit installé sur le Fold 7
# 2. adb pair + adb connect
# 3. Snapshot packages initial
# 4. Fiche AND-002 créée
# 5. Notif Telegram "AND-002 Fold 7 opérationnel"
```

---

## Phase 2 — Fold 7 : Apps prioritaires (10 min)

**Installer dans cet ordre :**

| # | App | Store | Priorité |
|---|---|---|---|
| 1 | **Tailscale** | Play Store | 🔴 Critique — requis pour ADB remote |
| 2 | **Galaxy Wearable** | Play Store | 🔴 Requis pour Watch |
| 3 | **Home Assistant** | Play Store | 🟠 Quand N100 prêt |
| 4 | Claude | Play Store | ✅ |
| 5 | ChatGPT | Play Store | ✅ |
| 6 | Perplexity | Play Store | ✅ |
| 7 | Obsidian | Play Store | ✅ |
| 8 | Notion | Play Store | ✅ |
| 9 | Brave Browser | Play Store | ✅ |
| 10 | Telegram | Play Store | ✅ |

**Tailscale — configuration :**
- Ouvrir Tailscale → se connecter avec le compte Tailscale
- Vérifier que le Fold 7 apparaît dans le tailnet
- IP attribuée automatiquement (100.x.x.x)
- Dire à Manus l'IP → Manus fait le reste

---

## Phase 3 — Watch Ultra 2 : Appairing (10 min)

### Ce que tu fais manuellement

1. **Allumer** la Watch Ultra 2
2. Sur le Fold 7 → ouvrir **Galaxy Wearable**
3. Suivre le processus d'appairing Bluetooth
4. **Compte Samsung** : connecter (même compte)
5. **Mises à jour Watch** : laisser se faire
6. **Capteurs santé** : activer uniquement ce que tu veux (voir liste AND-003)

### Capteurs recommandés à activer maintenant

- [ ] Fréquence cardiaque : OUI/NON ?
- [ ] Activité (pas, calories) : OUI recommandé
- [ ] Sommeil : OUI/NON ?
- [ ] SpO2 : OUI/NON ?

---

## Phase 4 — Intégration Y-OS (automatique via Manus)

**Dire à Manus "Fold 7 + Watch appairés"** → Manus exécute :

```bash
# Sur le CC automatiquement :
# 1. adb connect <FOLD7_TAILSCALE_IP>:5555
# 2. Snapshot packages AND-002
# 3. Ajouter AND-002 dans health_probe.py + drift_packages.py
# 4. Créer fiche AND-002-GALAXY-FOLD7.md avec snapshot initial
# 5. Vérifier batterie Watch via ADB Fold 7 (si exposée)
# 6. Push GitHub
# 7. Notif Telegram "AND-002 + AND-003 opérationnels — flotte 3/5"
```

---

## Paramètres système critiques à configurer

### Fold 7

| Paramètre | Valeur | Où |
|---|---|---|
| Options développeur | ON | Paramètres → À propos → Build number ×7 |
| Wireless Debugging | ON | Options développeur → Wireless debugging |
| Adaptive Battery | ON | Batterie → Adaptive Battery |
| Protection batterie | ON | Batterie → Protection batterie |
| Refresh rate | Adaptive | Affichage → Fréquence d'actualisation |
| Privacy Dashboard | Réviser | Confidentialité → Privacy Dashboard |

### Watch Ultra 2

| Paramètre | Valeur | Où |
|---|---|---|
| Always-on display | Selon autonomie | Paramètres → Affichage |
| Wake-up gesture | ON | Paramètres → Avancé |
| Optimisation batterie | OFF pour Galaxy Wearable + HA | Batterie → Optimisation |
| Localisation | Zone seulement | Confidentialité → Localisation |

---

## Checklist finale J-Day

- [ ] Fold 7 OOBE terminé
- [ ] Tailscale installé et connecté sur Fold 7
- [ ] Manus notifié → ADB connecté depuis CC
- [ ] Watch appairée via Galaxy Wearable
- [ ] Capteurs santé configurés (opt-in)
- [ ] Manus notifié → intégration Y-OS complète
- [ ] Notif Telegram reçue "AND-002 + AND-003 opérationnels"
