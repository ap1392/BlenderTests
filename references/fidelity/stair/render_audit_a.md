# Architecture A stair comparison — 2026-09-07

Inspected REF05, REF07, REF08 architecture_a renders against Wausau2,4,1. Five main differences per view below; do not regard current cameras as registered.

## REF05 lower stair versus Wausau2

1. **Geometry / critical correction to earlier research:** Huge concrete J panel obscures flight on right. Earlier identification of the L1 J double line as concrete wall was WRONG. Wausau2 shows glass at that edge; the concrete is far behind/right. Full L1 plan + hero atrium photo support concrete being the auditorium EAST curved wall, west of stair, alongside broad stair. Delete traced J concrete walls and use actual auditorium bulge around plan(680,450)→(742,482)→(760,567). Do not merely lower/shrink the J wall.
2. **Camera:** Render aims much too high; floor entry is cut off and most frame depicts upper floors. Reference has first step around90% image height, flight top around33%, and only a sliver of upper stair. Lower target and/or move camera back; preserve nearly centered frontal view of approach.
3. **Geometry:** Render bottom flight looks strongly bowed and wide in foreground with abrupt upper closure. Reference is almost straight frontal, with gentle lateral sway and curling upper end. Camera alignment must be fixed before judging width; retain actual ~1.9m plan approach, do not widen based on wide-angle crop.
4. **Surrounding geometry:** Reference elevator doors lower left, wood-paneled recessed entrance behind right, dark office frontage upper left. Render shows blank walls and heavy white undersides; add verified elevator/door and recess positions after auditorium relocation.
5. **Lighting/material:** Render is very white and flat with unnaturally uniform gray risers; reference white terrazzo retains restrained warm grain, wood ceilings are much darker, side LEDs visible but subtle. Broad white surfaces need tonal separation, not stronger emission.

## REF07 upper elevation versus Wausau4

1. **Geometry / critical:** Apparent helix handedness reversal. Reference dominant front ribbons slope DOWN left→right; render front ribbon slopes UP left→right. Verify direction of ascent around circle. Merely rotating camera cannot reverse the near half's slope. Current code increments angle as height rises; compare mirrored handedness while keeping landing angle fixed.
2. **Camera:** Render is too close and aims too high for source's stacked three-level elevation. Reference has roughly three front ribbon sweeps and compact floor span; render top is dominated by cropped soffit, middle has one huge ribbon. Move farther from center and fit vertical framing after handedness correction.
3. **Geometry:** Reference smooth ribbon transitions into broad floor junction with no sharp triangular connector sticking left. Render large angular bridge tongues / planar wedges at left are conspicuous. Integrate landing connection into gallery slab and smooth clean exposed underside junction.
4. **Geometry/detail:** Render glass has a forest of regularly repeated clamps and too many small panels. Reference uses larger radial panes, around several treads per pane, with sparse circular rail fittings. Current one panel per tread / two clamps per panel reads engineered differently. Match Wausau1 joints to roughly 3–4 treads per pane as a visual starting point, not measured fabrication spec.
5. **Architecture/material:** Background office doors and bands are sparse/untextured, source has textured charcoal carpet, gray office partitions, green doors, visible signs. Stair white is too bright to read cross-section and hides LEDs; source shaded white ribbon has substantial contrast.

## REF08 overhead versus Wausau1

1. **Camera / critical:** Camera nearly touches tread/guard. Render contains one huge close flight, source contains more than two full turns with central void and ground furniture. Reposition farther away / above the stack, aim through central well, then fit 2+ turns.
2. **Camera orientation:** Reference views diagonally across circle so treads occupy arcs in alternating upper/lower quadrants. Render aims nearly perpendicular to a single tread, making radial strips nearparallel. Increase lateral offset only after lifting camera, and avoid camera sitting on a stair surface.
3. **Geometry:** Render reveals angular stair landings/sidewall joins. Source continuous smooth white inner/outer edges through pauses. Broad intermediate flats are correct in principle, but do not make visible stepped polygon corners in ribbon silhouette.
4. **Detail:** Some rendered landings carry eight parallel lines, whereas reference groups are predominantly three lines at tread edges. Avoid unsupported repetitive landing stripes; Wausau1 should guide each visible landing pattern.
5. **Material/rail:** Glass is nearly invisible and white surfaces nearly clipped. Source has subtle green glass edges, gray metal rail below top, warm LED lines, discernible terrazzo. Render handrail is huge solely because camera is too close; do not resize rail before camera repair.

## Superseded research

`findings.md` and `lower_stair_trace.json` initially labeled a double-line J as concrete wall. That identity is deprecated by this multi-view comparison. The traced XY points remain valid image coordinates; their object identity does not. Concrete should instead be the auditorium east boundary, pending camera-fit confirmation.
