"""
gen_smile_wink.py — eYa "sourire chaud + clin d'œil coquin + tête inclinée"
Uses ONLY confirmed-working properties:
  - blendShape:xxx  (mouth smile, eyebrow lift)
  - opacity         (wink via eyelash-l + eyewhite-l fade)
  - rotation        (head tilt, torso sway)
  - position        (subtle head bob)

Node IDs from eya_smile(2).stretch:
  mouth          ivvtdwl  bs=rerzk5g  (smile)
  eyebrow-r      4t6ekts  bs=ojc5msv  (smile_brow)
  eyebrow-l      9oetuil  bs=tryuiiu  (smile_brow)
  eyelash-l      s2x7l81  opacity     (wink)
  eyewhite-l     2gbtloa  opacity     (wink)
  grp-head       grp-98lbjmyda  rotation  (head tilt)
  grp-torso      grp-velomqc2f  rotation  (body sway)
"""
import zipfile, json, copy, random, string, os

SRC = '/home/ubuntu/upload/eya_smile(2).stretch'
OUT = '/home/ubuntu/eya_pipeline/output/eya_smile_wink.stretch'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

# ── Load source project ──────────────────────────────────────────────────────
with zipfile.ZipFile(SRC, 'r') as z:
    proj = json.loads(z.read('project.json'))
    all_files = {name: z.read(name) for name in z.namelist()}

# ── Animation design ─────────────────────────────────────────────────────────
# Total: 5000ms @ 24fps
# Phase 1  0–500ms    : neutral hold
# Phase 2  500–1800ms : warm smile builds (mouth + brows)
# Phase 3  1800–2800ms: smile peak, subtle head settle
# Phase 4  2800–3200ms: head starts tilting right (coquin)
# Phase 5  3200–3800ms: LEFT eye winks (opacity 1→0→1), head tilt peaks, smile widens
# Phase 6  3800–4500ms: wink releases, head returns
# Phase 7  4500–5000ms: settle back to warm smile

DURATION = 5000

def ease(t):
    """Cubic ease in-out string for Stretchy."""
    return "easeInOut"

smile_wink_anim = {
    "id": uid(),
    "name": "eYa — Sourire & Clin d'œil",
    "duration": DURATION,
    "fps": 24,
    "audioTracks": [],
    "tracks": [

        # ── MOUTH smile blendShape ──────────────────────────────────────────
        {
            "nodeId": "ivvtdwl",
            "property": "blendShape:rerzk5g",
            "keyframes": [
                {"time": 0,    "value": 0.0,  "easing": "easeInOut"},
                {"time": 500,  "value": 0.0,  "easing": "easeInOut"},
                {"time": 1800, "value": 0.85, "easing": "easeInOut"},  # smile builds
                {"time": 2800, "value": 0.90, "easing": "easeInOut"},  # peak
                {"time": 3500, "value": 0.95, "easing": "easeInOut"},  # widens with wink
                {"time": 4200, "value": 0.88, "easing": "easeInOut"},  # release
                {"time": 5000, "value": 0.80, "easing": "easeInOut"},  # settle
            ]
        },

        # ── EYEBROW-R smile_brow blendShape ────────────────────────────────
        {
            "nodeId": "4t6ekts",
            "property": "blendShape:ojc5msv",
            "keyframes": [
                {"time": 0,    "value": 0.0,  "easing": "easeInOut"},
                {"time": 700,  "value": 0.0,  "easing": "easeInOut"},
                {"time": 1800, "value": 0.70, "easing": "easeInOut"},
                {"time": 2800, "value": 0.75, "easing": "easeInOut"},
                {"time": 3200, "value": 0.80, "easing": "easeInOut"},  # slight raise with wink
                {"time": 4200, "value": 0.70, "easing": "easeInOut"},
                {"time": 5000, "value": 0.65, "easing": "easeInOut"},
            ]
        },

        # ── EYEBROW-L smile_brow blendShape ────────────────────────────────
        {
            "nodeId": "9oetuil",
            "property": "blendShape:tryuiiu",
            "keyframes": [
                {"time": 0,    "value": 0.0,  "easing": "easeInOut"},
                {"time": 700,  "value": 0.0,  "easing": "easeInOut"},
                {"time": 1800, "value": 0.70, "easing": "easeInOut"},
                {"time": 2800, "value": 0.75, "easing": "easeInOut"},
                {"time": 3200, "value": 0.85, "easing": "easeInOut"},  # left brow arches for wink
                {"time": 3600, "value": 0.90, "easing": "easeInOut"},  # peak arch during wink
                {"time": 4200, "value": 0.70, "easing": "easeInOut"},
                {"time": 5000, "value": 0.65, "easing": "easeInOut"},
            ]
        },

        # ── EYELASH-L opacity (wink — left eye closes) ─────────────────────
        {
            "nodeId": "s2x7l81",
            "property": "opacity",
            "keyframes": [
                {"time": 0,    "value": 1},
                {"time": 3100, "value": 1},
                {"time": 3350, "value": 0},   # eye closes
                {"time": 3650, "value": 1},   # eye opens
                {"time": 5000, "value": 1},
            ]
        },

        # ── EYEWHITE-L opacity (wink — white disappears too) ───────────────
        {
            "nodeId": "2gbtloa",
            "property": "opacity",
            "keyframes": [
                {"time": 0,    "value": 1},
                {"time": 3100, "value": 1},
                {"time": 3350, "value": 0},
                {"time": 3650, "value": 1},
                {"time": 5000, "value": 1},
            ]
        },

        # ── HEAD rotation (tilt right = coquin) ────────────────────────────
        # Positive = tilt right (eYa's right = viewer's left)
        {
            "nodeId": "grp-98lbjmyda",
            "property": "rotation",
            "keyframes": [
                {"time": 0,    "value": 0},
                {"time": 1000, "value": -1},   # very subtle settle as smile builds
                {"time": 2000, "value": 0},
                {"time": 2800, "value": 0},
                {"time": 3200, "value": -5},   # head tilts right (coquin)
                {"time": 3600, "value": -7},   # peak tilt during wink
                {"time": 4200, "value": -4},   # releasing
                {"time": 5000, "value": -2},   # settle slightly tilted
            ]
        },

        # ── TORSO rotation (gentle sway — natural breathing feel) ──────────
        {
            "nodeId": "grp-velomqc2f",
            "property": "rotation",
            "keyframes": [
                {"time": 0,    "value": 0},
                {"time": 1200, "value": -1},
                {"time": 2500, "value": 0},
                {"time": 3500, "value": 1},    # slight counter-sway during wink
                {"time": 5000, "value": 0},
            ]
        },

    ]
}

# ── Inject into project ──────────────────────────────────────────────────────
# Keep existing animations, add ours
proj['animations'].append(smile_wink_anim)

# ── Write new .stretch file ──────────────────────────────────────────────────
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'project.json':
            zout.writestr('project.json', json.dumps(proj, separators=(',', ':')))
        else:
            zout.writestr(name, data)

print(f"✅ Written: {OUT}")
print(f"   Animation: '{smile_wink_anim['name']}' | {DURATION}ms | {len(smile_wink_anim['tracks'])} tracks")
print(f"   Tracks: mouth_smile, eyebrow_r, eyebrow_l, eyelash_l_opacity, eyewhite_l_opacity, head_rotation, torso_rotation")
