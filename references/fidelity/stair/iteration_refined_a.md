# Refined A stair audit

Read-only inspection of REF05/06/07/08 refined_a, source photographs, 01_height_stair.py, 13 refinement script, original build geometry helpers. No Blender edits.

## Implementable geometry diagnosis

**Primary angular tongues are likely OLD landing meshes, not new skin smoothing.** Original build creates `L2 stair landing connection` through `L6 stair landing connection` using literal polygon:
`[(1.48*cos(-47deg),1.48*sin(-47deg)),(3*cos(-47deg),3*sin(-47deg)),(3.5,-3.4),(1.7,-4.4)]`.
Neither 01_height_stair nor06 cleanup removes names containing `stair landing connection`; 13 only affects names `smooth spiral white stringer` and `continuous stair soffit`. Therefore existing wedges survive every refinement. Remove these stale connection meshes, reconstruct only the necessary landing bridge from actual annular terminal to gallery slab, and union or align their boundary with the slab so no triangular underside projects into void. The exposed polygon currently reads as a separate blade under the staircase.

**13 smooths only skins, not their dependent geometry.** It correctly assumes ribbon stride4 and soffit stride2 (verified helper topology), but rail, LEDs, glass and soffit-seam lines retain raw piecewise zz. This explains residual kinked bright rail/LED above smoother white. Use one common sampled smooth height profile for skin, glass-bottom/top, rail, and lighting; keep tread geometry planar. Do not repeatedly smooth existing meshes (non-idempotent). Compute smoothing once from original az/zz with endpoint constraints. A weighted convolution radius7 is a sensible first pass; apply its delta consistently to every section and associated rail sample. Glass panel edges can remain vertical seams, but their height must agree with stringer.

**Eight-line landing pattern persists in01.** Flat interval branch explicitly generates8 strips. New university overhead source supports3-line edge groups rather than uniformly spaced8. Change landing branch based on actual visible nosing position, not repeat a generic stripe field.

**Floor rise and diameter:** No new geometric measurement justifies changing H=4.4196 orD=6.0. Camera differences currently dominate apparent pitch. Keep dimensions while fitting cameras, then compare projected floor spacing against stair outer diameter.

## REF05 vs Wausau2 — five largest

1. Camera scale: first step reference y90%, render89%; flight top reference33%, render44%. The flight needs approximately27% more vertical image extent with lower anchor held. Initial lens test30→38mm, then compensate framing to move enlarged flight upward around9% of image. Do not change stair rise based on this view yet.
2. Camera/architecture composition: reference is almost entirely lower flight and immediate L2 gallery; current shows multiple upper spiral turns and very large ceiling fields. Tighter camera above should remove much of irrelevant upper volume.
3. Stale landing tongues: an angular blade is visible beneath upper connection. Remove/rebuild original landing meshes described above.
4. Lower context remains simplified: elevators now exist at left but sit in broad blank wall. Source has charcoal overhead wall/soffit, proper metal doors, and warm wood entry behind right. Add only observed wall return and door depth, not another concrete stair enclosure.
5. Stair/riser contrast is too striped: gray faces are much darker than source nearly-white terrazzo. Adjust material/light after camera fit. LED reads as bright outline; reference line is warmer and restrained. Concrete is still regular gray courses rather than subtle board-grain concrete.

## REF06 vs Wausau3 — five largest

1. Stair appears too small within frame: current shows much more width/depth of whole atrium. Start a tighter camera (19mm→~24–26mm) and fit outer-stair width at midheight; do not increase physical diameter yet.
2. Camera downward pitch/framing: reference emphasizes lower spiral and ground group while top roof occupies a modest strip. Current huge roof and foreground auditorium crescent claim large portions of frame. Adjust aim down and lateral position together, checking full spiral remains visible.
3. Lower spiral termination and gallery junction have visibly protruding angular flats; replace old landing polygons and unify railing profile as above.
4. Source ground has substantial desks along glazing and dense grouped seating; current ground looks mostly empty with undersized sparse furniture. Parent's14 furniture work may change this; re-render before further placement conclusions.
5. Background laboratory glazing remains uniform grid and flat reflection. Source has light/dark alternating occupied write-up rows and visibly deeper furnishing. Repetitive glowing orange murals on every floor dominate current right side; source does not show that repeated bright motif so prominently.

## REF07 vs Wausau4 — five largest

1. Camera floor is wrong. Current12 camera usesz=2H+1.65 (L3); source has401–419 signage and predominantly upper three turns. Raise BOTH camera and target byoneH=4.4196, keeping lens30mm and angle initially. Current lowerstair/concrete intrusion should disappear. This is more defensible than changing pitch/diameter.
2. Stale angular landing tongues remain a major silhouette mismatch; remove original connections and rebuild flush gallery attachment.
3. Rail/LED sharply change slope where white skin now curves, creating floating or detached-looking relationships. Use same smooth height profile.
4. Background source office/core wall is substantially more enclosed, with green doors and gray wall rather than transparent repetitive pink-table gallery. Confirm opaque core positions relative to plan; room labels in source are useful anchors.
5. White stringer shading still shows broad flat regions and occasional seams. Continuous normal smoothing is improved, but avoid abrupt face-angle splits within curved side surfaces. Preserve hard edges only at actual cross-section boundaries; don't blur tread edges.

## REF08 vs university004-1 — five largest

1. Camera axis still too centered. Source lower well around45%width/70%height; current~50%/52%. Aim through an offset target to place deep well lower-left, not merely pan final image. Offset camera modestly to create progressively displaced nested rings.
2. Current source-scale crop is improved, but nearest inner white band still fits mostly in frame while source nearly fills/cuts frame edges. Increase lens modestly after offset, around28→32–35mm initial test; preserve1.498 aspect.
3. Eight-line broad landing stripes conspicuous; replace as noted. Source three-line groups strong enough to use as angular registration anchors.
4. Current LED continuous cream outline is much stronger than source almost imperceptible line in bright daylight. Reduce emission/visibility to support geometry, not dominate inner edge.
5. Current inner well appears as a centered blank disk while source sees lower ground/stair contour asymmetrically. This is mainly axial camera/framing, but after changing viewpoint verify there isn't an unintended cap/landing filling the well. The open circular stair must remain uncapped.
