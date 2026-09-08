# ISEC reconstruction — Blender and Unreal cinematic

Start with **[the editable Blender master](blender/ISEC_Master.blend)**. This repository contains the existing Northeastern ISEC reconstruction, its textures, the Unreal presentation project, the earlier interactive web prototype, and supporting reference and fidelity documentation.

![Atrium rendered in Blender Cycles](renders/cinematic/cycles_heroes/CINE_01_Atrium.png)

## Download and explore

| Deliverable | Repository path / download |
|---|---|
| Authoritative Blender scene | [blender/ISEC_Master.blend](blender/ISEC_Master.blend) |
| Textures and other Blender assets | [blender/assets](blender/assets) |
| Earlier Blender checkpoints and scripts | [blender](blender) |
| Complete Unreal project | [unreal/ISEC_Cinematic](unreal/ISEC_Cinematic) |
| Unreal project entry point | [ISEC_Cinematic.uproject](unreal/ISEC_Cinematic/ISEC_Cinematic.uproject) |
| 72-second 4K cinematic MP4 | [Download the 4K MP4](https://github.com/ap1392/BlenderTests/releases/download/isec-cinematic-v1/ISEC_72s_4K.mp4) |
| Five Blender Cycles 4K hero stills | [renders/cinematic/cycles_heroes](renders/cinematic/cycles_heroes) |
| Earlier interactive browser prototype | [web](web) |
| Exported browser model | [web/public/models/ISEC.glb](web/public/models/ISEC.glb) |
| Reference images, sources and research | [references](references) |
| Confidence map and approximations | [cinematic_confidence_map.md](references/fidelity/cinematic_confidence_map.md) |
| Unreal rendering workflow | [unreal/README.md](unreal/README.md) |

Clone or download the repository to retain the relative asset folders. Open the master with **Blender 5.2.1 LTS**, the version used for this work. Keep `blender/assets` alongside it. Open the complete Unreal project with **Unreal Engine 5.8.2**; its `Content` and `Config` folders are required alongside the `.uproject` file. The presentation map is `/Game/ISEC/Maps/ISEC_Presentation` and the sequence is `/Game/ISEC/Cinematics/ISEC_72s`.

For the earlier browser prototype, see [web/README.md](web/README.md). It predates the final Blender cinematic pass.

## Delivery status

The Unreal movie has been encoded and technically verified at **3840×2160, 24 fps, 72 seconds, 1,728 frames**. All six standalone rendering jobs exited successfully. **Full moving-image visual review remains pending**; this is not a claim of final visual approval. The five Cycles hero stills are 4K, 256-sample renders from the Blender master.

The complete raw image sequence is preserved locally at `renders/cinematic/unreal/frames`, but excluded from Git because it is approximately 17 GB. The MP4 and its SHA-256 checksum are available in the [cinematic release](https://github.com/ap1392/BlenderTests/releases/tag/isec-cinematic-v1). Generated caches, dependencies, temporary jobs and crash logs are also excluded. No local source files or raw frames are deleted by these exclusions.

This is a reference-informed architectural reconstruction, not an as-built survey. See the confidence map for inferred dimensions, hidden details and material approximations. Do not rerun `blender/scripts/build_isec.py` to open this model: it is the original destructive prototype builder. Open the saved master instead.

## Local setup

The original workspace is `/Users/aditya2610/Desktop/Projects3/BlenderTests` on the author's Mac. On another computer, use the folder where you cloned the repository. Some production scripts still contain author-machine paths and should be inspected before reuse.

## Workflow

Describe the object or scene you want in this Codex task. Codex can write Blender
Python scripts, run them with Blender, inspect the rendered images, and iterate.
The resulting `.blend` files can be opened and edited normally in Blender.
This workflow uses Blender's bundled Python (`bpy`); no separate Python package,
API key, or Blender MCP add-on is required.

## Commands

Run these from this folder:

```sh
# Verify the installed version
./blender.sh --version

# Rebuild the setup verification scene and render
./blender.sh --background --python-exit-code 1 --python scripts/setup_check.py

# Open the editable scene on macOS
open -a Blender output/setup_check/setup_check.blend
```

`blender.sh` uses `/Applications/Blender.app/Contents/MacOS/Blender`.
Set `BLENDER_APP` if you move Blender to a different location.

## Files

- `scripts/setup_check.py`: reproducible studio scene with a cube, sphere, and ring.
- `output/setup_check/setup_check.blend`: editable scene, camera, lights, and materials.
- `output/setup_check/setup_check.png`: rendered preview.
- `output/setup_check/setup_report.json`: Blender version and rendering device used.

The setup check rebuilds its own output files. Keep future projects in separate
subfolders so rerunning it does not overwrite your work.

## References

- [OpenAI's Blender workflow](https://developers.openai.com/blog/architectural-visualization-with-astra)
- [Blender Python API](https://docs.blender.org/api/current/)

## Blender MCP integration

Installed the community `ahujasid/blender-mcp` package 1.9.1 from source commit
`c5f35d9cc54451d785ac4c00c48bf9e98a2e8db9` into `integrations/blender-mcp-env`.
The source checkout is in `integrations/blender-mcp`.

Codex's global MCP configuration has an enabled `blender` entry pointing to the
environment's absolute `bin/blender-mcp` path, with `DISABLE_TELEMETRY=true`,
`BLENDER_HOST=127.0.0.1`, and `BLENDER_PORT=9876`.
Keep this project folder in place so the configured command remains valid.

The add-on is installed at
`~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py`, enabled
in saved Blender preferences, and running on localhost port 9876. Its telemetry
consent is disabled. Optional asset services remain disabled.
Keep Blender open for MCP requests. The add-on defaults to starting on launch;
its connection can also be managed in the viewport sidebar's MCP for Blender tab.

Verified using a real MCP client: initialization, discovery of 28 tools, and
`get_scene_info` returning the nine objects in the setup scene. Report:
`output/setup_check/mcp_report.json`.

To repeat the read-only check (avoid simultaneous clients):

```sh
integrations/blender-mcp-env/bin/python scripts/check_blender_mcp.py
```

The current Codex conversation's tool inventory may need a refresh before the
new MCP tools appear directly. Restart Codex if they are absent. The integration
itself has already been verified through the MCP client above.

## ISEC reconstruction

Current fidelity report: [references/fidelity/current_pass_report.md](references/fidelity/current_pass_report.md).

The refined editable master is `blender/ISEC_Master.blend`. This fidelity pass
continues the original project, with architectural corrections, reference-specific
furniture/materials and twelve comparison cameras. Current large Cycles validation
images are in `renders/fidelity/large/`; paired reference/render boards are in
`renders/fidelity/comparisons/`. The earlier diagnostic set is retained in
`renders/fidelity/large_initial/`.

Start with `references/fidelity/iteration_register.md` and
`references/remaining_fidelity_work.md`. Camera transforms, source links and EXIF
are recorded under `references/fidelity/calibration/`. Research and independent
critiques are under `references/fidelity/atrium/`, `stair/` and `visual/`.

The sequential refinement scripts are in `blender/scripts/fidelity/` and packed
as Blender text blocks. Some are one-time migration steps; do not rerun the entire
folder blindly. `build_isec.py` remains the original destructive prototype builder.
Open the saved master to continue. Earlier checkpoints are in `blender/backups/`.

The model remains reference-constrained, with documented uncertainty in unmeasured
geometry, camera registration and some furniture/detail. It is not an as-built
survey. Unknown room interiors remain bounded and closed.

The browser under `web/` and the original `renders/final/` are the earlier
prototype. They were intentionally not regenerated during this Blender-focused
phase. The original local browser launcher and navigation tests remain available.
