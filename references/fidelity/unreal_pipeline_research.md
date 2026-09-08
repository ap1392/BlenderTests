# Blender ISEC → Unreal on macOS: bounded pipeline research

Research 2026-09-07. Official Epic documentation only. No scene or project edits; Unreal is not installed yet, so no API or import has been executed. General docs resolved to5.8; several Python 5.8 class URLs failed, so Python class references below are explicitly 5.7 and require a small installed 5.8 smoke test.

## Recommendation

Use **logical FBX mesh batches + an authoritative JSON manifest**, with shared prototype assets and explicit placements. Keep Blender master unchanged. This recommendation is an engineering inference from the scene's15,524 objects, shared furniture data, procedural shaders and18 GB memory—not an Epic-prescribed architecture.

- Export evaluated geometry from temporary copies: realize curve bevels and modifiers, retain split/custom normals, triangulate intentionally. Group static architecture by floor, system and material where editing permits. Keep transparent glazing separate; keep stair skins and railings independently identifiable.
- Export shared furniture prototypes once; record every instance transform and material override. Rebuild placements inUEusing shared StaticMesh assets, preferably instanced components for repetitive static items. Do not import15,524independent assets or one enormous Blueprint with15,524components.
- Manifest should contain stableobject/prototypeIDs, sourcecollection/floor, localmeshasset, parentID, local/worldmatrix, materialslotIDs, visibility, bounds, units, exportaxisbasis, camera matrices/sensor/focal/shift andlightsettings. Use manifest IDs for idempotent import/update.
- Import in bounded batches; save and log asset paths after each. Geometry-only roundtrip first:1 m calibration cube, asymmetric XYZ axis fixture, stairskin, curve handrail, two instances of one chair, glass pane. Require exact scale and bounds, orientation, normals, material slots and instance count before the full scene.

Epic's FBX pipeline supports separate meshes, smoothinggroups, UVsets andcustomcollision, usesFBX2020.2, and recommendscontrolledtriangulation. A different exporterFBXversion needs this smoke test. [FBX Static Mesh Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine)

Hierarchy is deliberately reconstructed from the manifest; ordinary asset import does not recreate the level hierarchy. Epic's full FBX scene import supports cameras, lights and hierarchy, but full scene reimport requires one Blueprint. That's less attractive for this large automated scene. [FBX Scene Import](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-scene-import-in-unreal-engine)

## Formats compared

| Format | Fit for this task |
|---|---|
| FBX+manifest | Recommended controllable nativeStatic Mesh pipeline, explicitnormals/scaleoptions, easyper-asset reimport. Materials andcamera optics needseparate reconstruction. |
| glTF/GLB | Good alternate baked PBR scene exchange through Interchange. Useful smoke test or comparison, butnot a transfer of Blender procedural nodes; material coverage must be checked. |
| USD | Strong hierarchy/references/layers alternative. Epic USD Stage workflow can retain hierarchy and access animation in Sequencer, but is documented Beta and requires USD Importer. Adds another translator and stage lifecycle to a memory-limited single machine; keep as a future archival or interchange option rather than the first import. |

Epic's Interchange docs expose custom Python pipelines; asset naming and options differ fromlegacy FBX. Its pages are internally inconsistent about FBX status (one labels it Experimental, another lists FBX Import Into Level). Verify the installed importer and do not assume FbxImportUI options affect Interchange. [Interchange](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-assets-using-interchange-in-unreal-engine), [Import reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/interchange-import-reference-in-unreal-engine), [USD quick start](https://dev.epicgames.com/documentation/en-us/unreal-engine/usd-stage-editor-quick-start-in-unreal-engine)

## Material transfer

Rebuild a small UE master-material library (paint,terrazzo,wood,concrete,carpet,fabric,metal,glass,emissive) and driveinstancesfrom the manifest. Bake authored procedural color, roughness and normals to UV textures where appropriate; use analytic UE shaders for glass, metal and simple paint. Material slot assignment must use stable IDs. Do not promise the Cycles/AgX look will transfer; lighting, exposure, color transform and reflections need UE calibration. FBXsceneimport's material support is basic and may not match DCC appearance. [FBX Scene Import](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-scene-import-in-unreal-engine)

## Verified import APIs (5.7 class docs; smoke-test 5.8)

`AssetImportTask`: filename,destination_path,destination_name,automated,options,factory,save,replace_existing; use`get_objects()`or`imported_object_paths`, not deprecated `result`. Interchange ignores destination_name unless naming is set in its pipeline. [AssetImportTask](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AssetImportTask?application_version=5.7)

Suggested legacy-FBX task skeleton, authored for this project (not executed):

```python
import unreal
opts = unreal.FbxImportUI()
opts.automated_import_should_detect_type = False
opts.import_as_skeletal = False
opts.import_mesh = True
opts.import_materials = False
opts.import_textures = False
opts.import_animations = False
opts.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
sd = opts.static_mesh_import_data
sd.combine_meshes = False
sd.convert_scene = True
sd.convert_scene_unit = True
sd.import_uniform_scale = 1.0
sd.transform_vertex_to_absolute = False
sd.bake_pivot_in_vertex = False
sd.normal_import_method = unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
sd.auto_generate_collision = False
sd.build_nanite = False

task = unreal.AssetImportTask()
task.filename = source_fbx
```

The task setup continues with`task.destination_path`, `task.automated=True`, `task.options=opts`, `task.factory=unreal.FbxFactory()`, `task.save=True`, then`unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])`. The legacy factory selection must be checked in 5.8; if Interchange intercepts, use a project-specific Interchange pipeline or explicitly test the FBX feature flag before full import. Do not mix both option models.

Normal/unit/pivot options are documented in[FbxStaticMeshImportData](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FbxStaticMeshImportData?application_version=5.7); mesh/material/type flags in[FbxImportUI](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FbxImportUI?application_version=5.7). Treat unit conversion as one operation: the calibration cube must be 100 UE centimeters, not 1 or 10,000. Manifest transforms need the same basis and unit mapping as meshes; do not multiply translations twice.

## Camera sequence automation

Enable Python Editor Script Plugin, Editor Scripting Utilities, Sequencer Scripting and Movie Render Queue features. Python is Editor-only. Use startup scripts orExecutePythonScript for import and setup; command-line Python exits after the script, so asynchronous MRQ must not be abandoned when the process ends. The commandlet does not automatically load a level. [Editor Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)

The current 5.8 Sequencer guide explicitly documents:

```python
at = unreal.AssetToolsHelpers.get_asset_tools()
seq = at.create_asset('ISEC_REF01', '/Game/ISEC/Sequences',
                      unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
seq.set_display_rate(unreal.FrameRate(24, 1))
seq.set_playback_start(0)
seq.set_playback_end(24)
unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(seq)
ls = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
camera_binding = ls.create_camera(spawnable=True)
```

`create_camera` creates a camera binding and camera cut track. `binding.add_track(unreal.MovieScene3DTransformTrack)`, `track.add_section()`, `section.set_range(start,end)`are documented. For fixed reference views, prefer one Cine Camera actor and cut per sequence, with manifest transform and optics; verify the spawned-actor resolution API in the installed editor before keying. [Sequencer Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-scripting-in-sequencer-in-unreal-engine)

CineCameraComponent exposes filmback and current_focal_length; transfer actual sensor width and height along with focal length, not focal length alone. Blender lens shift and fisheye cameras need explicit projection matching; do not assume FBX camera import preserves them. [CineCameraComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/CineCameraComponent?application_version=5.7)

## MRQ automation APIs

Use Editor `MoviePipelineQueueSubsystem`, not runtime `MoviePipelineQueueEngineSubsystem`. Documented calls:

```python
sub = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
queue = sub.get_queue()
job = queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
job.job_name = 'ISEC_REF01'
job.map = unreal.SoftObjectPath('/Game/ISEC/Maps/ISEC.ISEC')
job.sequence = unreal.SoftObjectPath('/Game/ISEC/Sequences/ISEC_REF01.ISEC_REF01')
cfg = job.get_configuration()
out = cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
out.output_resolution = unreal.IntPoint(1600, 1200)
out.output_directory = unreal.DirectoryPath(render_directory)
cfg.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
executor = sub.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
```

This is asynchronous; keep the editor running and register completion and error callbacks. Do not delete other existing queue jobs—allocate a dedicated queue or track only task-owned jobs. API references:[QueueSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineQueueSubsystem?application_version=5.7), [Queue](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineQueue?application_version=5.7), [ExecutorJob](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineExecutorJob?application_version=5.7), [OutputSetting](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineOutputSetting?application_version=5.7).

## M3 Pro18 GB constraints and first milestone

Epic 5.8 Mac requirements: Sonoma 14.5 minimum; Xcode 26.0 minimum, 26.1.1 recommended; 26.4 incompatible. Memory 16 GB minimum / 32 GB recommended. M3 meets the processor recommendation but 18 GB is below recommended memory. Software Lumen works on M1+; hardware Lumen and MegaLights are not currently supported; Nanite and VSM require M2+ and are Beta. [Mac requirements](https://dev.epicgames.com/documentation/en-us/unreal-engine/macos-development-requirements-for-unreal-engine)

Start with software Lumen, deferred rendering, moderate viewport resolution and one reference camera. Keep Nanite off for the initial proof; enable selectively after checking Mac behavior and mesh cost. Avoid simultaneous Blender Cycles rendering and UE shader compilation or import. Stage geometry, furniture and material batches; prefer shared 1K/2K textures before 4K. These are memory-management recommendations, not benchmarked limits.

First completion checkpoint: installed UE version and Xcode verified; smoke-test assets correct; one atrium floor and one instanced chair family; one Cine Camera Sequencer cut; one MRQ PNG successfully written; then the full scene. No UE rendering claim until this actually runs.

## Standalone MRQ preparation

Epic documents command-line rendering with a saved MoviePipelinePrimaryConfig asset, -game, -LevelSequence and -MoviePipelineConfig. We will use saved per-shot 4K presets in separate sequential processes, closing the asset-building editor first to avoid a duplicated editor/PIE world. A 640×360 runtime window does not set output resolution; the MRQ preset explicitly specifies 3840×2160. This is a memory-management experiment, not yet validated as a successful render.

Source: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-command-line-rendering-with-move-render-queue-in-unreal-engine
