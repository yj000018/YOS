"""
eya_expressions_v2.py
=====================
Generates Stretchy Studio animations using the CORRECT mesh vertex displacement format.

Format: each keyframe contains absolute XY coordinates for ALL mesh vertices.
- MouthWarp: 9 vertices (3x3 grid)
- EyeLWarp / EyeRWarp: 9 vertices each
- EyebrowLWarp / EyebrowRWarp: 9 vertices each
- FaceWarp: 36 vertices (6x6 grid)

Usage:
    from eya_expressions_v2 import add_expression, add_expression_from_prompt
    add_expression('/path/to/input.stretch', '/path/to/output.stretch', 'smile')
    add_expression_from_prompt('/path/to/input.stretch', '/path/to/output.stretch', 'eYa sourit')
"""

import zipfile
import json
import copy
import os
import re
import tempfile
import shutil

# ─────────────────────────────────────────────
# EXPRESSION DEFINITIONS
# Each expression defines DELTA offsets applied to the neutral (t=0) vertex positions.
# Format: { 'nodeId': [(dx0,dy0), (dx1,dy1), ...], ... }
# Positive Y = down in canvas space.
# ─────────────────────────────────────────────

EXPRESSION_DELTAS = {

    "smile": {
        # MouthWarp (wqb5nmv): 9 vertices (3x3)
        # Corners up → smile shape. Calibrated to ~15px/vertex like Parameters anim.
        "wqb5nmv": [
            (-18, -14), (0, -10), (18, -14),  # top row: corners lift strongly
            (-20,   0), (0,   0), (20,   0),  # mid row: corners out
            (-14,  12), (0,   8), (14,  12),  # bottom row: corners down (open)
        ],
        # EyebrowLWarp (f16aiwn): raise outer corner
        "f16aiwn": [
            (-4, -6), (0, -4), (4, -8),
            (-4, -6), (0, -4), (4, -8),
            (-4, -6), (0, -4), (4, -8),
        ],
        # EyebrowRWarp (swpfcoe): mirror
        "swpfcoe": [
            (-4, -8), (0, -4), (4, -6),
            (-4, -8), (0, -4), (4, -6),
            (-4, -8), (0, -4), (4, -6),
        ],
        # EyeLWarp (ihl34zg): happy squint
        "ihl34zg": [
            (0,  6), (0,  6), (0,  6),
            (0,  0), (0,  0), (0,  0),
            (0, -6), (0, -6), (0, -6),
        ],
        # EyeRWarp (3zdcal0): mirror
        "3zdcal0": [
            (0,  6), (0,  6), (0,  6),
            (0,  0), (0,  0), (0,  0),
            (0, -6), (0, -6), (0, -6),
        ],
        # FaceWarp (0z3f78q): cheek lift (36 vertices)
        "0z3f78q": [(0, 0)] * 36,
    },

    "big_smile": {
        "wqb5nmv": [
            (-24, -18), (0, -14), (24, -18),
            (-26,   4), (0,   0), (26,   4),
            (-20,  18), (0,  14), (20,  18),
        ],
        "f16aiwn": [
            (-6, -10), (0, -6), (6, -12),
            (-6, -10), (0, -6), (6, -12),
            (-6, -10), (0, -6), (6, -12),
        ],
        "swpfcoe": [
            (-6, -12), (0, -6), (6, -10),
            (-6, -12), (0, -6), (6, -10),
            (-6, -12), (0, -6), (6, -10),
        ],
        "ihl34zg": [
            (0,  10), (0,  10), (0,  10),
            (0,   0), (0,   0), (0,   0),
            (0, -10), (0, -10), (0, -10),
        ],
        "3zdcal0": [
            (0,  10), (0,  10), (0,  10),
            (0,   0), (0,   0), (0,   0),
            (0, -10), (0, -10), (0, -10),
        ],
        "0z3f78q": [(0, 0)] * 36,
    },

    "sad": {
        "wqb5nmv": [
            (16,  10), (0,  6), (-16,  10),  # corners down
            (12,   0), (0,  0), (-12,   0),
            (10, -10), (0, -6), (-10, -10),
        ],
        "f16aiwn": [
            (8, 8), (0, 4), (-4,  0),
            (8, 8), (0, 4), (-4,  0),
            (8, 8), (0, 4), (-4,  0),
        ],
        "swpfcoe": [
            (4,  0), (0, 4), (-8,  8),
            (4,  0), (0, 4), (-8,  8),
            (4,  0), (0, 4), (-8,  8),
        ],
        "ihl34zg": [(0, 0)] * 9,
        "3zdcal0": [(0, 0)] * 9,
        "0z3f78q": [(0, 0)] * 36,
    },

    "surprised": {
        "wqb5nmv": [
            (0, -12), (0, -12), (0, -12),  # top row up (mouth opens)
            (0,   0), (0,   0), (0,   0),
            (0,  14), (0,  14), (0,  14),  # bottom row down
        ],
        "f16aiwn": [
            (-4, -14), (0, -14), (4, -14),  # brows shoot up
            (-4, -14), (0, -14), (4, -14),
            (-4, -14), (0, -14), (4, -14),
        ],
        "swpfcoe": [
            (-4, -14), (0, -14), (4, -14),
            (-4, -14), (0, -14), (4, -14),
            (-4, -14), (0, -14), (4, -14),
        ],
        "ihl34zg": [
            (0, -12), (0, -12), (0, -12),  # eyes wide open
            (0,   0), (0,   0), (0,   0),
            (0,  12), (0,  12), (0,  12),
        ],
        "3zdcal0": [
            (0, -12), (0, -12), (0, -12),
            (0,   0), (0,   0), (0,   0),
            (0,  12), (0,  12), (0,  12),
        ],
        "0z3f78q": [(0, 0)] * 36,
    },

    "angry": {
        "wqb5nmv": [
            (12,  6), (0,  0), (-12,  6),
            ( 8,  0), (0,  0), ( -8,  0),
            ( 8, -6), (0,  0), ( -8, -6),
        ],
        "f16aiwn": [
            (12, 14), (6, 10), (-2,  4),  # inner brow down, outer up = angry V
            (12, 14), (6, 10), (-2,  4),
            (12, 14), (6, 10), (-2,  4),
        ],
        "swpfcoe": [
            ( 2,  4), (-6, 10), (-12, 14),
            ( 2,  4), (-6, 10), (-12, 14),
            ( 2,  4), (-6, 10), (-12, 14),
        ],
        "ihl34zg": [(0, 0)] * 9,
        "3zdcal0": [(0, 0)] * 9,
        "0z3f78q": [(0, 0)] * 36,
    },

    "blink": {
        "ihl34zg": [
            (0,  14), (0,  14), (0,  14),  # top lid down
            (0,   0), (0,   0), (0,   0),
            (0, -14), (0, -14), (0, -14),  # bottom lid up
        ],
        "3zdcal0": [
            (0,  14), (0,  14), (0,  14),
            (0,   0), (0,   0), (0,   0),
            (0, -14), (0, -14), (0, -14),
        ],
        "wqb5nmv": [(0, 0)] * 9,
        "f16aiwn": [(0, 0)] * 9,
        "swpfcoe": [(0, 0)] * 9,
        "0z3f78q": [(0, 0)] * 36,
    },

    "wink": {
        "ihl34zg": [
            (0,  14), (0,  14), (0,  14),  # left eye closes
            (0,   0), (0,   0), (0,   0),
            (0, -14), (0, -14), (0, -14),
        ],
        "3zdcal0": [(0, 0)] * 9,  # right eye stays open
        "wqb5nmv": [
            (-10, -8), (0, -6), (10, -8),  # slight smile
            (-10,  0), (0,  0), (10,  0),
            (-10,  8), (0,  6), (10,  8),
        ],
        "f16aiwn": [(0, 0)] * 9,
        "swpfcoe": [(0, 0)] * 9,
        "0z3f78q": [(0, 0)] * 36,
    },

    "neutral": {
        # All zeros — returns to rest pose
        "wqb5nmv": [(0, 0)] * 9,
        "f16aiwn": [(0, 0)] * 9,
        "swpfcoe": [(0, 0)] * 9,
        "ihl34zg": [(0, 0)] * 9,
        "3zdcal0": [(0, 0)] * 9,
        "0z3f78q": [(0, 0)] * 36,
    },

    "thinking": {
        "wqb5nmv": [
            (10, -6), (4, -4), (-4, -6),  # mouth slightly asymmetric
            (10,  0), (4,  0), (-4,  0),
            (10,  6), (4,  4), (-4,  6),
        ],
        "f16aiwn": [
            (-2, -10), (0, -8), (4, -6),  # left brow slightly raised
            (-2, -10), (0, -8), (4, -6),
            (-2, -10), (0, -8), (4, -6),
        ],
        "swpfcoe": [
            (-4, -6), (0, -8), (2, -10),
            (-4, -6), (0, -8), (2, -10),
            (-4, -6), (0, -8), (2, -10),
        ],
        "ihl34zg": [(0, 0)] * 9,
        "3zdcal0": [
            (0,  6), (0,  6), (0,  6),  # right eye slightly squinted
            (0,  0), (0,  0), (0,  0),
            (0, -6), (0, -6), (0, -6),
        ],
        "0z3f78q": [(0, 0)] * 36,
    },

    "shy": {
        "wqb5nmv": [
            (-10, -10), (0, -8), (10, -10),  # small smile
            (-10,   0), (0,  0), (10,   0),
            (-10,   6), (0,  4), (10,   6),
        ],
        "f16aiwn": [(0, 0)] * 9,
        "swpfcoe": [(0, 0)] * 9,
        "ihl34zg": [
            (0,  8), (0,  8), (0,  8),  # eyes slightly downcast
            (0,  0), (0,  0), (0,  0),
            (0, -8), (0, -8), (0, -8),
        ],
        "3zdcal0": [
            (0,  8), (0,  8), (0,  8),
            (0,  0), (0,  0), (0,  0),
            (0, -8), (0, -8), (0, -8),
        ],
        "0z3f78q": [(0, 0)] * 36,
    },
}

# ─────────────────────────────────────────────
# PROMPT → EXPRESSION MAPPING
# ─────────────────────────────────────────────

PROMPT_MAP = {
    # French
    "sourit": "smile",
    "sourire": "smile",
    "grand sourire": "big_smile",
    "triste": "sad",
    "tristesse": "sad",
    "surpris": "surprised",
    "surprise": "surprised",
    "étonné": "surprised",
    "étonnée": "surprised",
    "en colère": "angry",
    "colère": "angry",
    "cligne": "blink",
    "clin d'oeil": "wink",
    "clin d'œil": "wink",
    "neutre": "neutral",
    "pense": "thinking",
    "réfléchit": "thinking",
    "timide": "shy",
    "gêné": "shy",
    # English
    "smile": "smile",
    "smiling": "smile",
    "big smile": "big_smile",
    "happy": "smile",
    "sad": "sad",
    "crying": "sad",
    "surprised": "surprised",
    "shocked": "surprised",
    "angry": "angry",
    "mad": "angry",
    "blink": "blink",
    "blinking": "blink",
    "wink": "wink",
    "winking": "wink",
    "neutral": "neutral",
    "thinking": "thinking",
    "shy": "shy",
    "embarrassed": "shy",
}


def _apply_deltas(neutral_verts, deltas):
    """Apply delta offsets to neutral vertex positions."""
    result = []
    for i, v in enumerate(neutral_verts):
        dx, dy = deltas[i] if i < len(deltas) else (0, 0)
        result.append({"x": v["x"] + dx, "y": v["y"] + dy})
    return result


def _get_neutral_verts(tracks, node_id):
    """Get neutral (t=0) vertex positions for a given nodeId."""
    for t in tracks:
        if t["nodeId"] == node_id:
            kfs = t["keyframes"]
            if kfs:
                return kfs[0]["value"]
    return None


def add_expression(input_stretch, output_stretch, expression_name,
                   animation_name=None, duration_ms=1000, fps=24):
    """
    Add an expression animation to a .stretch file using mesh vertex displacement.

    Args:
        input_stretch: path to source .stretch file
        output_stretch: path to output .stretch file
        expression_name: key from EXPRESSION_DELTAS dict
        animation_name: display name in Stretchy Studio (default: expression_name)
        duration_ms: animation duration in milliseconds
        fps: frames per second
    """
    if expression_name not in EXPRESSION_DELTAS:
        raise ValueError(f"Unknown expression: {expression_name}. Available: {list(EXPRESSION_DELTAS.keys())}")

    if animation_name is None:
        animation_name = f"eYa {expression_name}"

    deltas = EXPRESSION_DELTAS[expression_name]

    # Read source .stretch
    with zipfile.ZipFile(input_stretch, 'r') as z:
        with z.open('project.json') as f:
            proj = json.load(f)
        # Get all file names
        file_list = z.namelist()

    # Find the "Parameters" animation to get neutral vertex positions
    params_anim = next((a for a in proj.get('animations', []) if a['name'] == 'Parameters'), None)
    if params_anim is None:
        raise ValueError("No 'Parameters' animation found in .stretch file — cannot determine neutral pose")

    neutral_tracks = params_anim['tracks']

    # Build animation tracks
    anim_tracks = []
    for node_id, node_deltas in deltas.items():
        neutral_verts = _get_neutral_verts(neutral_tracks, node_id)
        if neutral_verts is None:
            print(f"  Warning: nodeId {node_id} not found in Parameters tracks, skipping")
            continue

        # Pose at peak (half duration)
        peak_verts = _apply_deltas(neutral_verts, node_deltas)
        half_t = duration_ms // 2

        track = {
            "nodeId": node_id,
            "property": "mesh_verts",
            "keyframes": [
                {"time": 0,           "value": copy.deepcopy(neutral_verts)},
                {"time": half_t,      "value": peak_verts},
                {"time": duration_ms, "value": copy.deepcopy(neutral_verts)},
            ]
        }
        anim_tracks.append(track)

    # Build animation object
    new_anim = {
        "id": f"anim-{expression_name}-{os.urandom(4).hex()}",
        "name": animation_name,
        "duration": duration_ms,
        "fps": fps,
        "tracks": anim_tracks
    }

    # Add to project
    proj_copy = copy.deepcopy(proj)
    # Remove any existing animation with same name
    proj_copy['animations'] = [a for a in proj_copy.get('animations', [])
                                if a.get('name') != animation_name]
    proj_copy['animations'].append(new_anim)

    # Write output .stretch (ZIP)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract original
        with zipfile.ZipFile(input_stretch, 'r') as z:
            z.extractall(tmpdir)

        # Write updated project.json
        proj_path = os.path.join(tmpdir, 'project.json')
        with open(proj_path, 'w') as f:
            json.dump(proj_copy, f, separators=(',', ':'))

        # Repack as ZIP
        with zipfile.ZipFile(output_stretch, 'w', zipfile.ZIP_DEFLATED) as zout:
            for root, dirs, files in os.walk(tmpdir):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    arcname = os.path.relpath(fpath, tmpdir)
                    zout.write(fpath, arcname)

    print(f"✅ Expression '{animation_name}' added → {output_stretch}")
    print(f"   Duration: {duration_ms}ms @ {fps}fps")
    print(f"   Tracks: {len(anim_tracks)} warp nodes")
    return output_stretch


def add_expression_from_prompt(input_stretch, output_stretch, prompt):
    """
    Add an expression animation from a natural language prompt.

    Args:
        input_stretch: path to source .stretch file
        output_stretch: path to output .stretch file
        prompt: natural language description (e.g., "eYa sourit", "smile", "triste")
    """
    prompt_lower = prompt.lower().strip()

    # Try to match prompt to expression
    expression_name = None
    for keyword, expr in PROMPT_MAP.items():
        if keyword in prompt_lower:
            expression_name = expr
            break

    if expression_name is None:
        # Default to smile if no match
        print(f"  Warning: no expression match for '{prompt}', defaulting to 'smile'")
        expression_name = "smile"

    print(f"  Prompt '{prompt}' → expression '{expression_name}'")
    return add_expression(input_stretch, output_stretch, expression_name,
                          animation_name=prompt)


def add_all_expressions(input_stretch, output_dir):
    """Generate one .stretch file per expression."""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for expr_name in EXPRESSION_DELTAS.keys():
        out_path = os.path.join(output_dir, f"eya_{expr_name}.stretch")
        add_expression(input_stretch, out_path, expr_name)
        results.append(out_path)
    return results


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="eYa Expressions v2 — Stretchy Studio mesh vertex format")
    parser.add_argument("input", help="Input .stretch file")
    parser.add_argument("output", help="Output .stretch file")
    parser.add_argument("--expression", "-e", default="smile",
                        help=f"Expression name: {list(EXPRESSION_DELTAS.keys())}")
    parser.add_argument("--prompt", "-p", default=None,
                        help="Natural language prompt (overrides --expression)")
    parser.add_argument("--all", action="store_true",
                        help="Generate all expressions (output must be a directory)")
    parser.add_argument("--duration", "-d", type=int, default=1000,
                        help="Animation duration in ms (default: 1000)")
    parser.add_argument("--list", action="store_true",
                        help="List available expressions and exit")
    args = parser.parse_args()

    if args.list:
        print("Available expressions:")
        for k in EXPRESSION_DELTAS.keys():
            keywords = [kw for kw, v in PROMPT_MAP.items() if v == k]
            print(f"  {k}: {keywords}")
        sys.exit(0)

    if args.all:
        results = add_all_expressions(args.input, args.output)
        print(f"\n✅ Generated {len(results)} expression files in {args.output}")
    elif args.prompt:
        add_expression_from_prompt(args.input, args.output, args.prompt)
    else:
        add_expression(args.input, args.output, args.expression, duration_ms=args.duration)
