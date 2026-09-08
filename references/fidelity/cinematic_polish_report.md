# Finite cinematic polish — 2026-09-07

The existing post60 architecture remains the foundation. No reconstruction restart. The post60 master is preserved in `blender/backups/ISEC_post60_before_cinematic.blend` and its twelve reference comparisons remain unchanged as baseline evidence.

## Accepted bounded changes

- Revision62 separates satin white architectural enamel from plaster, refines oak grain scale and contrast, reduces carpet mottling, reduces terrazzo relief, adds shallow concrete roughness variation, and clears the glass tint/roughness while preserving its paired surfaces and radial normals. Daylight background changes from0.16to0.19; exposure remains0.7 across cinematic shots. The concrete bitmap remains an AI reconstruction, not a site scan.
- Revision63 replaces the eight prominent magenta chairs' disjoint back/pedestal with a continuous upholstered shell and a dark seat. The silhouette follows visible reference features; dimensions and manufacturer remain unverified.
- REF03/04/05 polish62 previews and REF09 polish63 preview were inspected against the existing material/furniture issues. Improvements are restrained; this remains architectural visualization, with simplified workstation equipment and inferred hidden details. There is no claim of photographic equivalence.
- Six12-second camera moves at24fps yield72seconds. They emphasize the atrium, lower stair, upper spiral, one documented social hub and the stair well. The upper lounge reveal was rejected because it prominently exposed repeated inferred mural/context details. The full reference-camera set is retained.
- Upper-ribbon camera was moved away from the lab glazing. An inside-glass trial was rejected because a mullion occluded the subject; the accepted track is on the atrium side. This is a stabilized camera-rig move, not a claimed pedestrian route. The overhead track likewise represents a supported cinematic rig.

## Verification and limits

The camera clearance audit samples150 keyed positions against evaluated visible mesh/curve surfaces with a0.15m radius. The accepted tracks report zero proximity issues. This does not certify every interpolated frame, camera frustum, building accessibility or Unreal import. Complete moving-image review remains required.

The first cinematic64 preview batch was invalid because Blender's timeline camera markers overrode the requested still camera. The preview helper now temporarily clears and restores marker bindings; corrected65views and subsequent66/67adjustments are the review evidence. The invalid diagnostic images are retained, not presented as deliverables.

See `cinematic_confidence_map.md` for feature-by-feature evidence and uncertainty. HIGH confidence describes supported architectural relationships, not survey-grade dimensions. Exact roof openings, balcony curves/joints, complete mural artwork, concealed stair construction, product attribution and exterior-building placement remain approximate.

## Delivery status

Final Blender polish is saved by67_capture_cinematic_master.py. All five Cycles hero stills are complete at3840×2160,256samples,16-bit PNG, and visually reviewed in renders/cinematic/cycles_heroes. The background render exited normally.

Unreal 5.8.2 is installed. Eight representative fixtures passed scale and bounds checks. The persistent graphical editor imported all 203 architecture batches, with bounds agreeing with the Blender source within 0.02 cm. Independent FBX checks found zero collapsed UV triangles. An extended normal audit localized zero corner-normal entries to 306 microscopic furniture triangles across 26 batches. The Unreal scene now rebuilds weighted normals and tangents for those batches; all other architectural custom normals are retained. Source FBX normal warnings remain documented rather than being relabeled as a passed source-normal audit.

All 43 current Unreal materials passed the actual material compiler check. The glass uses a newly compiled thin-translucent material; rendered calibration remains pending. The presentation map and 72-second Sequencer asset exist, with 203 architecture actors, 159 source-derived lights, and six CineCameraActors. Explicit actor transform checks preserve the validated Blender coordinate conversion.

Three 3840×2160 MRQ atrium review iterations completed. They exposed and corrected culled single-sheet stair undersides, excessive exposure and bloom. A further daylight balance is saved and is being checked through standalone MRQ; all twelve per-shot review/final presets are saved. No completed full movie is yet claimed. Camera, lighting, glass, shading and motion review remain required before delivery. The user's quality target remains unchanged; work is staged sequentially to reduce memory pressure on the 18 GB Mac. See unreal/validation/shutdown_investigation.md for separate crash and memory observations.

## Encoded delivery update — 8 September 2026

All six native standalone final jobs exited 0. All 1,728 frames were preserved and decoded by the postprocessing audits. The 3840×2160, 24 fps, 72-second MP4 passed frame-count, duration and full decode checks. Full moving-image visual review remains pending. The earlier pending-render statements above record the calibration history; they do not describe the current encoding status.
