# ISEC presentation project

Open `ISEC_Cinematic/ISEC_Cinematic.uproject` in Unreal Engine 5.8.2.
The authoritative architecture is the existing `../blender/ISEC_Master.blend`;
this project presents its evaluated geometry, with import-specific shading fixes.

- Map: `/Game/ISEC/Maps/ISEC_Presentation`
- Sequence: `/Game/ISEC/Cinematics/ISEC_72s` — six 12-second shots, 24 fps
- Saved MRQ presets: `/Game/ISEC/Cinematics/ISEC_Review_01` through `06`,
  and `ISEC_Final_01` through `06`
- Cycles references: `../renders/cinematic/cycles_heroes`
- Confidence map: `../references/fidelity/cinematic_confidence_map.md`

The 72-second 4K movie is encoded and technically verified; full moving-image
visual review remains pending. The MP4 remains local; release upload is pending approval. The presets specify 3840×2160, TSR with eight temporal
samples, software Lumen, and modest motion blur. Hardware ray tracing and Nanite
are disabled in this Mac presentation configuration. Final presets use 64 render
warm-up samples and a higher local-light shadow cap than the review presets.

203 floor/system batches preserve source-object provenance in
`source/architecture/manifest.json`. World-space FBX vertices convert to Unreal
centimeters as `(100*x, -100*y, 100*z)`; mesh actors use identity transforms.
Eight fixtures passed a 0.01 cm bounds tolerance, and all architectural imports
passed 0.02 cm. Material slots were mapped explicitly, and 43 assigned materials
passed the actual material compiler checks.

The Blender stair soffits are thin sheets with upward face winding. Two-sided
white architectural shaders preserve their visible undersides. Twenty-six
furniture batches rebuild weighted normals and tangents in Unreal because their
FBX files contain 306 microscopic triangles with invalid corner normals; details
are in `validation/normal_warning_provenance.json`. Other imported architectural
normals are retained. All exported UV triangles pass the collapsed-chart audit.

On the 18 GB M3 Pro, run heavy Blender and Unreal operations sequentially. The
asset-building editor has a reproducible Slate notification cleanup crash at
exit, and its crash-report helper can also fail on exit. Saved assets and finished
frames survive these observed shutdown failures. Native ARM64 standalone MRQ rendered the first 4K review and exited cleanly,
with an observed peak footprint around 15 GB versus 25 GB in the editor test.
The launcher explicitly forces ARM64 because the default local Python can run
under Rosetta. All six camera views rendered successfully. Corrected lower-stair, social-hub and
stair-well views also exited cleanly after the final material and player-visibility
fixes. The full 72-second movie is encoded; complete motion review is pending.

After presets are saved and the editor is closed, run from the repository root:

```sh
python3 unreal/scripts/render_standalone.py --mode Review --shots 1
# After reviewing all six camera views and motion:
python3 unreal/scripts/render_standalone.py --mode Final
python3 unreal/scripts/encode_cinematic.py
```

The encoder refuses incomplete frame sequences and validates the encoded
resolution, frame count, frame rate, and 72-second duration. Visual review of the
whole movie is a separate required delivery check.
