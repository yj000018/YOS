---
device_id: AND-002
model: Samsung Galaxy Z Fold 7
status: pending_delivery
decision_management: Baseline légère — Tailscale + ADB + HA (No MDM, No Knox)
decision_date: 2026-08-07
---

# AND-002 — Galaxy Z Fold 7 — Procédure Setup

> **⚠️ DÉCISION CRITIQUE** : Le choix du mode de gestion doit être pris **avant le premier démarrage (OOBE)**. L'enrôlement Device Owner n'est possible qu'à cette étape ou après factory reset.

---

## Étape 0 — Décision de gestion (AVANT déballage)

### Matrice de décision

| Scénario | Mode recommandé | Conséquence |
|---|---|---|
| **Usage exclusivement professionnel** | Fully Managed (Device Owner) via Knox | Contrôle total, pas d'espace personnel |
| **Pro + perso assumé** ⭐ | **WP-C/COPE** (Work Profile Corporate-Owned) | Séparation pro/perso, contrôle pro uniquement |
| **Perso avec outils pro** | Work Profile BYOD | Respect maximal du perso, conformité limitée |
| **Pas prêt pour MDM** | Tailscale + ADB + HA, sans MDM | Réversible, pas d'enforcement policy |

**DéCISION PRISE ✅ : WP-C/COPE** — Pro + perso (confirmé 2026-08-07)

> Usage pro/perso mixte. Espace professionnel séparé de l'espace personnel. Contrôle Y-OS limité à l'espace pro.

---

## Étape 1 — Avant le premier démarrage

- [ ] Décision de gestion prise et documentée
- [ ] Si Knox/EMM : avoir le QR code d'enrôlement prêt (Knox Mobile Enrollment ou EMM)
- [ ] Compte Samsung créé et 2FA configuré
- [ ] Compte Google professionnel prêt
- [ ] Tailscale installé sur un autre appareil pour vérifier la connexion

---

## Étape 2 — OOBE (Out Of Box Experience)

**Décision confirmée : Baseline légère — No MDM, No Knox (2026-08-07)**

1. Démarrer normalement, connecter WiFi
2. Connecter compte Google
3. Connecter compte Samsung
4. **Ne pas activer Knox** — pas de MDM
5. **Ne pas restaurer depuis iPhone** — repartir propre Android natif
6. Biométrie : empreinte + PIN robuste
7. Laisser les mises à jour se faire

---

## Étape 3 — Configuration baseline Y-OS (tous modes)

```bash
# Depuis le CC après pairing ADB
ADB="adb -s <IP_FOLD7>:5555"

# 1. Activer Wireless Debugging (manuellement sur l'appareil)
# Paramètres → Options développeur → Wireless debugging → ON

# 2. Pairing initial
adb pair <IP>:<PORT_PAIRING> <CODE>

# 3. Connexion permanente
adb connect <IP>:5555

# 4. Vérifier
$ADB shell getprop ro.product.model
```

**Apps à installer en priorité :**
1. Tailscale (Play Store)
2. Home Assistant Companion (quand N100 prêt)
3. Pushover (notifications Y-OS)
4. Obsidian, Notion, Claude, ChatGPT, Perplexity

**Paramètres critiques :**
- Options développeur → ON (Wireless Debugging)
- Batterie → Protection batterie ON, charge optimisée ON
- Privacy Dashboard → révision permissions
- Adaptive Battery → ON
- Refresh rate → Adaptive (120Hz)

---

## Étape 4 — Intégration Y-OS

- [ ] Ajouter dans `FLEET` du `health_probe.py` sur le CC
- [ ] Ajouter dans `FLEET` du `drift_packages.py`
- [ ] Créer fiche `AND-002-GALAXY-FOLD7.md`
- [ ] Ajouter ACL Tailscale (CC → Fold 7 uniquement)
- [ ] Premier snapshot packages
- [ ] Notif Telegram : "AND-002 Fold 7 opérationnel"
