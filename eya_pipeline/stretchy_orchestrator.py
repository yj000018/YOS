"""
eYa AutoLive2D — Stretchy Studio Orchestrator
Module 1 : DOM Cache + Pipeline automatique

Principe :
- Versionne le DOM de Stretchy Studio (v0.2)
- Rejoue le flux exact sans redécouverte
- Si version change → réanalyse DOM automatique
- Stocke les paramètres optimaux dans stretchy_config.json
"""

import json
import time
import os
import hashlib
import subprocess
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "stretchy_config.json"
DOM_CACHE_PATH = Path(__file__).parent / "stretchy_dom_cache.json"

DEFAULT_CONFIG = {
    "stretchy_version": "0.2",
    "stretchy_url": "http://localhost:8771",
    "params": {
        "mesh_all_parts": True,
        "rigging_method": "heuristic",   # "heuristic" | "dwpose"
        "dwpose_model_path": "/opt/yos/models/dw-ll_ucoco_384.onnx",
        "export_formats": ["stretch", "live2d_json"],  # les deux
        "animation_preset": "idle",
    },
    "export": {
        "stretch_path": "/home/ubuntu/eya_pipeline/output/eya.stretch",
        "live2d_json_path": "/home/ubuntu/eya_pipeline/output/eya_live2d.json",
    }
}

# ─────────────────────────────────────────────
# DOM FLOW CACHE — Stretchy Studio v0.2
# ─────────────────────────────────────────────
# Chaque step = action exacte à rejouer sans redécouverte DOM

DOM_FLOW_V02 = {
    "version": "0.2",
    "fingerprint_selector": "div#root",  # pour vérifier la version
    "fingerprint_text": "Stretchy Studio v0.2",
    "steps": [
        {
            "id": "load_psd",
            "description": "Injecter le PSD dans l'input file caché",
            "method": "inject_file",
            "selector": "input[type='file']",
            "file_url": "/eya_correct.psd",
            "wait_after": 2.0,
        },
        {
            "id": "click_continue",
            "description": "Valider le mapping des layers",
            "method": "click_by_text",
            "text": "Continue",
            "wait_after": 1.5,
        },
        {
            "id": "click_next_reorder",
            "description": "Passer à l'étape Reorder Layers",
            "method": "click_by_text",
            "text": "Next: Adjust Joints →",
            "wait_after": 2.0,
        },
        {
            "id": "click_next_params",
            "description": "Passer à Setup Parameters (rig heuristique validé)",
            "method": "click_by_text",
            "text": "Next: Setup Parameters →",
            "wait_after": 3.0,
        },
        {
            "id": "click_done",
            "description": "Finaliser le rig",
            "method": "click_by_text",
            "text": "Done",
            "wait_after": 2.0,
        },
    ],
    "dwpose_steps": [
        # Étapes supplémentaires si rigging_method == "dwpose"
        {
            "id": "inject_dwpose_model",
            "description": "Injecter le modèle ONNX DWPose",
            "method": "inject_file",
            "selector": "input[accept='.onnx']",
            "file_path": "/opt/yos/models/dw-ll_ucoco_384.onnx",
            "wait_after": 5.0,
        },
        {
            "id": "wait_dwpose_build",
            "description": "Attendre la fin du build DWPose (CPU ~5-10 min)",
            "method": "wait_for_text_gone",
            "text": "Building rig…",
            "timeout": 600,  # 10 min max
            "poll_interval": 10,
        },
    ]
}

# ─────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[CONFIG] Saved to {CONFIG_PATH}")

def load_dom_cache() -> Optional[dict]:
    if DOM_CACHE_PATH.exists():
        with open(DOM_CACHE_PATH) as f:
            return json.load(f)
    return None

def save_dom_cache(cache: dict):
    with open(DOM_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)
    print(f"[DOM CACHE] Saved to {DOM_CACHE_PATH}")

def get_stretchy_version(page_text: str) -> Optional[str]:
    """Extrait la version de Stretchy Studio depuis le texte de la page."""
    import re
    match = re.search(r"Stretchy Studio\s+v([\d.]+)", page_text)
    return match.group(1) if match else None

def check_version_match(current_version: str, cached_version: str) -> bool:
    return current_version == cached_version

# ─────────────────────────────────────────────
# ORCHESTRATEUR PRINCIPAL
# ─────────────────────────────────────────────

class StretchyOrchestrator:
    """
    Orchestre le pipeline Stretchy Studio de façon déterministe.
    
    Usage:
        orch = StretchyOrchestrator()
        orch.run_full_pipeline(psd_path="/home/ubuntu/stretchy-studio/public/eya_correct.psd")
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config = load_config()
        self.dom_flow = DOM_FLOW_V02
        self.base_url = self.config["stretchy_url"]
        self.log = []

    def _log(self, step_id: str, status: str, detail: str = ""):
        entry = {"step": step_id, "status": status, "detail": detail, "ts": time.time()}
        self.log.append(entry)
        icon = "✅" if status == "ok" else "❌" if status == "error" else "⏳"
        print(f"  {icon} [{step_id}] {detail or status}")

    def generate_js_for_step(self, step: dict) -> str:
        """Génère le JavaScript à exécuter dans le browser pour chaque step."""
        method = step["method"]

        if method == "inject_file":
            file_url = step.get("file_url", "")
            file_path = step.get("file_path", "")
            selector = step["selector"]
            accept = step.get("accept", "")

            if file_url:
                return f"""
(async () => {{
  const resp = await fetch('{file_url}');
  const blob = await resp.blob();
  const fname = '{file_url}'.split('/').pop();
  const file = new File([blob], fname, {{ type: 'application/octet-stream' }});
  const input = document.querySelector("{selector}");
  if (!input) {{ console.error('INPUT NOT FOUND: {selector}'); return; }}
  const dt = new DataTransfer();
  dt.items.add(file);
  Object.defineProperty(input, 'files', {{ value: dt.files, writable: false }});
  input.dispatchEvent(new Event('change', {{ bubbles: true }}));
  console.log('FILE INJECTED:', fname, file.size, 'bytes');
}})();
"""
            else:
                # Fichier local — doit être servi via HTTP
                fname = Path(file_path).name
                return f"""
(async () => {{
  const resp = await fetch('/{fname}');
  const blob = await resp.blob();
  const file = new File([blob], '{fname}', {{ type: 'application/octet-stream' }});
  const input = document.querySelector("{selector}");
  if (!input) {{ console.error('INPUT NOT FOUND: {selector}'); return; }}
  const dt = new DataTransfer();
  dt.items.add(file);
  Object.defineProperty(input, 'files', {{ value: dt.files, writable: false }});
  input.dispatchEvent(new Event('change', {{ bubbles: true }}));
  console.log('FILE INJECTED:', '{fname}', file.size, 'bytes');
}})();
"""

        elif method == "click_by_text":
            text = step["text"]
            return f"""
const btns = Array.from(document.querySelectorAll('button'));
const btn = btns.find(b => b.textContent.includes('{text}'));
if (btn) {{
  btn.click();
  console.log('CLICKED:', '{text}');
}} else {{
  console.error('BUTTON NOT FOUND: {text}');
  console.log('Available buttons:', btns.map(b => b.textContent.trim()).join(' | '));
}}
"""

        elif method == "wait_for_text_gone":
            text = step["text"]
            timeout = step.get("timeout", 300)
            poll = step.get("poll_interval", 10)
            return f"""
// Polling: attendre que '{text}' disparaisse
// Timeout: {timeout}s — à implémenter côté Python avec polling
console.log('WAITING FOR TEXT GONE: {text}');
"""

        return "console.log('UNKNOWN METHOD');"

    def get_flow(self) -> list:
        """Retourne le flux complet selon la méthode de rigging configurée."""
        steps = list(self.dom_flow["steps"])
        if self.config["params"]["rigging_method"] == "dwpose":
            # Insérer les étapes DWPose avant "click_next_params"
            insert_idx = next(
                (i for i, s in enumerate(steps) if s["id"] == "click_next_params"), 
                len(steps)
            )
            for dwstep in reversed(self.dom_flow["dwpose_steps"]):
                steps.insert(insert_idx, dwstep)
        return steps

    def print_pipeline_summary(self):
        """Affiche un résumé du pipeline configuré."""
        config = self.config
        flow = self.get_flow()
        print("\n" + "="*60)
        print("  eYa AutoLive2D — Pipeline Stretchy Studio")
        print("="*60)
        print(f"  Version DOM : {self.dom_flow['version']}")
        print(f"  URL         : {self.base_url}")
        print(f"  Rigging     : {config['params']['rigging_method']}")
        print(f"  Export      : {', '.join(config['params']['export_formats'])}")
        print(f"  Steps       : {len(flow)}")
        print("-"*60)
        for i, step in enumerate(flow, 1):
            print(f"  {i:2d}. [{step['id']}] {step['description']}")
        print("="*60 + "\n")

    def generate_full_js_script(self) -> str:
        """Génère le script JS complet pour automatiser tout le wizard."""
        flow = self.get_flow()
        parts = [
            "// eYa AutoLive2D — Stretchy Studio Full Pipeline Script",
            f"// Version: {self.dom_flow['version']}",
            f"// Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "(async () => {",
            "  const sleep = ms => new Promise(r => setTimeout(r, ms));",
            "",
        ]

        for step in flow:
            parts.append(f"  // ── Step: {step['id']} ──────────────────────────")
            step_id = step['id']
            parts.append(f"  console.log('STEP: {step_id}');")

            js = self.generate_js_for_step(step)
            # Indent the JS
            for line in js.strip().split('\n'):
                parts.append(f"  {line}")

            wait = step.get("wait_after", 1.0)
            parts.append(f"  await sleep({int(wait * 1000)});")
            parts.append("")

        parts.append("  console.log('PIPELINE COMPLETE');")
        parts.append("})();")

        return "\n".join(parts)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    orch = StretchyOrchestrator()
    orch.print_pipeline_summary()

    # Générer et sauvegarder le script JS
    js_script = orch.generate_full_js_script()
    js_path = Path(__file__).parent / "stretchy_pipeline.js"
    with open(js_path, "w") as f:
        f.write(js_script)
    print(f"[JS] Script saved to {js_path}")

    # Sauvegarder la config
    save_config(orch.config)
    print(f"[CONFIG] Config saved to {CONFIG_PATH}")

    # Sauvegarder le DOM cache
    save_dom_cache({
        "version": DOM_FLOW_V02["version"],
        "fingerprint": DOM_FLOW_V02["fingerprint_text"],
        "flow_hash": hashlib.md5(json.dumps(DOM_FLOW_V02["steps"]).encode()).hexdigest(),
        "saved_at": time.strftime('%Y-%m-%d %H:%M:%S'),
    })
    print(f"[DOM CACHE] Cache saved to {DOM_CACHE_PATH}")
