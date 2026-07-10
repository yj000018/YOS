"""
eya_expressions_v3.py — Generate eYa expression animations using Stretchy Studio BlendShapes.

Root cause fix: BlendShapes are on PART nodes (not warp deformer nodes).
Structure:
  - node.blendShapes[].deltas = per-vertex dx/dy offsets
  - animation track: nodeId=partId, property="blendShape:shapeId", value=0..1
"""
import zipfile, json, math, shutil, os, random, string
from pathlib import Path

SRC = '/home/ubuntu/eya_pipeline/output/eya_heuristic.stretch'
OUT_DIR = '/home/ubuntu/eya_pipeline/output/expressions_v3'
os.makedirs(OUT_DIR, exist_ok=True)

def rand_id(n=7):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def load_project():
    with zipfile.ZipFile(SRC) as z:
        with z.open('project.json') as f:
            return json.load(f)

def save_stretch(proj, name, out_path):
    """Save project as .stretch zip."""
    with zipfile.ZipFile(SRC) as zin:
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'project.json':
                    zout.writestr(item, json.dumps(proj, separators=(',', ':')))
                else:
                    zout.writestr(item, zin.read(item.filename))

def compute_smile_deltas(verts, cx, intensity=1.0):
    """
    Smile: corners of mouth go up and out, center stays.
    cx = horizontal center of mouth mesh
    """
    deltas = []
    x_range = max(v['x'] for v in verts) - min(v['x'] for v in verts)
    y_range = max(v['y'] for v in verts) - min(v['y'] for v in verts)
    for v in verts:
        # Normalized x position: -1 (left) to +1 (right)
        nx = (v['x'] - cx) / (x_range / 2 + 1e-6)
        # Smile curve: corners go up (dy negative), center stays
        # Quadratic: dy = -A * nx^2 + B (parabola opening down)
        dy = -intensity * 12 * (nx ** 2)  # corners up, center flat
        dx = intensity * 4 * nx           # corners spread outward
        deltas.append({'dx': round(dx, 2), 'dy': round(dy, 2)})
    return deltas

def compute_sad_deltas(verts, cx, intensity=1.0):
    """Sad: corners go down."""
    deltas = []
    x_range = max(v['x'] for v in verts) - min(v['x'] for v in verts)
    for v in verts:
        nx = (v['x'] - cx) / (x_range / 2 + 1e-6)
        dy = intensity * 10 * (nx ** 2)  # corners down
        dx = 0
        deltas.append({'dx': round(dx, 2), 'dy': round(dy, 2)})
    return deltas

def compute_open_deltas(verts, cy, intensity=1.0):
    """Open mouth: top lip up, bottom lip down."""
    deltas = []
    y_range = max(v['y'] for v in verts) - min(v['y'] for v in verts)
    for v in verts:
        ny = (v['y'] - cy) / (y_range / 2 + 1e-6)
        dy = intensity * 8 * ny   # top goes up, bottom goes down
        deltas.append({'dx': 0, 'dy': round(dy, 2)})
    return deltas

def compute_eyebrow_raise_deltas(verts, intensity=1.0):
    """Raise eyebrows up."""
    return [{'dx': 0, 'dy': round(-intensity * 8, 2)} for _ in verts]

def compute_eyebrow_furrow_deltas(verts, cx, intensity=1.0):
    """Furrow eyebrows: inner corners down."""
    deltas = []
    x_range = max(v['x'] for v in verts) - min(v['x'] for v in verts)
    for v in verts:
        nx = (v['x'] - cx) / (x_range / 2 + 1e-6)
        # Inner corner (toward center face) goes down
        dy = intensity * 6 * (1 - abs(nx))
        deltas.append({'dx': 0, 'dy': round(dy, 2)})
    return deltas

def compute_eyelid_close_deltas(verts, cy, intensity=1.0):
    """Close eyelid: top vertices move down."""
    deltas = []
    y_min = min(v['y'] for v in verts)
    y_max = max(v['y'] for v in verts)
    for v in verts:
        # Top vertices (lower y value) move down more
        t = 1.0 - (v['y'] - y_min) / (y_max - y_min + 1e-6)
        dy = intensity * 15 * t
        deltas.append({'dx': 0, 'dy': round(dy, 2)})
    return deltas

def make_blendshape_animation(proj, name, shapes_by_node):
    """
    shapes_by_node: dict of {node_name: [(shape_name, deltas)]}
    Returns modified project copy with blendShapes added + animation.
    """
    import copy
    proj = copy.deepcopy(proj)

    anim_tracks = []

    for node_name, shapes in shapes_by_node.items():
        node = next((n for n in proj['nodes'] if n['name'] == node_name), None)
        if node is None:
            print(f"  WARNING: node '{node_name}' not found")
            continue

        if 'blendShapes' not in node:
            node['blendShapes'] = []
        if 'blendShapeValues' not in node:
            node['blendShapeValues'] = {}

        for shape_name, deltas in shapes:
            shape_id = rand_id()
            node['blendShapes'].append({
                'id': shape_id,
                'name': shape_name,
                'deltas': deltas,
            })
            node['blendShapeValues'][shape_id] = 0.0

            # Animation track: 0 → 1 → 0 over 1 second
            anim_tracks.append({
                'nodeId': node['id'],
                'property': f'blendShape:{shape_id}',
                'keyframes': [
                    {'time': 0,    'value': 0.0, 'easing': 'linear'},
                    {'time': 500,  'value': 1.0, 'easing': 'linear'},
                    {'time': 1000, 'value': 0.0, 'easing': 'linear'},
                ]
            })

    # Add animation
    anim = {
        'id': rand_id(),
        'name': f'eYa {name}',
        'duration': 1000,
        'fps': 24,
        'audioTracks': [],
        'tracks': anim_tracks,
    }
    proj['animations'].append(anim)
    return proj

# ─── Load project ───────────────────────────────────────────────────────────
proj_base = load_project()

# Get geometry centers
def get_node(name): return next(n for n in proj_base['nodes'] if n['name'] == name)
def center(node):
    verts = node['mesh']['vertices']
    return sum(v['x'] for v in verts)/len(verts), sum(v['y'] for v in verts)/len(verts)

mouth_node = get_node('mouth')
mouth_verts = mouth_node['mesh']['vertices']
mouth_cx, mouth_cy = center(mouth_node)

eyebrow_l_node = get_node('eyebrow-l')
eyebrow_l_verts = eyebrow_l_node['mesh']['vertices']
eyebrow_l_cx, _ = center(eyebrow_l_node)

eyebrow_r_node = get_node('eyebrow-r')
eyebrow_r_verts = eyebrow_r_node['mesh']['vertices']
eyebrow_r_cx, _ = center(eyebrow_r_node)

eyelash_l_node = get_node('eyelash-l')
eyelash_l_verts = eyelash_l_node['mesh']['vertices']
_, eyelash_l_cy = center(eyelash_l_node)

eyelash_r_node = get_node('eyelash-r')
eyelash_r_verts = eyelash_r_node['mesh']['vertices']
_, eyelash_r_cy = center(eyelash_r_node)

# ─── Define expressions ─────────────────────────────────────────────────────
EXPRESSIONS = {
    'smile': {
        'mouth': [('smile', compute_smile_deltas(mouth_verts, mouth_cx, 1.0))],
        'eyebrow-l': [('smile_brow', compute_eyebrow_raise_deltas(eyebrow_l_verts, 0.3))],
        'eyebrow-r': [('smile_brow', compute_eyebrow_raise_deltas(eyebrow_r_verts, 0.3))],
    },
    'big_smile': {
        'mouth': [('big_smile', compute_smile_deltas(mouth_verts, mouth_cx, 1.8)),
                  ('open', compute_open_deltas(mouth_verts, mouth_cy, 0.8))],
        'eyebrow-l': [('brow', compute_eyebrow_raise_deltas(eyebrow_l_verts, 0.6))],
        'eyebrow-r': [('brow', compute_eyebrow_raise_deltas(eyebrow_r_verts, 0.6))],
    },
    'sad': {
        'mouth': [('sad', compute_sad_deltas(mouth_verts, mouth_cx, 1.0))],
        'eyebrow-l': [('sad_brow', compute_eyebrow_furrow_deltas(eyebrow_l_verts, eyebrow_l_cx, 0.8))],
        'eyebrow-r': [('sad_brow', compute_eyebrow_furrow_deltas(eyebrow_r_verts, eyebrow_r_cx, 0.8))],
    },
    'surprised': {
        'mouth': [('open', compute_open_deltas(mouth_verts, mouth_cy, 1.5))],
        'eyebrow-l': [('raise', compute_eyebrow_raise_deltas(eyebrow_l_verts, 1.2))],
        'eyebrow-r': [('raise', compute_eyebrow_raise_deltas(eyebrow_r_verts, 1.2))],
    },
    'angry': {
        'mouth': [('sad', compute_sad_deltas(mouth_verts, mouth_cx, 0.6))],
        'eyebrow-l': [('furrow', compute_eyebrow_furrow_deltas(eyebrow_l_verts, eyebrow_l_cx, 1.5))],
        'eyebrow-r': [('furrow', compute_eyebrow_furrow_deltas(eyebrow_r_verts, eyebrow_r_cx, 1.5))],
    },
    'blink': {
        'eyelash-l': [('close', compute_eyelid_close_deltas(eyelash_l_verts, eyelash_l_cy, 1.0))],
        'eyelash-r': [('close', compute_eyelid_close_deltas(eyelash_r_verts, eyelash_r_cy, 1.0))],
    },
    'wink': {
        'eyelash-l': [('close', compute_eyelid_close_deltas(eyelash_l_verts, eyelash_l_cy, 1.0))],
        'mouth': [('smile', compute_smile_deltas(mouth_verts, mouth_cx, 0.5))],
    },
    'neutral': {
        # Neutral = no deformation (zero deltas)
        'mouth': [('neutral', [{'dx': 0, 'dy': 0} for _ in mouth_verts])],
    },
    'thinking': {
        'eyebrow-l': [('raise', compute_eyebrow_raise_deltas(eyebrow_l_verts, 0.8))],
        'eyebrow-r': [('furrow', compute_eyebrow_furrow_deltas(eyebrow_r_verts, eyebrow_r_cx, 0.5))],
        'mouth': [('slight', compute_smile_deltas(mouth_verts, mouth_cx, 0.2))],
    },
    'shy': {
        'mouth': [('shy', compute_smile_deltas(mouth_verts, mouth_cx, 0.6))],
        'eyebrow-l': [('raise', compute_eyebrow_raise_deltas(eyebrow_l_verts, 0.4))],
        'eyebrow-r': [('raise', compute_eyebrow_raise_deltas(eyebrow_r_verts, 0.4))],
    },
}

# ─── Generate files ──────────────────────────────────────────────────────────
print(f"Generating {len(EXPRESSIONS)} expressions...")
results = []
for expr_name, shapes_by_node in EXPRESSIONS.items():
    proj = make_blendshape_animation(proj_base, expr_name, shapes_by_node)
    out_path = os.path.join(OUT_DIR, f'eya_{expr_name}.stretch')
    save_stretch(proj, expr_name, out_path)
    size = os.path.getsize(out_path)
    n_tracks = sum(len(shapes) for shapes in shapes_by_node.values())
    print(f"  ✅ {expr_name:15s} → {out_path.split('/')[-1]}  ({size//1024}KB, {n_tracks} tracks)")
    results.append((expr_name, out_path, n_tracks))

print(f"\n✅ {len(results)} expressions generated in {OUT_DIR}")
