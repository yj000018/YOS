# Y-OS Tool Registry

**Single Source of Truth** pour tous les outils intégrés dans Y-OS.

## Structure

```
tool_registry/
├── README.md                          # Ce fichier
├── yos_tool_registry.json             # Registre complet (87 outils)
├── YOS_Secret_Management_Architecture.md  # Architecture SSOT
├── YOS_Tool_Registry_Report.md        # Rapport d'analyse
├── fact_sheets/                       # 87 Tool Fact Sheets individuelles
│   ├── openai.md
│   ├── anthropic.md
│   └── ...
└── scripts/
    ├── sync_1p_to_manus.py            # Sync 1Password → Manus
    ├── yos_secrets.py                 # Module de gestion des secrets (fallback)
    ├── yos_secret_audit.py            # Audit de cohérence des miroirs
    └── build_tool_registry.py         # Reconstruction du registre
```

## Architecture

```
1Password (SSOT)
    ↓ sync_1p_to_manus.py
Manus Custom API Connectors (Mirror)
    ↓ yos_secrets.py (fallback)
Scripts Y-OS
```

## Statistiques

- **87 outils** inventoriés
- **49** avec clé API
- **34** MCP Managed (token injecté par Manus)
- **4** OAuth natif (Gmail, Google Calendar, Instagram, Shopify)
- **39** items manquants dans 1Password → à créer

## Usage

```bash
# Synchroniser 1Password → Manus
python3 scripts/sync_1p_to_manus.py

# Auditer la cohérence des miroirs
python3 scripts/yos_secret_audit.py --verbose

# Utiliser un secret dans un script
from yos_secrets import get_secret
api_key = get_secret("OPENAI_API_KEY")
```
