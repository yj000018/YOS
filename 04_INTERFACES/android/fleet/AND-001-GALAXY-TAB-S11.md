---
device_id: AND-001
owner: Yannick
role: Tablette créative & démonstrateur yOS
status: operational
management_level: P0 — ADB + Tailscale (sans MDM)
last_updated: 2026-08-07
---

# AND-001 — Samsung Galaxy Tab S11

## Identité

| Champ | Valeur |
|---|---|
| **Modèle** | Samsung Galaxy Tab S11 (SM-X730) |
| **Android** | 16 (SDK 36) |
| **Build** | X730XXU1AXG4 |
| **Patch sécurité** | 2026-07-01 |
| **Tailscale IP** | 100.89.158.44 |
| **ADB endpoint** | 100.89.158.44:5555 |
| **Pipeline CC** | CC (100.93.75.9) → Tailscale/DERP → Tab S11 |

## Santé (snapshot 2026-08-07)

| Métrique | Valeur | Seuil alerte |
|---|---|---|
| **Batterie** | 57% · non chargée · Li-ion | <20% → P2, <10% → P1 |
| **Température batterie** | 24.3°C | >40°C → P2 |
| **Stockage /data** | 19% utilisé (44 GB / 234 GB) | >85% → P2, >92% → P1 |
| **RAM totale** | 11.8 GB | — |
| **RAM disponible** | 5.3 GB | <1 GB → P2 |
| **Uptime** | 2 jours 4h53 | — |
| **Load average** | 24.98 / 24.70 / 24.65 | >50 → investiguer |
| **Apps tierces actives** | 118 | — |

> ⚠️ Load average élevé (~25) — normal sur Android (threads kernel comptés différemment), à surveiller sur tendance.

## Gestion & Connectivité

| Composant | État |
|---|---|
| **Tailscale** | ✅ Connecté — IP 100.89.158.44 |
| **Wireless Debugging** | ✅ Actif — port 5555 |
| **ADB depuis CC** | ✅ Opérationnel |
| **Auto-reconnect cron** | ✅ Actif (*/2 min sur CC) |
| **Notif Telegram sur échec** | ✅ Après 3 échecs consécutifs |
| **MDM** | ❌ Non enrôlé (décision P0 — pas de reset) |
| **Home Assistant** | 🔜 À installer (P1) |

## Profil applicatif

- **Apps tierces actives** : 118 (debloaté depuis 190 le 2026-08-07)
- **Bloatwares Samsung désactivés** : 14 (Bixby DE/IT, TTS, TV Plus, Kids Mode, etc.)
- **Apps supprimées** : 32 (IA doublons, jeux, gadgets, browsers doublons)

## Décisions d'architecture

- **Pas de MDM rétroactif** : A1 ne sera pas réinitialisé pour enrôlement. MDM possible uniquement après backup validé + acceptation explicite d'un reset.
- **ADB = canal de contrôle P0** : seul le CC est autorisé comme hôte ADB. Aucun port ADB exposé à Internet.
- **Wireless Debugging** : stable sur reboot normal. Reset possible sur OTA majeure → cron notifie automatiquement.

## Prochaines actions (P1)

- [ ] Installer Home Assistant Companion → activer capteurs batterie/stockage/réseau
- [ ] Déployer health probe ADB automatisé (script CC, cron 15min)
- [ ] Générer rapport de santé initial (baseline)
- [ ] Configurer alertes Telegram P1/P2 dédupliquées
- [ ] Activer détection drift applicatif (diff packages quotidien)
