# Detail A stair audit — 2026-09-07

Compared REF05/07/08 detail_a against Wausau2/Wausau4/university isec_reflections_004-1 respectively. The corrected upper helix handedness now agrees with the reference. Concrete relocation removed the earlier blocking J wall.

## REF05 lower stair — five largest discrepancies

1. **Furniture placement / camera obstruction:** Three large magenta chairs occupy most of lower/right image and hide first steps. Wausau2 has a completely clear flight, with only a slim gray plant pot at lower right. Current camera lies behind a furniture cluster. Check cluster placement against plan first; move camera in front of cluster only if that position still gives the correct staircase framing. Do not use a pink-chair-obscured image as successful registration.
2. **Camera:** Flight is now much better framed vertically, but reference starts at about90% image height, ends33%; current visible bottom is around80%, top36%. Move camera slightly closer and/or shift downward once obstruction cleared. Preserve full first riser and a little floor. Reference frontal symmetry is closer than previous render.
3. **Architecture:** Missing elevator bank to lower left and dark wood-lined entry right behind upper approach. Current blank white/black bands make the space float. These are reference-visible geometry and material zones, not decoration. Locate doors from plan rather than plastering them onto arbitrary walls.
4. **Concrete/material geometry:** Auditorium wall now correctly lies behind/right, but repeated large flat gray board rectangles read as masonry strips. Reference horizontally board-formed concrete has fine grain, irregular board tones and subtle joints, with a curved overall surface. Suppress giant regular tiles and improve board-scale variation.
5. **Stair proportion/detail:** Current treads/riser faces look alternating dark-gray/white, whereas source appears nearly uniform light terrazzo with subtle nosing detail. Once camera agrees, reduce riser contrast and retain three fine dark strips atop each tread. Source has gentle approach sway and a clear continuous white sidewall; render's white at top junction appears abruptly thick.

## REF07 upper stair — five largest discrepancies

1. **Camera:** Source presents about three complete repeating front ribbon sweeps; render presents roughly two with a massive cropped soffit at top. Pull back roughly20–30% or shorten focal length from37mm toward30mm, then lower pitch so upper cropped soffit does not dominate. Keep staircase vertical axis and source portrait ratio.
2. **Geometry:** Obvious angular wedges where stair touches floor remain, and lower stringer/soffit edges have sharp kinks at flat landings. Source curved silhouette is much smoother. Keep walking landings level, but interpolate soffit/stringer slope transitions over a short interval either side; integrate connector underside into floor edge instead of a protruding triangular tongue.
3. **Background architecture:** Render repeats conspicuous pink seats/round tables directly behind spiral with very sparse glazed office fronts. Wausau4's gallery immediately behind stair has gray walls, green exit/core doors, signage, carpet and more enclosed backdrop. Current missing/too-open core zone remains important.
4. **Glass/rail detail:** Glass still has polygonal top silhouette at changes and continuous luminous edge reading brighter than source. Rail should sit below glass top with sparse round clamps; current light strip is conspicuous white rather than subtle warm cove. Smooth rail path across transitions and reduce LED energy if material pass amplifies it.
5. **Material/light:** Reference white ribbons have bright neutral faces with soft shade; render is substantially gray and low contrast against gray walls. The warmer wood ceiling is closer than before, but stairs need brighter diffuse skylight and better separation without bleaching tread detail. Assess after geometry/camera corrections; don't solve through white emission.

## REF08 true overhead — five largest discrepancies

1. **Camera/aspect:** Actual source is5904x3940 (ratio1.498); current output is square. Set source aspect, e.g1280x854. This is a registration error before geometry comparison.
2. **Camera/framing:** Source nearest inner white band extends beyond frame; three nested turns dominate and virtually no building surroundings appear. Current13mm shows entire outer top stair, gallery furniture and curtain wall. Increase focal length approximately26–32mm as an initial test, aiming to fill frame with nearest inner band; refine against reference.
3. **Camera/axis:** Source hole center is around45%width and70%height, with rings shifted progressively as they descend. Current camera is exactly on axis and creates concentric circles centered50/50. Offset camera modestly from axis and aim obliquely through well, then adjust shift/aim so ground well lies lower-left of center. Exact offsets must be rendered, not assumed.
4. **Geometry:** Current upper white/stringer curve has noticeable flattened polygon segments and a blocky flat landing corner. Reference inner band is exceptionally continuous and round. Improve interpolation through transition regions while preserving circular plan and flat treads; camera magnification will make current facets more visible.
5. **Detail/material:** Reference has groups of three very crisp dark strips, subtle green glass edges and bright almost-white terrazzo. Render repeats eight lines across broad landings and is comparatively gray. Eight-line flat landing pattern is not supported by this new reference: change to appropriate edge groups of three. Reference clearly distinguishes thin dark glass edge from metal rail; preserve that difference.

No Blender changes made by this audit.
