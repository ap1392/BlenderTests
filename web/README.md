# ISEC walkthrough

Local first-person architectural study of Northeastern University's ISEC atrium.

## Launch

Requires Node.js 22.13 or newer (24 LTS also works).

```sh
npm install
npm run dev
```

Open http://127.0.0.1:5173/ in Chrome, Safari, or another WebGL2 browser.
Click **Enter walkthrough**. WASD walks, mouse looks, Escape pauses/releases
pointer lock. Shift increases walking speed modestly. The floor buttons move
to safe gallery starting points; normal movement has gravity and collisions.
If pointer lock is unavailable in an embedded browser, drag to look while using
WASD. This is a desktop keyboard/mouse experience; touch navigation is not included.

All assets and Draco decoders are served locally. No account, API key, CDN or
hosted service is needed after dependency installation. Nothing is published.

## Validation

```sh
node tests/navigation.mjs
npm run build
```

The navigation test exercises the same Rapier character controller and the same
collision mesh used by the browser. Reports are saved in ../renders/validation.
`npm run build` creates the production bundle; `npm run dev` is the simplest local
launch command. The master scene is ../blender/ISEC_Master.blend.

## Scope and fidelity

This is a provisional, reference-based reconstruction, not a measured digital
twin. The central atrium, six levels, upper spiral, lower stair, broad stair,
curved galleries, glazed frontage and public seating are modeled. Closed office
and classroom doors remain non-interactive. No private lab interiors are invented
for exploration. Exterior context is limited massing, not a surveyed Boston model.

Read ../references/reference_sources.txt and
../references/assumptions_and_uncertainties.txt for evidence and limitations.

The browser uses a separately batched and Draco-compressed GLB. Its real-time
lighting, simplified glass and base material colors differ from the master
Cycles scene. Procedural microtextures are retained in Blender, not baked into
the GLB. The architecture and major furniture geometry share the same source.

## Implementation

- Three.js GLTFLoader + bundled Draco decoder.
- Rapier capsule character: 1.65 m eye height, 0.28 m radius, 60 Hz fixed step.
- Auto-step limited to 0.23 m; smooth collision ramps align with stair surfaces.
- Floors, railings, glass, walls, closed doors, major furniture and columns collide.
- Collision coordinates: Blender (x, y, z) maps to web (x, z, -y).
- `lib/isec/physics.mjs` is shared by the app and navigation tests.
- `lib/isec/engine.ts` handles rendering, input, lifecycle cleanup and optional
  WebMCP floor/position/walking tools. Pointer-lock entry still requires a click.
- `blender/scripts/export_web.py` preserves the master and exports temporary,
  material-batched evaluated meshes plus separate collision data.
