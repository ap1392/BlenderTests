# Camera targets and first registered-frame critique

## Exact active-photo crops

Pixel bounds use Pillow `(left, top, right, bottom)` with right/bottom exclusive. JPEG compression creates 1–3 pale fringe pixels outside some edges; these bounds follow the actual photo transition, not the outer compression halo. Cropped image copies and `crop_bounds.json` are in this directory.

| Source | Bounds | Active size / aspect |
|---|---|---|
| slide-6-7-1600x900.jpg | (171,0,1429,900) | 1258×900 / 1.39778 |
| slide-7-6-1600x900.jpg | (251,0,1349,900) | 1098×900 / 1.22000 |
| slide-8-3-1600x900.jpg | (0,64,1600,836) | 1600×772 / 2.07254 |
| wausau1.jpeg | (0,0,467,700) | 467×700 / .66714 |
| wausau2.jpeg | (0,0,467,700) | 467×700 / .66714 |
| wausau3.jpeg | (0,0,467,700) | 467×700 / .66714 |
| wausau4.jpeg | (0,0,467,700) | 467×700 / .66714 |

Slide 8 has TOP AND BOTTOM white bands. Treating it as a 16:9 reference would materially distort camera fitting.

## Ten different reference targets

The following are **initial search regions, not solved camera extrinsics**. Coordinates refer to the existing model's inferred plan frame (spiral axis x=0,y=0; north laboratory side positive y; office galleries predominantly negative y). Floor levels in photos are visual estimates unless a sign identifies a floor. These positions must be reprojected after the plan corrections. Start with lens shift and level optical axis for the architectural photographs; use actual downward pitch for near-overhead documentary images.

| ID | Reference | Starting camera region / floor | Look direction / target | What it uniquely validates |
|---|---|---|---|---|
| REF01 | cropped atrium-slide-10 | east atrium gallery, x15–18,y5–8, L2 eye (current fit16.8,7.39,5.85) | west toward stair and far bridge; retain current landmark fit as seed | Lower approach + concrete + broad stair, left office gallery, full lab curve |
| REF02 | crop_slide-7-6 | close to spiral on office side, x-3–1,y-4–-1, L2/L3 eye to test | toward east lab/end portals, target roughly(13,10,8) | Huge overhead soffit, ground classroom bays, lime portal stack |
| REF03 | crop_slide-6-7 | broad southern social hub x-7–-2,y-10–-7, probably L3/L4 | north/northeast through stair, target roughly(0,4,camera_z) | Full kitchenette, blade ceiling + pendants, furniture and glass guard |
| REF04 | crop_slide-8-3 | north write-up corridor x12–18,y13–16, L2 based on concrete wall visible across void | west along corridor, target roughly(-15,10,camera_z) | Second glazing, gray piers, oak write-up table, linear lights and limited observed labs |
| REF05 | crop_wausau2 | ground lower stair foot, x5–9,y5–10, z1.6 | southwest/up initial flight, aim near(1,0,4) | Long lower flight, guard profile, open underside, concrete overhead, elevator/wood foyer |
| REF06 | crop_wausau3 | west atrium bridge/landing, x-14–-9,y2–6, likely L4 eye | east along atrium, aim(7,1,10–12) with downward framing | Reverse whole atrium, all spiral turns, floor pattern, roof apertures |
| REF07 | crop_wausau4 | east of spiral x6–10,y-2–2, L3/L4 eye (visible401–419 portal) | west at stair axis, target(0,0,11–13) | Ribbon depth, landing connections, three flights, glass vs handrail profile |
| REF08 | crop_wausau1 | immediately adjacent to spiral on office landing x1–3,y-4–-2, L3/L4 | steep downward at(0,0,camera_z-5) | Wedge treads, traction triples, broad landings, LED/stringer/guard detail |
| REF09 | neu_m041w475j.jpg | gallery overlooking ground pink group, choose x3–9,y-5–0, L3/L4 | steep downward toward ground seating cluster | Actual tulip furniture shape/layout and large terrazzo fields; validates set dressing independently |
| REF10 | neu_m0413673f.jpg | upper west end/gallery, x-16–-10,y0–5, L5/L6 | east through atrium, aim upward toward roof/stair | Ceiling aperture size/shape/depth and total enclosure; original is strongly fisheye, so use Blender fisheye or explicitly fit only central perspective crop |

Optional eleventh: `04-getting-shot.jpg`, office-side landing near spiral, downward view from upper levels. Valuable for fine rail/clamp/traction validation, but composition overlaps REF08, so prioritize the more distinct ten first.

For every target, first mark stable architecture: floor/slab intersections, curtain-wall piers, stair outer silhouette and axis, gallery edge. Fit an image's camera independently from arbitrary model proportions. A fit based on a single far-wall plane can align beautifully while foreground geometry remains incorrect.

## REF01_before.png versus cropped hero (visually inspected)

Render:804×630; hero crop approximately1149×900. Aspect is aligned. The far bridge vertical band near x~.43–.56 is a reasonable starting fit. Camera tilt is much less problematic than the old arbitrary ultrawide renders. It is still not a full geometric registration.

Five biggest differences, in repair order:

1. **Lower stair/concrete location and topology (GEOMETRY).** In photo, board-formed wall is a broad curved body at x~.30–.49, y~.55–.72, behind and to the right of the lower stair. In render the concrete is a narrow cylinder at x~.18–.27, y~.60–.83, left of the stair. Lower reference stair travels from the spiral diagonally toward the right foreground and has substantial horizontal run. Model's lower stair is almost upright in image and wrongly compact. Do not shift camera to hide this; rebuild from plans and frontal Wausau photo.
2. **Broad stair alignment (GEOMETRY).** Hero broad stair near x~.51–.56 reads predominantly frontally, with top at the near edge of the far bridge and foot toward camera; render presents its side as a long left-to-right diagonal ramp around x~.42–.60. Rotate/retrace the flight and fit the undercroft/bridge junction together. Its actual orientation cannot be repaired by focal length while keeping the facade/stair fit.
3. **Foreground gallery and office frontage (GEOMETRY plus camera validation).** Photo has a substantial curved glass guard sweeping across entire bottom, attached to a charcoal gallery on left with glass-front offices and wood frames. Render has no foreground rail, and blank gray walls. Check whether current x16.8,y7.39 camera is actually on the intended corrected gallery. Reconstruct the foreground edge before judging camera position; do not invent a free-floating camera just to align the background.
4. **Stair ribbons/roof opening (GEOMETRY).** Stair's outer-right envelope is already at roughly42–43% frame width in both images, so indiscriminate scaling is unjustified. However model shows overly exposed upper treads/flat angular landings and thin soffit, while photo reads broad smooth continuous white ribbons. In photo skylight is rounded triangular with broad white tapered reveal; render is ellipse with a conspicuous black rim/railing. Fix profiles and roof depth, retaining camera seed.
5. **Lab/ground layer and light hierarchy (GEOMETRY then SHADING).** Render facade repeats mirrored blank office doors and pink chairs, has green spherical trees behind the far wall, and missing classroom openings. Photo facade has laboratory shelf/column/linear-light layers, true blue-gray spandrels, and ground undercroft with round diffusers. Most of the generic appearance comes from missing structure. After adding layers, raise neutral daylight bounce modestly, retain black service depth above oak blades and polish terrazzo with broad gray fields. Do not fix emptiness with increased glass opacity.

Secondary camera note: Reference foreground rail and people show eye level genuinely on L2; current fit's z5.85 is defensible as a provisional L2 eye height. Reference camera's horizontal placement still needs one or more near-plane landmarks in the solve (spiral axis and foreground gallery edge), since current fit.json uses only one far bridge plane. Add those to calibration after geometry correction. The photo stair axis occupies~.32 of width vs current~.31, a modest camera/yaw difference rather than evidence of huge radius error.
