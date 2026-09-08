# Unreal import shutdown investigation — 7 September 2026

The user's macOS report identifies CrashReportClientEditor 5.8.2, which itself crashed in logging while LowLevelTasks::FScheduler was being destroyed. It is a secondary crash, not the importer call stack.

The originating UnrealEditor crash context for PID 6815 shows allocation cleanup from ubidi_close_64, FICUTextBiDi, Slate text layout, an asynchronous notification delegate, and FTSTicker destruction at application exit. The log saved all eight imported meshes and completed normal editor shutdown before this failure. This suggests an import notification lifetime / teardown ordering issue; it does not establish a general macOS compatibility defect or certify rendered scene correctness.

Experiment: use Epic's EditorPythonScripting keep-alive API, let the editor tick for 20 seconds after imports, then request normal exit. Crash reporting remains enabled. Results pending in smoke_editor_deferred_exit.log.

All eight mesh bounds agree with the measured axis transform within 0.01 cm. See bounds_roundtrip.json. Appearance checks remain outstanding.

The 20-second deferred exit reproduced the same Slate notification / ICU teardown crash (originating editor PID 8326). The second user report, dated 10:38:47 PDT, is the corresponding CrashReportClientEditor failure with the same scheduler/logging stack as the first. Delay alone is not a fix. Next experiment uses the corrected UV assets through the Python commandlet, avoiding Slate notification creation.

Corrected Python commandlet completed successfully: shell exit 0; Unreal reports "Success - 0 error(s), 0 warning(s)"; all eight packages saved. This establishes a working non-Slate import path. It does not prove the graphical editor or movie renderer stable. See smoke_commandlet_corrected.log.

The user's third report is Blender PID 8892 at 10:39:50, a separate startup failure from the first sandboxed full-export launch. That launch exited 139 before the log reported loading the master. The normal-runtime retry (PID 8959) loaded the saved master; the hero render is a separate process (PID 98978). This report does not establish corruption of the .blend file.

The full Blender export retry completed successfully: 203 batches, 2,426,873 vertices. Independent parsing of every written binary FBX passed vertex-count and source-coordinate bounds checks. The initial Blender startup crash did not prevent the export.

The first full import failed while reporting near-zero tangents in the first architecture batch; its FBX warning handler tried to access unavailable Slate. No architecture asset was saved. Export-copy UV repair was strengthened to validate each evaluated loop triangle, preserving source corner normals and valid UVs while replacing collapsed charts and omitting zero-area triangles. A new binary UV audit catches this before another Unreal launch.

All five Cycles heroes completed at3840×2160,256samples,16-bit RGB PNG. File headers verified and images visually reviewed. The render process exited0. All43 Unreal material assets were also created with commandlet exit0 and zero reported errors/warnings; rendered calibration remains pending.

The completed export-copy repair now passes both independent audits:203binary FBX files,2,426,873vertices, source bounds matched, zero collapsed UV triangles. The full import retry uses this validated set. Four batches needed local triangle UV coordinates to avoid floating-point collapse on microscopic seams; other valid UVs were retained.

Persistent full editor import succeeded: all203batches saved, and all mesh bounds agree with Blender within0.02cm. The commandlet remains unsuitable for batches that issue tangent warnings because its FBX warning handler requires Slate. The graphical editor handles those warnings normally and remains running. Tangent warnings are recorded in import_tangent_warnings.json for shading review; no warning was suppressed.

The persistent editor subsequently built the presentation map and six-shot, 72-second sequence. All 43 currently assigned materials passed MaterialEditingLibrary.recompile_material with empty compiler-error arrays, including the replacement thin-translucent glass material. Earlier shader problems were repaired; material appearance still requires rendered validation.

The user's memory-pressure screenshot is a working-memory warning, distinct from remaining disk capacity. An optional Blender export was stopped to avoid simultaneous heavy Blender and Unreal work. It had loaded the master but had not reported any completed export batches. The persistent Python script dialog is expected for this editor job worker and is not by itself evidence of a hang. The first 4K MRQ review is warming up; no successful finished render is claimed yet.

An extended source-normal audit identifies 26 furniture batches with zero-length normal entries, despite all UV triangles passing. The later all-smooth export-copy normal experiment was interrupted for memory pressure and is unverified. This remains a bounded shading follow-up; earlier statements about the two passed audits refer to geometry bounds and collapsed UVs, not this newer normal audit.

At 11:41 PDT the asset-building editor closed after saving the balanced-lighting map, rebuilt furniture normals, and all twelve MRQ presets. It exited with the known Slate notification/ICU teardown failure. The user supplied its crash-reporter window. The subsequent 11:42:58 report identifies CrashReportClientEditor PID 19540, again failing in logging during FScheduler teardown. It is a secondary helper failure, separate from the new standalone renderer PID 19591. The renderer's startup sample showed dynamic library loading; it subsequently began writing normal Unreal startup logs.

The initial standalone test inherited Rosetta from the system Python and was stopped before rendering. The launcher now explicitly uses /usr/bin/arch -arm64. All six native standalone 4K review shots completed with exit code 0. The final material/scene editor again failed only after successful package saves; the user's 12:01:40 report is the secondary CrashReportClientEditor scheduler cleanup failure. The three subsequent corrected standalone review shots also completed with exit code 0 (101.6, 76.3 and 88.4 seconds). This supports using the separate native standalone renderer; it does not yet certify the full movie. The full six-shot render has now started.
