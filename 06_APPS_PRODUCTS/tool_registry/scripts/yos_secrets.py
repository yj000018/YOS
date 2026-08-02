#!/usr/bin/env python3
"""
Y-OS Secret Management Module

Fournit une interface unifiée pour récupérer les secrets dans Y-OS.
Implémente le pattern "Local Mirror with Lazy Fetch Fallback" :
1. Cherche dans l'environnement local (Miroir Manus/JGPT).
2. Si introuvable, va chercher dans 1Password (SSOT).
3. (Optionnel) Déclenche une mise à jour du miroir.
"""

import os
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("yos_secrets")

VAULT = "MAIN VAULT"

def _fetch_from_1password(secret_name: str) -> str:
    """
    Tente de récupérer un secret depuis 1Password via op CLI.
    Recherche par titre d'item ou par ID.
    """
    log.info(f"Fallback: Fetching '{secret_name}' from 1Password...")
    try:
        # Chercher l'item par nom
        env = os.environ.copy()
        result = subprocess.run(
            ["op", "item", "get", secret_name, "--vault", VAULT, "--format", "json"],
            capture_output=True, text=True, timeout=15, env=env
        )
        
        if result.returncode != 0:
            log.warning(f"1Password item '{secret_name}' not found or error: {result.stderr.strip()}")
            return ""
            
        detail = json.loads(result.stdout)
        
        # Extraire le credential
        for f in detail.get("fields", []):
            fid = f.get("id", "").lower()
            label = f.get("label", "").lower()
            if fid in ["credential", "password"] or label in ["credential", "api key", "token", "key"]:
                val = f.get("value")
                if val:
                    return val
                    
        log.warning(f"Item '{secret_name}' found in 1P, but no credential field identified.")
        return ""
        
    except Exception as e:
        log.error(f"Error fetching from 1Password: {e}")
        return ""

def get_secret(env_var_name: str, op_item_name: str = None) -> str:
    """
    Récupère un secret avec le mécanisme de fallback.
    
    Args:
        env_var_name: Le nom de la variable d'environnement (ex: 'OPENAI_API_KEY')
        op_item_name: Le titre de l'item dans 1Password (ex: 'OpenAI API Key'). 
                      Si None, utilise env_var_name.
                      
    Returns:
        La valeur du secret, ou une chaîne vide si introuvable.
    """
    # 1. Local Mirror (Environment Variable)
    val = os.environ.get(env_var_name)
    if val:
        log.debug(f"Secret '{env_var_name}' found in local mirror (env).")
        return val
        
    # 2. Fallback to 1Password
    target_name = op_item_name if op_item_name else env_var_name
    val = _fetch_from_1password(target_name)
    
    if val:
        log.info(f"Secret '{env_var_name}' successfully fetched from 1Password fallback.")
        # Mettre à jour l'environnement courant pour les appels subséquents
        os.environ[env_var_name] = val
        
        # TODO: Implémenter l'appel asynchrone vers manus-config pour mettre à jour le miroir persistant
        # _trigger_mirror_update_async(env_var_name, target_name)
        
        return val
        
    log.error(f"CRITICAL: Secret '{env_var_name}' not found in mirror OR 1Password.")
    return ""

if __name__ == "__main__":
    # Test simple
    print("Testing Y-OS Secret Fallback Mechanism...")
    
    # Test 1: Env var existe
    os.environ["TEST_SECRET"] = "local_mirror_value"
    val1 = get_secret("TEST_SECRET")
    print(f"Test 1 (Local): {val1}")
    
    # Test 2: Fallback 1Password
    # On utilise un item connu pour tester (Exa)
    val2 = get_secret("EXA_API_KEY", "EXA API Key")
    preview = val2[:10] + "..." if val2 else "FAILED"
    print(f"Test 2 (Fallback 1P): {preview}")
