# Stretchy Studio — BlendShapes System (Root Cause Found)

## Root Cause of "No Movement"
We were animating WARP DEFORMER keyframes (mesh_verts on warpDeformer nodes).
The correct approach for expressions is **BLEND SHAPES** on PART nodes.

## BlendShape Structure (on part nodes)
```json
{
  "id": "partNodeId",
  "type": "part",
  "mesh": { "vertices": [...], "uvs": [...], "triangles": [...] },
  "blendShapes": [
    {
      "id": "shapeId",
      "name": "smile",
      "deltas": [
        {"dx": 5, "dy": -10},  // per-vertex delta from rest position
        ...
      ]
    }
  ],
  "blendShapeValues": { "shapeId": 0.0 }  // 0=off, 1=full
}
```

## Animation Track for BlendShapes
```json
{
  "nodeId": "partNodeId",
  "property": "blendShape:shapeId",
  "keyframes": [
    {"time": 0, "value": 0.0},
    {"time": 500, "value": 1.0},
    {"time": 1000, "value": 0.0}
  ]
}
```

## How it Works (CanvasViewport.jsx lines 686-715)
1. For each part node with blendShapes:
   - Get influence value from: draftPose OR keyframe OR blendShapeValues default
   - `const prop = 'blendShape:${shape.id}'`
   - `const v = draft?.[prop] ?? kfOv?.[prop] ?? node.blendShapeValues?.[shape.id] ?? 0`
2. Apply weighted deltas: `bx += d.dx * influences[j]`
3. Result goes into poseOverrides as mesh_verts for the part node

## Key Difference from Warp Deformers
- Warp deformers: animate the GRID control points (affects children via bilinear)
- BlendShapes: animate VERTEX DELTAS directly on the part mesh
- BlendShapes are ON THE PART NODE, not the warp deformer node

## What We Need to Do
For each expression (smile, sad, etc.):
1. Add blendShapes array to the relevant PART nodes (mouth, eyelash-l, eyelash-r, eyebrow-l, eyebrow-r)
2. Each blendShape has deltas for each vertex of that part's mesh
3. Add animation tracks with property "blendShape:shapeId" targeting the PART node
4. Keyframe the influence from 0 → 1 → 0

## Part Node IDs
- mouth: ivvtdwl (95 vertices)
- eyelash-l: s2x7l81
- eyelash-r: vx26b5l
- eyebrow-l: 9oetuil
- eyebrow-r: 4t6ekts
- face: hzb9442

## Stretchy Studio is Running Locally
- URL: http://localhost:8771/
- Source: /home/ubuntu/stretchy-studio/
- Can be controlled via Playwright browser automation

## Live2D Export Pipeline
- exportLive2D(project, images) → .moc3 + .motion3.json + texture atlas
- Uses OffscreenCanvas (browser API) — needs to run in browser context
- Can be triggered via Playwright on localhost:8771

## GitHub Repo
- yj000018/YOS
- Module: 03_AUTOMATIONS/modules/eya-autolive2d/
- Latest commit: d1ab647
