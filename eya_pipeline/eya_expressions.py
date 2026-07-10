#!/usr/bin/env python3
"""
eya_expressions.py — eYa Live2D expression library + animate(prompt) function

41 paramètres disponibles dans le .stretch eYa :
  ParamAngleX/Y/Z       : rotation tête (-30/+30)
  ParamEyeLOpen/ROpen   : ouverture œil (0=fermé, 1=ouvert)
  ParamEyeLSmile/RSmile : plissement souriant (0-1)
  ParamEyeBallX/Y       : direction regard (-1/+1)
  ParamEyeBallForm      : forme pupille (-1/+1)
  ParamTear             : larmes (0-2)
  ParamBrowLY/RY        : hauteur sourcil (-1/+1)
  ParamBrowLX/RX        : position horizontale sourcil
  ParamBrowLAngle/RAngle: angle sourcil (-1/+1)
  ParamBrowLForm/RForm  : forme sourcil (-1/+1)
  ParamMouthForm        : forme bouche (-1=triste, 0=neutre, 1=sourire)
  ParamMouthOpenY       : ouverture bouche (0-1)
  ParamBodyAngleX/Y/Z   : rotation corps (-10/+10)
  ParamBreath           : respiration (0-1)
  ParamCheek            : rougeur joues (0-1)
  ParamHairFront/Side/Back/Fluffy : cheveux
  ParamArmLA/RA/LB/RB   : bras
  ParamHandL/R          : mains
  ParamShoulderY        : épaules
  ParamBustX/Y          : buste
  ParamBaseX/Y          : position globale

Usage:
    from eya_expressions import animate, apply_expression, EXPRESSIONS

    # Appliquer une expression nommée
    params = EXPRESSIONS["smile"]

    # Générer depuis un prompt
    params, keyframes = animate("eYa sourit doucement et cligne des yeux")

    # Injecter dans le .stretch
    apply_to_stretch("eya_heuristic.stretch", params, keyframes, "eya_smile.stretch")
"""

import json
import zipfile
import shutil
import math
import random
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ─────────────────────────────────────────────────────────────
# 1. PARAMÈTRE PAR DÉFAUT (pose neutre)
# ─────────────────────────────────────────────────────────────
NEUTRAL = {
    "ParamAngleX": 0, "ParamAngleY": 0, "ParamAngleZ": 0,
    "ParamEyeLOpen": 1, "ParamEyeROpen": 1,
    "ParamEyeLSmile": 0, "ParamEyeRSmile": 0,
    "ParamEyeBallX": 0, "ParamEyeBallY": 0, "ParamEyeBallForm": 0,
    "ParamTear": 0,
    "ParamBrowLY": 0, "ParamBrowRY": 0,
    "ParamBrowLX": 0, "ParamBrowRX": 0,
    "ParamBrowLAngle": 0, "ParamBrowRAngle": 0,
    "ParamBrowLForm": 0, "ParamBrowRForm": 0,
    "ParamMouthForm": 0, "ParamMouthOpenY": 0,
    "ParamBodyAngleX": 0, "ParamBodyAngleY": 0, "ParamBodyAngleZ": 0,
    "ParamBreath": 0,
    "ParamCheek": 0,
    "ParamHairFront": 0, "ParamHairSide": 0, "ParamHairBack": 0, "ParamHairFluffy": 0,
    "ParamArmLA": 0, "ParamArmRA": 0, "ParamArmLB": 0, "ParamArmRB": 0,
    "ParamHandL": 0, "ParamHandR": 0,
    "ParamShoulderY": 0,
    "ParamBustX": 0, "ParamBustY": 0,
    "ParamBaseX": 0, "ParamBaseY": 0,
}

# ─────────────────────────────────────────────────────────────
# 2. LES 10 EXPRESSIONS DE BASE
# ─────────────────────────────────────────────────────────────
EXPRESSIONS = {

    # 1. SMILE — sourire doux et naturel
    "smile": {
        **NEUTRAL,
        "ParamMouthForm": 0.75,
        "ParamEyeLSmile": 0.4,
        "ParamEyeRSmile": 0.4,
        "ParamEyeLOpen": 0.85,
        "ParamEyeROpen": 0.85,
        "ParamBrowLY": 0.1,
        "ParamBrowRY": 0.1,
        "ParamCheek": 0.3,
    },

    # 2. BIG_SMILE — grand sourire expressif
    "big_smile": {
        **NEUTRAL,
        "ParamMouthForm": 1.0,
        "ParamMouthOpenY": 0.3,
        "ParamEyeLSmile": 0.8,
        "ParamEyeRSmile": 0.8,
        "ParamEyeLOpen": 0.7,
        "ParamEyeROpen": 0.7,
        "ParamBrowLY": 0.2,
        "ParamBrowRY": 0.2,
        "ParamCheek": 0.6,
        "ParamBodyAngleY": 2,
    },

    # 3. SAD — tristesse
    "sad": {
        **NEUTRAL,
        "ParamMouthForm": -0.7,
        "ParamBrowLY": -0.4,
        "ParamBrowRY": -0.4,
        "ParamBrowLAngle": -0.5,
        "ParamBrowRAngle": 0.5,
        "ParamEyeLOpen": 0.8,
        "ParamEyeROpen": 0.8,
        "ParamEyeBallY": -0.2,
        "ParamBodyAngleY": -3,
        "ParamAngleY": -5,
    },

    # 4. SURPRISED — surprise
    "surprised": {
        **NEUTRAL,
        "ParamEyeLOpen": 1.0,
        "ParamEyeROpen": 1.0,
        "ParamEyeBallForm": 0.3,
        "ParamMouthOpenY": 0.5,
        "ParamMouthForm": 0.1,
        "ParamBrowLY": 0.6,
        "ParamBrowRY": 0.6,
        "ParamBrowLAngle": 0.2,
        "ParamBrowRAngle": -0.2,
        "ParamBodyAngleY": 3,
        "ParamAngleY": 5,
    },

    # 5. ANGRY — colère
    "angry": {
        **NEUTRAL,
        "ParamMouthForm": -0.5,
        "ParamMouthOpenY": 0.2,
        "ParamBrowLY": -0.6,
        "ParamBrowRY": -0.6,
        "ParamBrowLAngle": 0.7,
        "ParamBrowRAngle": -0.7,
        "ParamBrowLForm": -0.5,
        "ParamBrowRForm": -0.5,
        "ParamEyeLOpen": 0.9,
        "ParamEyeROpen": 0.9,
        "ParamEyeBallY": 0.2,
        "ParamAngleX": 5,
        "ParamBodyAngleX": 3,
    },

    # 6. THINKING — réflexion / regard de côté
    "thinking": {
        **NEUTRAL,
        "ParamEyeBallX": 0.6,
        "ParamEyeBallY": -0.3,
        "ParamBrowLY": 0.1,
        "ParamBrowRY": 0.3,
        "ParamBrowRAngle": -0.2,
        "ParamMouthForm": -0.1,
        "ParamAngleX": -8,
        "ParamAngleY": -5,
        "ParamAngleZ": 5,
    },

    # 7. WINK — clin d'œil gauche
    "wink": {
        **NEUTRAL,
        "ParamEyeLOpen": 0.0,
        "ParamEyeLSmile": 1.0,
        "ParamEyeROpen": 1.0,
        "ParamMouthForm": 0.6,
        "ParamBrowLY": -0.1,
        "ParamCheek": 0.2,
    },

    # 8. CRYING — larmes
    "crying": {
        **NEUTRAL,
        "ParamMouthForm": -0.8,
        "ParamEyeLOpen": 0.6,
        "ParamEyeROpen": 0.6,
        "ParamEyeBallY": -0.3,
        "ParamTear": 1.5,
        "ParamBrowLY": -0.5,
        "ParamBrowRY": -0.5,
        "ParamBrowLAngle": -0.6,
        "ParamBrowRAngle": 0.6,
        "ParamAngleY": -8,
        "ParamBodyAngleY": -5,
    },

    # 9. NEUTRAL_IDLE — pose de repos avec micro-vie
    "neutral_idle": {
        **NEUTRAL,
        "ParamBreath": 0.5,
        "ParamEyeLOpen": 0.95,
        "ParamEyeROpen": 0.95,
        "ParamBodyAngleY": 1,
        "ParamHairFluffy": 0.2,
    },

    # 10. SPEAKING — bouche en mouvement (snapshot milieu de phrase)
    "speaking": {
        **NEUTRAL,
        "ParamMouthForm": 0.2,
        "ParamMouthOpenY": 0.4,
        "ParamEyeLOpen": 1.0,
        "ParamEyeROpen": 1.0,
        "ParamBrowLY": 0.1,
        "ParamBrowRY": 0.1,
        "ParamBodyAngleY": 2,
        "ParamBreath": 0.3,
    },
}

# ─────────────────────────────────────────────────────────────
# 3. GÉNÉRATEUR DE KEYFRAMES
# ─────────────────────────────────────────────────────────────

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def ease_in_out(t: float) -> float:
    return t * t * (3 - 2 * t)

def make_keyframes(
    from_params: Dict,
    to_params: Dict,
    duration: float = 1.0,
    fps: int = 24,
    easing: str = "ease_in_out"
) -> List[Dict]:
    """Interpolate between two param states, return list of keyframes."""
    frames = []
    n = max(2, int(duration * fps))
    for i in range(n):
        t = i / (n - 1)
        if easing == "ease_in_out":
            t = ease_in_out(t)
        frame = {}
        for key in to_params:
            a = from_params.get(key, NEUTRAL.get(key, 0))
            b = to_params[key]
            frame[key] = round(lerp(a, b, t), 4)
        frame["_time"] = round(i / fps, 4)
        frames.append(frame)
    return frames

def make_blink(start_t: float = 0.0, fps: int = 24) -> List[Dict]:
    """Generate a single blink animation (0.15s)."""
    return [
        {"_time": start_t,        "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0},
        {"_time": start_t + 0.07, "ParamEyeLOpen": 0.0, "ParamEyeROpen": 0.0},
        {"_time": start_t + 0.15, "ParamEyeLOpen": 1.0, "ParamEyeROpen": 1.0},
    ]

def make_idle_breath(duration: float = 3.0, fps: int = 24) -> List[Dict]:
    """Generate idle breathing cycle."""
    frames = []
    n = int(duration * fps)
    for i in range(n):
        t = i / fps
        breath = 0.5 + 0.5 * math.sin(2 * math.pi * t / duration)
        body_y = 1.5 * math.sin(2 * math.pi * t / duration)
        hair = 0.15 * math.sin(2 * math.pi * t / (duration * 1.3))
        frames.append({
            "_time": round(t, 4),
            "ParamBreath": round(breath, 4),
            "ParamBodyAngleY": round(body_y, 4),
            "ParamHairFluffy": round(abs(hair), 4),
        })
    return frames

def make_speaking(duration: float = 3.0, fps: int = 24) -> List[Dict]:
    """Generate mouth movement for speaking."""
    frames = []
    n = int(duration * fps)
    for i in range(n):
        t = i / fps
        # Irregular mouth opening pattern
        mouth_open = max(0, 0.4 * abs(math.sin(t * 7.3)) + 0.2 * abs(math.sin(t * 3.1)))
        mouth_form = 0.1 + 0.15 * math.sin(t * 4.7)
        frames.append({
            "_time": round(t, 4),
            "ParamMouthOpenY": round(min(1.0, mouth_open), 4),
            "ParamMouthForm": round(mouth_form, 4),
        })
    # Add random blinks
    blink_times = [random.uniform(0.5, duration - 0.5) for _ in range(int(duration / 2.5))]
    for bt in blink_times:
        frames.extend(make_blink(bt))
    frames.sort(key=lambda f: f["_time"])
    return frames

# ─────────────────────────────────────────────────────────────
# 4. animate(prompt) — LLM-style keyword parser
# ─────────────────────────────────────────────────────────────

# Keyword → expression mapping
KEYWORD_MAP = {
    # Expressions
    "sourit": "smile", "smile": "smile", "heureuse": "smile", "joyeuse": "smile",
    "grand sourire": "big_smile", "rit": "big_smile", "éclate de rire": "big_smile",
    "triste": "sad", "tristesse": "sad", "pleure": "crying", "larmes": "crying",
    "surprise": "surprised", "surpris": "surprised", "étonnée": "surprised",
    "colère": "angry", "fâchée": "angry", "angry": "angry",
    "réfléchit": "thinking", "pense": "thinking", "thinking": "thinking",
    "clin d'œil": "wink", "wink": "wink",
    "parle": "speaking", "speaking": "speaking", "discours": "speaking",
    "neutre": "neutral_idle", "repos": "neutral_idle", "idle": "neutral_idle",
}

# Action → keyframe generator mapping
ACTION_MAP = {
    "cligne": "blink", "blink": "blink",
    "respire": "breath", "breath": "breath",
    "tourne la tête": "head_turn",
    "regarde à droite": "look_right",
    "regarde à gauche": "look_left",
    "hoche la tête": "nod",
}

def animate(prompt: str, duration: float = 2.0) -> Tuple[Dict, List[Dict]]:
    """
    Parse a natural language prompt and return (params_dict, keyframes_list).

    Examples:
        animate("eYa sourit doucement")
        animate("eYa est surprise puis sourit", duration=3.0)
        animate("eYa parle pendant 3 secondes", duration=3.0)
        animate("eYa cligne des yeux et regarde à droite")
    """
    prompt_lower = prompt.lower()
    params = dict(NEUTRAL)
    keyframes = []

    # 1. Find base expression
    base_expr = None
    for keyword, expr_name in KEYWORD_MAP.items():
        if keyword in prompt_lower:
            base_expr = expr_name
            break

    if base_expr:
        params = dict(EXPRESSIONS[base_expr])
        # Transition from neutral to expression
        keyframes = make_keyframes(NEUTRAL, params, duration=min(0.5, duration * 0.3))

    # 2. Find actions
    if "cligne" in prompt_lower or "blink" in prompt_lower:
        blink_t = duration * 0.5
        keyframes.extend(make_blink(blink_t))

    if "parle" in prompt_lower or "speaking" in prompt_lower or "discours" in prompt_lower:
        keyframes.extend(make_speaking(duration))

    if "respire" in prompt_lower or "breath" in prompt_lower or "idle" in prompt_lower:
        keyframes.extend(make_idle_breath(duration))

    if "regarde à droite" in prompt_lower or "look right" in prompt_lower:
        look = dict(params)
        look["ParamEyeBallX"] = 0.7
        look["ParamAngleX"] = 10
        keyframes.extend(make_keyframes(params, look, duration=0.3))

    if "regarde à gauche" in prompt_lower or "look left" in prompt_lower:
        look = dict(params)
        look["ParamEyeBallX"] = -0.7
        look["ParamAngleX"] = -10
        keyframes.extend(make_keyframes(params, look, duration=0.3))

    if "hoche" in prompt_lower or "nod" in prompt_lower:
        nod = dict(params)
        nod["ParamAngleY"] = -10
        kf = make_keyframes(params, nod, duration=0.25)
        kf.extend(make_keyframes(nod, params, duration=0.25))
        for k in kf:
            k["_time"] = round(k["_time"] + duration * 0.3, 4)
        keyframes.extend(kf)

    # 3. "puis" / "then" — sequence two expressions
    if " puis " in prompt_lower or " then " in prompt_lower:
        parts = prompt_lower.split(" puis " if " puis " in prompt_lower else " then ")
        if len(parts) >= 2:
            _, kf2 = animate(parts[1], duration=duration * 0.6)
            offset = duration * 0.4
            for kf in kf2:
                kf["_time"] = round(kf["_time"] + offset, 4)
            keyframes.extend(kf2)

    # Sort keyframes by time
    keyframes.sort(key=lambda f: f.get("_time", 0))

    # If no expression found, return neutral with idle breath
    if not base_expr and not keyframes:
        params = dict(EXPRESSIONS["neutral_idle"])
        keyframes = make_idle_breath(duration)

    return params, keyframes


# ─────────────────────────────────────────────────────────────
# 5. APPLY TO .STRETCH FILE
# ─────────────────────────────────────────────────────────────

def apply_to_stretch(
    input_stretch: str,
    params: Dict,
    keyframes: List[Dict],
    output_stretch: str,
    animation_name: str = "expression"
) -> str:
    """
    Inject expression params and keyframes into a .stretch file.
    Returns path to the new .stretch file.
    """
    input_path = Path(input_stretch)
    output_path = Path(output_stretch)

    # Copy the .stretch file
    shutil.copy(input_path, output_path)

    # Read project.json
    with zipfile.ZipFile(output_path, 'r') as z:
        with z.open('project.json') as f:
            project = json.load(f)

    # Update parameter default values
    for param in project.get('parameters', []):
        pid = param['id']
        if pid in params:
            param['default'] = params[pid]

    # Find or create animation
    animations = project.get('animations', [])
    existing = next((a for a in animations if a.get('name') == animation_name), None)

    if not existing:
        existing = {
            "id": f"anim_{animation_name}",
            "name": animation_name,
            "duration": max((kf.get('_time', 0) for kf in keyframes), default=1.0) + 0.1,
            "fps": 24,
            "tracks": []
        }
        animations.append(existing)

    # Build tracks from keyframes
    # Group keyframes by parameter
    param_tracks = {}
    for kf in keyframes:
        t = kf.get('_time', 0)
        for key, val in kf.items():
            if key == '_time':
                continue
            if key not in param_tracks:
                param_tracks[key] = []
            param_tracks[key].append({"time": t, "value": val})

    # Convert to Stretchy track format
    existing['tracks'] = []
    for param_id, points in param_tracks.items():
        existing['tracks'].append({
            "parameterId": param_id,
            "keyframes": sorted(points, key=lambda p: p['time'])
        })

    project['animations'] = animations

    # Write back to zip
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        tmp_path = tmp.name

    with zipfile.ZipFile(output_path, 'r') as zin:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'project.json':
                    zout.writestr(item, json.dumps(project, indent=2))
                else:
                    zout.writestr(item, zin.read(item.filename))

    shutil.move(tmp_path, output_path)
    print(f"✅ Expression '{animation_name}' injected → {output_path}")
    return str(output_path)


# ─────────────────────────────────────────────────────────────
# 6. CLI / DEMO
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="eYa expression generator")
    parser.add_argument("--prompt", default="eYa sourit doucement et cligne des yeux",
                        help="Natural language animation prompt")
    parser.add_argument("--expression", default=None,
                        help="Use a named expression directly (smile, sad, surprised...)")
    parser.add_argument("--list", action="store_true", help="List all available expressions")
    parser.add_argument("--input", default="/home/ubuntu/eya_pipeline/output/eya_heuristic.stretch")
    parser.add_argument("--output", default="/home/ubuntu/eya_pipeline/output/eya_expression.stretch")
    parser.add_argument("--duration", type=float, default=2.0)
    args = parser.parse_args()

    if args.list:
        print("Available expressions:")
        for name in EXPRESSIONS:
            print(f"  {name}")
        sys.exit(0)

    if args.expression:
        if args.expression not in EXPRESSIONS:
            print(f"Unknown expression: {args.expression}")
            print(f"Available: {list(EXPRESSIONS.keys())}")
            sys.exit(1)
        params = EXPRESSIONS[args.expression]
        keyframes = make_keyframes(NEUTRAL, params, duration=0.5)
        prompt_used = args.expression
    else:
        params, keyframes = animate(args.prompt, duration=args.duration)
        prompt_used = args.prompt

    print(f"\nPrompt: {prompt_used}")
    print(f"Params changed from neutral:")
    for k, v in params.items():
        if v != NEUTRAL.get(k, 0):
            print(f"  {k}: {NEUTRAL.get(k,0)} → {v}")
    print(f"Keyframes: {len(keyframes)}")

    if Path(args.input).exists():
        out = apply_to_stretch(args.input, params, keyframes, args.output, prompt_used[:30])
        print(f"\nOutput: {out}")
    else:
        print(f"\n[No .stretch file found at {args.input} — params only]")
