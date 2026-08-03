#!/usr/bin/env python3
"""
Stocke tous les tokens validés dans 1Password MAIN VAULT
Format: op item create --category API_CREDENTIAL --vault "MAIN VAULT"
"""

import subprocess
import json
import os
import sys

VAULT = "MAIN VAULT"

# Tous les tokens à stocker
TOKENS = [
    {
        "name": "Linear API Key — yOS",
        "var": "LINEAR_API_KEY",
        "value": "op://MAIN VAULT/Linear API Key — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Todoist API Token — yOS",
        "var": "TODOIST_API_TOKEN",
        "value": "op://MAIN VAULT/Todoist API Token — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Sentry Auth Token — yOS",
        "var": "SENTRY_AUTH_TOKEN",
        "value": "op://MAIN VAULT/Sentry Auth Token — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Cloudinary API Credentials — yOS",
        "var": "CLOUDINARY_CLIENT_ID",
        "value": "op://MAIN VAULT/Cloudinary API Credentials — yOS/credential",
        "extra_fields": [
            ("client_secret", "b4b0c002688aba1b8e1df1038b01905cdea85450baf0a8ffd7b71a442078f151"),
        ],
        "tags": ["yos-manus", "yos-secret", "oauth2"],
        "status": "OAUTH2",
    },
    {
        "name": "MailerLite API Token — yOS",
        "var": "MAILERLITE_API_KEY",
        "value": "op://MAIN VAULT/MailerLite API Token — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Monday.com API Token — yOS",
        "var": "MONDAY_API_TOKEN",
        "value": "op://MAIN VAULT/Monday.com API Token — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Jotform API Key — yOS",
        "var": "JOTFORM_API_KEY",
        "value": "op://MAIN VAULT/Jotform API Key — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Ahrefs API Token — yOS",
        "var": "AHREFS_API_TOKEN",
        "value": "op://MAIN VAULT/Ahrefs API Token — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "STORED_UNVERIFIED",  # 404 sur tous les endpoints testés
        "note": "Token stocké mais endpoint Ahrefs v3 retourne 404 — vérifier le plan Ahrefs",
    },
    {
        "name": "Tavily API Key — yOS",
        "var": "TAVILY_API_KEY",
        "value": "op://MAIN VAULT/Tavily API Key — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "STORED_UNVERIFIED",  # 403 — IP sandbox bloquée
        "note": "Token stocké mais 403 depuis sandbox IP — probablement valide depuis IP normale",
    },
    {
        "name": "Miro API Credentials — yOS",
        "var": "MIRO_CLIENT_ID",
        "value": "op://MAIN VAULT/Miro API Credentials — yOS/credential",
        "extra_fields": [
            ("client_secret", "op://MAIN VAULT/Miro API Credentials — yOS/client_secret"),
        ],
        "tags": ["yos-manus", "yos-secret", "oauth2"],
        "status": "OAUTH2",
    },
    {
        "name": "Wolfram Alpha AppID — yOS",
        "var": "WOLFRAM_APP_ID",
        "value": "op://MAIN VAULT/Wolfram Alpha AppID — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
    {
        "name": "Google Maps API Key — yOS",
        "var": "GOOGLE_MAPS_API_KEY",
        "value": "op://MAIN VAULT/Google Maps API Key — yOS/credential",
        "tags": ["yos-manus", "yos-secret", "api-key"],
        "status": "VALID",
    },
]

def item_exists(name):
    """Vérifie si un item existe déjà dans 1Password"""
    result = subprocess.run(
        ["op", "item", "get", name, "--vault", VAULT, "--fields", "credential"],
        capture_output=True, text=True
    )
    return result.returncode == 0

def create_or_update_item(token):
    name = token["name"]
    var = token["var"]
    value = token["value"]
    tags = token.get("tags", ["yos-manus"])
    extra = token.get("extra_fields", [])

    # Vérifier si l'item existe
    exists = item_exists(name)

    if exists:
        # Mettre à jour
        cmd = [
            "op", "item", "edit", name,
            "--vault", VAULT,
            f"credential={value}",
        ]
        action = "UPDATE"
    else:
        # Créer
        cmd = [
            "op", "item", "create",
            "--category", "API Credential",
            "--vault", VAULT,
            f"--title={name}",
            f"--tags={','.join(tags)}",
            f"credential={value}",
        ]
        action = "CREATE"

    # Ajouter les champs extra
    for field_name, field_value in extra:
        cmd.append(f"{field_name}={field_value}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {action}: {name} [{token['status']}]")
        return True
    else:
        print(f"❌ {action} FAILED: {name}")
        print(f"   Error: {result.stderr[:200]}")
        return False

# Exécution
print("=" * 60)
print("STOCKAGE 1PASSWORD — ART Token Store")
print("=" * 60)

created = updated = failed = 0
for token in TOKENS:
    exists = item_exists(token["name"])
    ok = create_or_update_item(token)
    if ok:
        if exists:
            updated += 1
        else:
            created += 1
    else:
        failed += 1

print("\n" + "=" * 60)
print(f"RÉSULTAT: {created} créés | {updated} mis à jour | {failed} échecs")
print("=" * 60)

# Sauvegarder le rapport
report = {
    "created": created,
    "updated": updated,
    "failed": failed,
    "tokens": [{"name": t["name"], "var": t["var"], "status": t["status"]} for t in TOKENS]
}
with open("/tmp/store_1p_report.json", "w") as f:
    json.dump(report, f, indent=2)
print("Rapport: /tmp/store_1p_report.json")
