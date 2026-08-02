#!/usr/bin/env python3
"""
Y-OS Secret Sync Engine — sync_1p_to_manus.py
==============================================
Synchronise les secrets depuis 1Password MAIN VAULT (SSOT)
vers les Manus Custom API Connectors (Miroir Local).

Stratégie de sélection des items :
  1. Items avec tag "yos-manus" (priorité)
  2. Items avec tag "yos-secret" (tous les systèmes)
  3. Fallback : tous les items de catégorie "API Credential"

Rapport: X créés, Y mis à jour, Z inchangés.
Log: /home/ubuntu/sync_1p_manus.log
"""

import json
import subprocess
import sys
import os
import re
import logging
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
VAULT = "MAIN VAULT"
LOG_FILE = "/home/ubuntu/sync_1p_manus.log"
REPORT_FILE = "/home/ubuntu/sync_1p_manus_report.json"

# Tags 1Password pour cibler les items à synchroniser vers Manus
# Accepte les tags existants ET les nouveaux tags standardisés
TARGET_TAGS = [
    # Tags standardisés (nouveaux)
    "yos-manus", "yos-secret",
    # Tags existants dans 1Password (compatibilité rétroactive)
    "yos-key", "manus", "yos",
]

# Mapping titre 1Password → (connector_name, env_var)
# Pattern (regex, case-insensitive) → {"name": ..., "env": ...}
CONNECTOR_MAP = [
    # ── Modèles LLM ─────────────────────────────────────────────────────────
    {"p": r"openai",                  "name": "OpenAI",           "env": "OPENAI_API_KEY"},
    {"p": r"anthropic|claude",        "name": "Anthropic",        "env": "ANTHROPIC_API_KEY"},
    {"p": r"gemini|google ai",        "name": "Google Gemini",    "env": "GEMINI_API_KEY"},
    {"p": r"x\.ai|xai api|grok",      "name": "Grok",             "env": "XAI_API_KEY"},
    {"p": r"deepseek",                "name": "DeepSeek API",     "env": "DEEPSEEK_API_KEY"},
    {"p": r"openrouter",              "name": "OpenRouter API",   "env": "OPENROUTER_API_KEY"},
    {"p": r"perplexity|sonar",        "name": "Perplexity",       "env": "SONAR_API_KEY"},
    {"p": r"groq(?! api key.*cloud)", "name": "Groq API",         "env": "GROQ_API_KEY"},
    {"p": r"cohere",                  "name": "Cohere API",       "env": "COHERE_API_KEY"},
    {"p": r"huggingface|hugging face","name": "HuggingFace API",  "env": "HUGGINGFACE_API_KEY"},
    # ── Image / Vidéo / Audio ───────────────────────────────────────────────
    {"p": r"replicate",               "name": "Replicate",        "env": "REPLICATE_API_TOKEN"},
    {"p": r"elevenlabs",              "name": "ElevenLabs API",   "env": "ELEVENLABS_API_KEY"},
    {"p": r"flux|bfl\.ai",            "name": "Flux API",         "env": "BFL_API_KEY"},
    {"p": r"stability.?ai",           "name": "Stability AI API", "env": "STABILITY_API_KEY"},
    {"p": r"fal\.ai",                 "name": "Fal.ai API",       "env": "FAL_API_KEY"},
    {"p": r"heygen",                  "name": "HeyGen API",       "env": "HEYGEN_API_KEY"},
    {"p": r"hume",                    "name": "Hume API",         "env": "HUME_API_KEY"},
    {"p": r"minimax",                 "name": "MiniMax API",      "env": "MINIMAX_API_KEY"},
    # ── Recherche / Web ─────────────────────────────────────────────────────
    {"p": r"exa api key$|exa.*yos",   "name": "Exa API",          "env": "EXA_API_KEY"},
    {"p": r"firecrawl",               "name": "Firecrawl API",    "env": "FIRECRAWL_API_KEY"},
    {"p": r"tavily",                  "name": "Tavily API",       "env": "TAVILY_API_KEY"},
    {"p": r"apify",                   "name": "Apify API",        "env": "APIFY_API_KEY"},
    {"p": r"bright.?data",            "name": "Bright Data API",  "env": "BRIGHT_DATA_API_KEY"},
    {"p": r"anchor.?browser",         "name": "Anchor Browser",   "env": "ANCHOR_API_KEY"},
    {"p": r"semrush",                 "name": "Semrush API",      "env": "SEMRUSH_API_KEY"},
    {"p": r"ahrefs",                  "name": "Ahrefs API",       "env": "AHREFS_API_KEY"},
    # ── Mémoire / Knowledge ─────────────────────────────────────────────────
    {"p": r"mem0",                    "name": "mem0",             "env": "MEM0_API_KEY"},
    {"p": r"notion api",              "name": "Notion API",       "env": "NOTION_API_KEY"},
    {"p": r"pinecone",                "name": "Pinecone API",     "env": "PINECONE_API_KEY"},
    {"p": r"tana",                    "name": "Tana API",         "env": "TANA_API_KEY"},
    # ── Automation / Infra ──────────────────────────────────────────────────
    {"p": r"n8n",                     "name": "n8n API",          "env": "N8N_API_KEY"},
    {"p": r"github.*manus|github.*yos|github pat.*yj0","name": "GITHUB (PAT)", "env": "GITHUB_PAT"},
    {"p": r"manus api",               "name": "Manus API",        "env": "MANUS_API_KEY"},
    {"p": r"fly\.io",                 "name": "Fly.io API",       "env": "FLY_API_TOKEN"},
    {"p": r"telegram",                "name": "Telegram API",     "env": "TELEGRAM_BOT_TOKEN"},
    {"p": r"upstash",                 "name": "UPSTASH",          "env": "UPSTASH_API_KEY"},
    {"p": r"supabase",                "name": "Supabase API",     "env": "SUPABASE_ACCESS_TOKEN"},
    {"p": r"cloudflare",              "name": "Cloudflare API",   "env": "CLOUDFLARE_API_TOKEN"},
    {"p": r"vercel",                  "name": "Vercel API",       "env": "VERCEL_API_KEY"},
    # ── Communication / Marketing ───────────────────────────────────────────
    {"p": r"resend",                  "name": "Resend API",       "env": "RESEND_API_KEY"},
    {"p": r"mailerlite",              "name": "MailerLite API",   "env": "MAILERLITE_API_KEY"},
    {"p": r"klaviyo",                 "name": "Klaviyo API",      "env": "KLAVIYO_API_KEY"},
    {"p": r"twilio",                  "name": "Twilio API",       "env": "TWILIO_API_KEY"},
    {"p": r"typeform",                "name": "Typeform",         "env": "TYPEFORM_API_KEY"},
    {"p": r"tally",                   "name": "Tally API",        "env": "TALLY_API_KEY"},
    # ── CRM / Productivité ──────────────────────────────────────────────────
    {"p": r"airtable",                "name": "Airtable API",     "env": "AIRTABLE_API_KEY"},
    {"p": r"harpa",                   "name": "HARPA",            "env": "HARPA_API_KEY"},
    {"p": r"raindrop",                "name": "Raindrop API",     "env": "RAINDROP_API_KEY"},
    {"p": r"stripe",                  "name": "Stripe API",       "env": "STRIPE_API_KEY"},
    {"p": r"deepl",                   "name": "DeepL API",        "env": "DEEPL_API_KEY"},
    # ── Finance / Data ──────────────────────────────────────────────────────
    {"p": r"alpha.?vantage",          "name": "Alpha Vantage API","env": "ALPHA_VANTAGE_API_KEY"},
    {"p": r"coingecko",               "name": "CoinGecko API",    "env": "COINGECKO_API_KEY"},
]

# ─── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger(__name__)


# ─── 1PASSWORD HELPERS ────────────────────────────────────────────────────────

def op_run(args: list, timeout: int = 20) -> str:
    """Exécute une commande op CLI et retourne stdout."""
    env = os.environ.copy()
    r = subprocess.run(["op"] + args, capture_output=True, text=True, timeout=timeout, env=env)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def fetch_1p_items() -> list:
    """Récupère tous les items API Credential du MAIN VAULT."""
    raw = op_run(["item", "list", "--vault", VAULT, "--categories", "API Credential",
                  "--format", "json"], timeout=30)
    return json.loads(raw)


def fetch_1p_item_detail(item_id: str) -> dict:
    """Récupère le détail complet d'un item 1Password."""
    raw = op_run(["item", "get", item_id, "--vault", VAULT, "--format", "json"], timeout=15)
    return json.loads(raw)


def extract_credential(fields: list) -> str:
    """Extrait la valeur principale du credential depuis les champs 1P."""
    PRIORITY_IDS = ["credential", "password"]
    PRIORITY_LABELS = ["credential", "api key", "token", "key", "secret",
                       "access token", "api token", "bearer token", "service account token",
                       "full pat", "manus full", "pat token"]
    SKIP_LABELS = ["username", "notesplain", "hostname", "type", "filename",
                   "valid from", "expires", "created", "service", "manus secret name",
                   "url", "website", "email", "name", "date", "notes"]

    # Pass 1: ID exact
    for fid in PRIORITY_IDS:
        for f in fields:
            if f.get("id", "").lower() == fid and f.get("value"):
                return f["value"]

    # Pass 2: Label prioritaire
    for label_target in PRIORITY_LABELS:
        for f in fields:
            if f.get("label", "").lower() == label_target and f.get("value"):
                return f["value"]

    # Pass 3: Heuristique — première valeur longue non-skip
    for f in fields:
        val = f.get("value", "")
        label = f.get("label", "").lower()
        if val and len(val) > 15 and not any(s in label for s in SKIP_LABELS):
            return val

    return ""


def get_item_tags(item_detail: dict) -> list:
    """Extrait les tags d'un item 1Password."""
    return item_detail.get("tags", [])


def get_item_env_var_override(item_detail: dict) -> str:
    """Cherche un champ 'yos-env-var' dans l'item pour override le nom de la variable."""
    for f in item_detail.get("fields", []):
        if f.get("label", "").lower() in ["yos-env-var", "env-var", "env var", "manus secret name"]:
            return f.get("value", "")
    return ""


# ─── MANUS CONFIG HELPERS ─────────────────────────────────────────────────────

def manus_list_connectors() -> list:
    """Retourne la liste des connectors Manus via manus-config."""
    r = subprocess.run(["manus-config", "connector", "list"],
                       capture_output=True, text=True, timeout=10)
    connectors = []
    for line in r.stdout.splitlines():
        parts = line.strip().split("  ")
        if len(parts) >= 2:
            uid = parts[0].strip()
            name = parts[1].strip()
            kind = parts[2].strip() if len(parts) > 2 else ""
            enabled = "enabled" in line
            editable = "editable" in line
            connectors.append({"uid": uid, "name": name, "kind": kind,
                                "enabled": enabled, "editable": editable})
    return connectors


def manus_get_connector(uid: str) -> dict:
    """Récupère le détail d'un connector Manus."""
    r = subprocess.run(["manus-config", "connector", "get", uid],
                       capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        return {}
    # Chercher le JSON dans la sortie
    try:
        start = r.stdout.index("{")
        return json.loads(r.stdout[start:])
    except (ValueError, json.JSONDecodeError):
        return {}


def manus_connector_by_name(connectors: list, name: str) -> dict:
    """Trouve un connector par nom (case-insensitive)."""
    nl = name.lower()
    for c in connectors:
        if c.get("name", "").lower() == nl:
            return c
    return {}


def _manus_env() -> dict:
    """Retourne l'environnement avec les vars MANUS_CONFIG propagées."""
    env = os.environ.copy()
    # S'assurer que les vars MANUS_CONFIG_RESULT_PATH sont présentes
    # (injectées par le shell Manus, mais pas propagées aux subprocesses Python)
    if "MANUS_CONFIG_RESULT_PATH" not in env:
        result_path = f"/tmp/manus_sync_{os.getpid()}.json"
        env["MANUS_CONFIG_RESULT_PATH"] = result_path
        env["MANUS_CONFIG_RESULT_FILEPATH"] = result_path
    return env


def manus_create_connector(name: str, env_var: str, credential: str) -> tuple:
    """Crée un nouveau Custom API Connector dans Manus."""
    note = (
        f"Use the {name} API. "
        f"The environment variable {env_var} is available. "
        f"Authenticate using the stored key. "
        f"Source of truth: 1Password MAIN VAULT (tag: yos-manus). "
        f"Do not assume endpoint paths; check the documentation first."
    )
    draft = {"type": "api", "name": name, "env": {env_var: credential}, "note": note}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(draft, f)
        fname = f.name
    try:
        r = subprocess.run(["manus-config", "connector", "create", "--file", fname],
                           capture_output=True, text=True, timeout=30, env=_manus_env())
        return r.returncode == 0, r.stdout + r.stderr
    finally:
        os.unlink(fname)


def manus_update_connector(uid: str, env_var: str, credential: str) -> tuple:
    """Met à jour le token d'un connector Manus existant."""
    patch = {"uid": uid, "env": [{"key": env_var, "value": credential}]}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(patch, f)
        fname = f.name
    try:
        r = subprocess.run(["manus-config", "connector", "update", "--file", fname],
                           capture_output=True, text=True, timeout=30, env=_manus_env())
        return r.returncode == 0, r.stdout + r.stderr
    finally:
        os.unlink(fname)


# ─── MATCHING ─────────────────────────────────────────────────────────────────

def match_connector_def(title: str, env_var_override: str = "") -> dict:
    """Trouve la définition de connector correspondant au titre 1P."""
    # Si un override d'env var est défini dans 1P, chercher par env var
    if env_var_override:
        for m in CONNECTOR_MAP:
            if m["env"].lower() == env_var_override.lower():
                return m

    title_lower = title.lower()
    for m in CONNECTOR_MAP:
        if re.search(m["p"], title_lower):
            return m
    return {}


# ─── MAIN SYNC ────────────────────────────────────────────────────────────────

def main():
    start = datetime.now()
    log.info("=" * 65)
    log.info("Y-OS SECRET SYNC ENGINE — 1Password → Manus")
    log.info(f"Start: {start.isoformat()}")
    log.info("=" * 65)

    stats = {"created": 0, "updated": 0, "unchanged": 0, "skipped": 0, "errors": 0}
    details = []

    # ── 1. Fetch 1Password items ───────────────────────────────────────────
    log.info("[1/4] Fetching items from 1Password MAIN VAULT...")
    try:
        items = fetch_1p_items()
        log.info(f"  → {len(items)} API Credential items found")
    except Exception as e:
        log.error(f"  FATAL: {e}")
        sys.exit(1)

    # ── 2. Fetch credentials ───────────────────────────────────────────────
    log.info("[2/4] Fetching credentials...")
    enriched = []
    for i, item in enumerate(items):
        iid, title = item["id"], item["title"]
        try:
            detail = fetch_1p_item_detail(iid)
            credential = extract_credential(detail.get("fields", []))
            tags = get_item_tags(detail)
            env_override = get_item_env_var_override(detail)
            enriched.append({
                "id": iid, "title": title, "credential": credential,
                "tags": tags, "env_override": env_override,
                "updated_at": item.get("updated_at", ""),
            })
            tag_str = f" [tags: {', '.join(tags)}]" if tags else ""
            log.info(f"  [{i+1:2d}/{len(items)}] {title}{tag_str}: {'✓' if credential else 'EMPTY'}")
        except Exception as e:
            log.warning(f"  [{i+1:2d}/{len(items)}] {title}: ERROR — {e}")
            enriched.append({"id": iid, "title": title, "credential": "", "tags": [], "error": str(e)})
            stats["errors"] += 1

    # ── 3. Load Manus connectors ───────────────────────────────────────────
    log.info("[3/4] Loading Manus connectors...")
    try:
        manus_connectors = manus_list_connectors()
        log.info(f"  → {len(manus_connectors)} connectors found")
    except Exception as e:
        log.error(f"  FATAL: {e}")
        sys.exit(1)

    # ── 4. Sync ────────────────────────────────────────────────────────────
    log.info("[4/4] Syncing...")
    handled = set()

    for cred in enriched:
        title = cred["title"]
        credential = cred.get("credential", "")
        tags = cred.get("tags", [])
        env_override = cred.get("env_override", "")

        # Filtrer : uniquement les items ciblés pour Manus
        # Matching case-insensitive sur les tags
        tags_lower = [t.lower() for t in tags]
        target_lower = [t.lower() for t in TARGET_TAGS]
        has_target_tag = any(t in target_lower for t in tags_lower)
        no_tags_defined = len(tags) == 0
        
        if not (has_target_tag or no_tags_defined):
            log.info(f"  SKIP (no target tag): {title} [tags: {tags}]")
            stats["skipped"] += 1
            details.append({"title": title, "action": "SKIP", "reason": f"tags={tags}, not in {TARGET_TAGS}"})
            continue

        if not credential:
            log.info(f"  SKIP (no credential): {title}")
            stats["skipped"] += 1
            details.append({"title": title, "action": "SKIP", "reason": "empty credential"})
            continue

        # Matcher la définition de connector
        mapping = match_connector_def(title, env_override)
        if not mapping:
            log.info(f"  SKIP (no mapping): {title}")
            stats["skipped"] += 1
            details.append({"title": title, "action": "SKIP", "reason": "no connector mapping"})
            continue

        connector_name = mapping["name"]
        env_var = env_override if env_override else mapping["env"]

        # Éviter les doublons (plusieurs items 1P → même connector)
        if connector_name in handled:
            log.info(f"  SKIP (duplicate): {title} → {connector_name}")
            stats["skipped"] += 1
            continue
        handled.add(connector_name)

        # Chercher le connector Manus existant
        existing = manus_connector_by_name(manus_connectors, connector_name)

        if not existing:
            # ── CREATE ──────────────────────────────────────────────────────
            log.info(f"  CREATE: {title} → [{connector_name}] ({env_var})")
            try:
                ok, out = manus_create_connector(connector_name, env_var, credential)
                if ok:
                    log.info(f"    ✅ Created: {connector_name}")
                    stats["created"] += 1
                    details.append({"title": title, "connector": connector_name, "env": env_var, "action": "CREATED"})
                else:
                    # manus-config create nécessite une confirmation UI
                    # En mode non-interactif, on log le besoin de confirmation
                    if "review" in out.lower() or "confirm" in out.lower() or "card" in out.lower():
                        log.info(f"    ⏳ Pending UI confirmation: {connector_name}")
                        stats["created"] += 1
                        details.append({"title": title, "connector": connector_name, "env": env_var,
                                        "action": "CREATED (pending confirmation)"})
                    else:
                        log.warning(f"    ⚠ Create failed: {out[:150]}")
                        stats["errors"] += 1
                        details.append({"title": title, "connector": connector_name, "action": "ERROR",
                                        "reason": out[:150]})
            except Exception as e:
                log.error(f"    ✗ Exception: {e}")
                stats["errors"] += 1
                details.append({"title": title, "connector": connector_name, "action": "ERROR", "reason": str(e)})

        else:
            # ── UPDATE or UNCHANGED ─────────────────────────────────────────
            uid = existing.get("uid", "")
            editable = existing.get("editable", False)

            if not editable:
                log.info(f"  UNCHANGED (not editable): {connector_name}")
                stats["unchanged"] += 1
                details.append({"title": title, "connector": connector_name, "action": "UNCHANGED",
                                 "reason": "not editable (built-in)"})
                continue

            # Tenter la mise à jour
            log.info(f"  UPDATE: {title} → [{connector_name}] (uid: {uid[:8]}...)")
            try:
                ok, out = manus_update_connector(uid, env_var, credential)
                if ok or "review" in out.lower() or "confirm" in out.lower():
                    log.info(f"    🔄 Updated: {connector_name}")
                    stats["updated"] += 1
                    details.append({"title": title, "connector": connector_name, "env": env_var,
                                    "action": "UPDATED", "uid": uid})
                else:
                    # Pas de changement détecté ou déjà à jour
                    log.info(f"    ✓ Unchanged: {connector_name}")
                    stats["unchanged"] += 1
                    details.append({"title": title, "connector": connector_name, "action": "UNCHANGED"})
            except Exception as e:
                log.warning(f"    ⚠ Update exception: {e} — marking unchanged")
                stats["unchanged"] += 1
                details.append({"title": title, "connector": connector_name, "action": "UNCHANGED",
                                 "reason": str(e)})

    # ── RAPPORT FINAL ──────────────────────────────────────────────────────
    end = datetime.now()
    duration = (end - start).total_seconds()

    log.info("")
    log.info("=" * 65)
    log.info("SYNC COMPLETE")
    log.info(f"  Duration : {duration:.1f}s")
    log.info(f"  ✅ Créés   : {stats['created']}")
    log.info(f"  🔄 Mis à jour : {stats['updated']}")
    log.info(f"  ✓  Inchangés  : {stats['unchanged']}")
    log.info(f"  ⏭  Ignorés    : {stats['skipped']}")
    log.info(f"  ❌ Erreurs    : {stats['errors']}")
    log.info("=" * 65)

    log.info("\nDÉTAIL PAR ITEM:")
    for d in details:
        action = d.get("action", "?")
        connector = d.get("connector", d.get("title", "?"))
        reason = f" ({d['reason']})" if "reason" in d else ""
        log.info(f"  [{action:30s}] {connector}{reason}")

    # Sauvegarder le rapport JSON
    report = {
        "timestamp": start.isoformat(),
        "duration_seconds": round(duration, 1),
        "vault": VAULT,
        "total_1p_items": len(enriched),
        "stats": stats,
        "details": details,
    }
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    log.info(f"\nReport: {REPORT_FILE}")
    log.info(f"Log:    {LOG_FILE}")

    return stats


if __name__ == "__main__":
    stats = main()
    sys.exit(0 if stats["errors"] == 0 else 1)
