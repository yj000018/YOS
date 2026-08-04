# Y-OS Hardware Registry
> **Source of truth** : ce fichier dans `yj000018/YOS`
> **Last updated** : 2026-08-05
> **Maintenu par** : Manus (mise à jour à chaque nouvelle machine ou changement réseau)

---

## Règle d'utilisation

> À chaque session Manus impliquant un appareil physique, lire ce fichier pour éviter de redemander les specs.
> Mettre à jour après chaque changement : nouvelle machine, nouvelle IP Tailscale, changement de rôle.

---

## Tailnet : `tail7c87e1.ts.net`

| Hostname Tailscale | IP Tailscale | Appareil | Statut | Rôle Y-OS |
|---|---|---|---|---|
| `yos-cloud-operator` | `100.93.75.9` | Manus Cloud Computer (GCP) | ✅ online | Pivot réseau, scripts, batches, ADB relay Android |
| `iphone-yan` | `100.115.151.92` | iPhone Yannick (actif) | ✅ online | Mobile principal |
| `galaxy-tab-s11` | `100.89.158.44` | Samsung Galaxy Tab S11 (SM-X730) | ✅ online | Android tablette — ADB via CC→Tailscale direct |
| `galaxy-fold-7` | _à renseigner_ | Samsung Galaxy Z Fold 7 | ⏳ à configurer | Android téléphone — ADB remote |
| `macbook-air-yannick` | `100.67.176.122` | MacBook Air Yannick | ⚠️ offline intermittent | Dev secondaire |
| `macbook-air` | `100.103.112.30` | MacBook Air (autre) | ⚠️ offline | — |
| `anandaz-ubuntu` | `100.87.123.30` | Ubuntu Anandaz | ❌ offline 93j | N100 à réactiver |
| `anandaz-windows` | `100.123.101.75` | Windows Anandaz | ❌ offline 134j | — |
| `nas-synology` | `100.71.221.108` | NAS Synology | ❌ offline 351j | Stockage |
| `iphone-yannick` | `100.78.155.123` | iPhone Yannick (ancien) | ❌ offline 363j | — |

---

## Inventaire détaillé

### CC-001 — Manus Cloud Computer
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `yos-cloud-operator` |
| **Type** | VM GCP (Basic) |
| **OS** | Ubuntu 24.04.4 LTS |
| **vCPU** | 2 |
| **RAM** | 955 MB |
| **Disque** | 33 GB |
| **IP publique** | 34.148.90.222 |
| **IP Tailscale** | 100.93.75.9 |
| **MagicDNS** | yos-cloud-operator.tail7c87e1.ts.net |
| **Tailscale version** | v1.98.10 |
| **ADB** | v1.0.41 — `/usr/bin/adb` |
| **Rôle** | Pivot réseau permanent, scripts Python, batches, ADB relay Android |
| **Accès Manus** | Session préfixée `cloud-pc-8cd489il:` |
| **Ref** | `AGENTS.md` sur le CC |

---

### AND-001 — Samsung Galaxy Tab S11
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `galaxy-tab-s11` |
| **Modèle** | Samsung Galaxy Tab S11 (SM-X730) |
| **Serial** | R5GYB0AXSBY |
| **OS** | Android 16 / One UI 8.0 |
| **SDK** | 36 |
| **Knox** | 3.12 / API 39 |
| **IP locale (WiFi)** | 192.168.1.91 (DHCP stable) |
| **IP Tailscale** | 100.89.158.44 |
| **MagicDNS** | galaxy-tab-s11.tail7c87e1.ts.net |
| **ADB port** | 5555 (tcpip permanent) |
| **ADB connexion** | `adb connect 100.89.158.44:5555` depuis le CC |
| **ADB serial** | R5GYB0AXSBY (guid: adb-R5GYB0AXSBY-91hXvS) |
| **Auto-reconnect** | Cron `*/2 * * * *` → `/home/ubuntu/yos/adb_reconnect.sh` (CC) |
| **Apps tierces** | 190 |
| **Rôle** | Android tablette — contrôle ADB remote via CC→Tailscale |
| **Statut** | ✅ Opérationnel — pipeline CC→Tailscale→ADB validé 2026-08-05 |
| **Doc complète** | `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md` |

**⚠️ Prérequis connexion :**
- Tailscale actif sur la tablette (app Tailscale → Connected)
- Wireless Debugging ON (Paramètres → Options développeur)
- Le CC est dans "Paired devices" sur la tablette

---

### AND-002 — Samsung Galaxy Z Fold 7
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `galaxy-fold-7` |
| **Modèle** | Samsung Galaxy Z Fold 7 (Pro) |
| **OS** | _à renseigner_ |
| **IP Tailscale** | _à renseigner_ |
| **Rôle** | Android téléphone — contrôle ADB remote via CC → Tailscale |
| **Statut** | ⏳ à configurer (session dédiée) |
| **Protocole** | Identique AND-001 — voir `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md` |

---

### MAC-001 — MacBook Pro (à venir)
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `macbook-pro-yannick` |
| **Modèle** | MacBook Pro (arrivée imminente) |
| **Rôle** | Machine centrale always-on, SSH via Tailscale depuis CC |
| **Statut** | ⏳ à configurer à réception |

---

### MAC-002 — MacBook Air Yannick
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `macbook-air-yannick` |
| **IP Tailscale** | 100.67.176.122 |
| **OS** | macOS |
| **Accès** | Manus Desktop Client + bore.pub:22847 (SSH) |
| **Mot de passe** | 4 espaces `    ` |
| **ADB** | v37.0.1 — `/opt/homebrew/bin/adb` |
| **Rôle** | Dev principal actuel, relais ADB pairing initial (1x) |
| **Statut** | ⚠️ offline dans tailnet (Tailscale non actif en permanence) |

---

### N100-001 — N100 Lambda (Anandaz)
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `anandaz-ubuntu` |
| **Type** | MiniPC physique Ubuntu |
| **RAM** | 8–16 GB |
| **IP Tailscale** | 100.87.123.30 |
| **Rôle** | n8n, Home Assistant, Docker, services 24/7 |
| **Statut** | ❌ offline depuis 93j — réactivation session dédiée |

---

### NAS-001 — NAS Synology
| Champ | Valeur |
|---|---|
| **Nom Y-OS** | `nas-synology` |
| **IP Tailscale** | 100.71.221.108 |
| **Statut** | ❌ offline depuis 351j |

---

## Architecture réseau Y-OS

```
Manus (orchestration)
    │
    ▼
CC yos-cloud-operator (100.93.75.9) ← pivot permanent always-on
    │
    ├── Tailscale → Galaxy Tab S11 (100.89.158.44:5555) ← ADB opérationnel ✅
    ├── Tailscale → Galaxy Z Fold 7 (à configurer) ← session future
    ├── SSH bore.pub:22847 → MacBook Air (dev actuel)
    ├── SSH Tailscale → MacBook Pro (à venir, always-on)
    └── SSH Tailscale → N100 Anandaz (100.87.123.30) ← à réactiver
```

---

## Protocole ADB over Tailscale — Résumé

```bash
# Connexion standard depuis le CC
adb kill-server && adb start-server && adb connect 100.89.158.44:5555

# Vérification
adb devices  # → 100.89.158.44:5555  device  SM_X730

# Utilisation
adb -s 100.89.158.44:5555 shell <commande>
```

**Doc complète** : `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md`

---

## Changelog

| Date | Action |
|---|---|
| 2026-08-03 | Création du registre. CC-001 opérationnel dans Tailscale. AND-001 Tailscale en cours d'installation. |
| 2026-08-04 | AND-001 Galaxy Tab S11 : Tailscale connecté (100.89.158.44). Pipeline ADB validé via Mac relais. Screenshot live capturé. |
| 2026-08-05 | **Pipeline final** : CC→Tailscale→100.89.158.44:5555 (bypass AP Isolation). Auto-reconnect cron installé. Module DOC créé. |
