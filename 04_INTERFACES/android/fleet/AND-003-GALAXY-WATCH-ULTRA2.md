---
device_id: AND-003
owner: Yannick
role: Santé, fitness, micro-interactions
status: pending_pairing
model: Samsung Galaxy Watch Ultra 2 (2026)
management_level: Bluetooth via AND-002 (Fold 7) + HA Companion
last_updated: 2026-08-07
---

# AND-003 — Samsung Galaxy Watch Ultra 2 (2026)

## Identité

| Champ | Valeur |
|---|---|
| **Modèle** | Samsung Galaxy Watch Ultra 2 (2026) |
| **OS** | Wear OS 7 (Powered by Samsung) |
| **One UI Watch** | 8 |
| **RAM / Stockage** | 2 GB / 64 GB |
| **Bluetooth** | 6.0 |
| **GPS** | L1+L5 Dual Frequency |
| **Mises à jour garanties** | 5 ans (jusqu'en 2031) |
| **Téléphone compagnon** | AND-002 Galaxy Z Fold 7 (à réception) |
| **Statut** | 🔜 En attente d'appairing avec AND-002 |

## Décisions d'architecture

| Décision | Choix | Raison |
|---|---|---|
| **Tailscale** | ❌ Non disponible | Wear OS ne supporte pas Tailscale |
| **ADB remote** | ❌ Pas via Tailscale | Pas d'accès direct CC → Watch |
| **ADB WiFi local** | ⚠️ Diagnostic uniquement | Même réseau requis, pas permanent |
| **Canal principal** | ✅ Bluetooth via Fold 7 | Canal natif Samsung |
| **Monitoring Y-OS** | ✅ Via HA Companion (quand N100 prêt) | Batterie, connexion, activité opt-in |
| **MDM** | ❌ Non applicable | Wear OS ne supporte pas Knox/MDM |
| **Données santé** | ✅ Opt-in strict via Health Connect | Jamais automatique, jamais dans Telegram |

## Pipeline de contrôle Y-OS

```
Manus → CC → ADB → AND-002 (Fold 7) → Galaxy Wearable → AND-003 (Watch)
                                    ↓
                          HA Companion Wear (quand N100 prêt)
                                    ↓
                          Home Assistant → entités batterie/activité
```

## Connectivité

| Canal | Disponible | Usage |
|---|---|---|
| **Bluetooth** (via Fold 7) | ✅ Principal | Notifications, apps, sync santé, Galaxy Wearable |
| **WiFi direct** (même réseau) | ✅ Secondaire | Sync rapide, mises à jour OTA |
| **ADB WiFi local** | ⚠️ Diagnostic | Debug ponctuel, même réseau requis |
| **USB/câble** | ❌ | Pas de port USB sur Watch Ultra 2 |
| **ADB via Bluetooth** | ❌ Non recommandé | Instable, peu fiable |

## Télémétrie disponible (via HA Companion)

| Capteur | Disponibilité | Fréquence | Opt-in |
|---|---|---|---|
| Batterie Watch | ✅ Via Companion téléphone | 15 min | Auto |
| Connexion Watch↔Téléphone | ✅ Événement | Temps réel | Auto |
| Activité (pas, calories) | ⚠️ Via Health Connect | Quotidien | Manuel |
| Fréquence cardiaque | ⚠️ Via Health Connect | Quotidien | Manuel |
| Sommeil | ⚠️ Via Health Connect | Quotidien | Manuel |
| Localisation GPS | ❌ Non exposé dans HA | — | N/A |

> **Règle Y-OS** : données santé = contexte volontaire uniquement. Activer capteur par capteur. Jamais dans Telegram. Jamais d'inférence automatique sur état de santé.

## Capteurs à activer (décision à prendre à réception)

- [ ] Fréquence cardiaque (si usage fitness actif)
- [ ] Activité physique (pas, calories) — valeur quotidienne
- [ ] Sommeil (si suivi souhaité)
- [ ] SpO2 (si usage santé)
- [ ] **NE PAS activer** : localisation GPS permanente, micro ambiant

## Prochaines actions

- [ ] Réceptionner AND-002 (Fold 7) — téléphone compagnon
- [ ] Appairer AND-003 via Galaxy Wearable sur AND-002
- [ ] Installer Galaxy Wearable + HA Companion Wear sur AND-003
- [ ] Activer capteurs santé opt-in (liste ci-dessus)
- [ ] Configurer HA Companion sur AND-002 (quand N100 prêt)
- [ ] Créer entités HA : batterie Watch, connexion, activité
- [ ] Ajouter monitoring batterie Watch dans `health_probe.py` (via AND-002 proxy)
