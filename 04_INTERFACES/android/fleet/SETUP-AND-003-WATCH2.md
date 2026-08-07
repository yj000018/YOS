---
device_id: AND-003
model: Samsung Galaxy Watch 2 (modèle exact à confirmer)
status: pending_delivery
integration: Home Assistant (pas ADB)
---

# AND-003 — Galaxy Watch 2 — Procédure Qualification & Setup

> **Principe** : La Watch ne passe pas par ADB/Tailscale. Son intégration Y-OS se fait via **Home Assistant Companion/Wear** + **Samsung Health** (opt-in strict).

---

## Étape 0 — Qualification à réception (AVANT tout setup)

### Vérifications obligatoires

| Point | À vérifier | Pourquoi |
|---|---|---|
| **Modèle exact** | Galaxy Watch 2 40mm ou 44mm ? SM-R??? | Compatibilité apps |
| **Wear OS version** | Wear OS 4 ou 5 ? | HA Companion Wear nécessite Wear OS 3+ |
| **One UI Watch version** | 5.0 ou 6.0 ? | Fonctionnalités et permissions |
| **Téléphone compagnon** | Fold 7 (Android) — compatible ✅ | Galaxy Watch = Samsung/Android uniquement |
| **Galaxy Wearable app** | Disponible sur Fold 7 | App de gestion obligatoire |
| **HA Companion Wear** | Disponible sur Galaxy Watch 2 ? | Vérifier Play Store Wear OS |

### Commande de vérification (une fois appairée au Fold 7)
```bash
# Via ADB sur le Fold 7 (pas la Watch directement)
adb -s <FOLD7_IP>:5555 shell dumpsys package com.samsung.android.app.watchmanager | grep version
```

---

## Étape 1 — Setup initial

1. **Appairer au Fold 7** via Galaxy Wearable app (Bluetooth)
2. **Compte Samsung** : connecter le même compte que le Fold 7
3. **Mises à jour** : mettre à jour Wear OS + Galaxy Watch software avant toute config
4. **Permissions santé** : activer **uniquement** les capteurs utiles (pas tout en bloc)

### Capteurs à activer (opt-in conscient)
- [ ] Fréquence cardiaque (si usage fitness)
- [ ] Activité physique (pas, calories)
- [ ] Sommeil (si suivi souhaité)
- [ ] SpO2 (si usage santé)
- [ ] **NE PAS activer** : localisation GPS permanente, micro ambiant

---

## Étape 2 — Intégration Home Assistant (quand N100 prêt)

### Prérequis
- HA installé sur N100 et accessible
- HA Companion installé sur Fold 7 (téléphone compagnon)
- HA Companion Wear installé sur la Watch (si disponible)

### Ce que HA peut exposer depuis la Watch
| Capteur | Disponibilité | Fréquence |
|---|---|---|
| Batterie Watch | ✅ Via Companion téléphone | 15min |
| Connexion Watch↔Téléphone | ✅ | Événement |
| Activité (pas, calories) | ⚠️ Via Health Connect | Quotidien |
| Fréquence cardiaque | ⚠️ Via Health Connect opt-in | Quotidien |
| Localisation | ❌ Pas de GPS Watch dans HA | — |

> **Règle Y-OS** : données santé = contexte volontaire uniquement. Jamais de monitoring exhaustif automatique. Jamais dans Telegram.

---

## Étape 3 — Intégration Y-OS minimale

```python
# Ajouter dans health_probe.py — via Fold 7 comme proxy
# (pas d'ADB direct sur Watch)
"AND-003": {
    "name": "Galaxy Watch 2",
    "type": "wear_os",
    "proxy": "AND-002",  # Fold 7 comme proxy
    "integration": "home_assistant",  # pas ADB
    "adb_host": None
}
```

**Métriques disponibles sans HA :**
- Batterie Watch : via `adb -s <FOLD7> shell dumpsys battery` (si exposée)
- Statut connexion : via Galaxy Wearable app

---

## Étape 4 — Fiche AND-003

À créer après réception et qualification :
- Modèle exact, Wear OS version, One UI Watch version
- Capteurs activés (liste opt-in)
- Intégration HA : oui/non, capteurs exposés
- Décision monitoring : scope et fréquence

---

## Limitations connues

| Limitation | Impact |
|---|---|
| Pas de Tailscale sur Wear OS | Pas d'accès direct CC → Watch |
| Pas d'ADB TCP/IP stable sur Watch | Diagnostic uniquement via Fold 7 |
| Health Connect = opt-in strict | Données santé non automatisables sans consentement |
| HA Companion Wear = beta | Fonctionnalités limitées vs Android |
