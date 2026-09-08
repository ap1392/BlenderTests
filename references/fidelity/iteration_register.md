# ISEC fidelity pass — working register

This pass continues the existing Blender master. A complete pre-pass checkpoint is
`blender/backups/ISEC_pre_fidelity_pass.blend`. The existing browser is unchanged.

## Evidence added

- Primary planning sections, BCDC 2013: explicit 14 ft 6 in story increments.
  Used as a stronger dimensional constraint, with the limitation that this is a
  design-stage section rather than an as-built survey.
- Twenty-six independently photographed university views from ISEC Reflections.
- Four Wausau terrazzo manufacturer photographs and the E-31 tread/riser product.
- Payette staff stair close-up, lighting description, material/supplier credits.
- Higher-resolution published L1 plan.

## Important corrections discovered by multi-view validation

1. The original upper helix ascended in the wrong direction. It now ascends
   clockwise in the plan frame; floor connections retain the same plan angle.
2. The prominent board-formed concrete volume is the auditorium's eastern curved
   wall. An initial interpretation of the J-shaped stair-plan lines as this wall
   was disproved by ground and reverse photos and has been removed.
3. The broad stair ascends primarily east to west, with an intermediate landing;
   the prototype's north-south orientation was wrong.
4. Two newly added bridge strips initially extended into the void because their
   offset signs were reversed. The twelve-view inspection exposed this and the
   floor strips now extend into the building.
5. Gallery blades are parallel within each ceiling field. The initial fanned
   approximation was replaced. Roof apertures are tapered rounded triangles,
   rather than ellipses cut into a thin flat slab.
6. The lab frontage now has distinct spandrel, vision and frit zones, write-up
   desks and structural piers, a second closed glazed partition, and a shallow
   documented bench/shelf layer. Ground classroom frontage is closed glazing.

## Validation sequence

- `REF01_before.png`: baseline camera with a manually fitted far bridge plane.
- `REF01_geometry_01.png`: first lower-stair/broad-stair corrections; exposed
  incorrect concrete identity and insufficient near-camera constraints.
- `*_architecture_a.png`: twelve initial reference camera previews. Several
  occluded or misoriented cameras were explicitly rejected by independent audits.
- `*_architecture_b.png`: helix direction, auditorium wall and camera corrections.
- `*_materials_a.png`: first material/daylight pass, revealed overly dark lighting,
  bounding-box-scaled terrazzo grain and remaining bridge/hub framing issues.
- `*_detail_a.png`: metre-scaled textures, revised illumination, documented
  furniture families, more complete social pod and camera refinement.

A camera name is not evidence of successful registration. Camera positions, lenses,
near/far image correspondences and qualitative critiques are retained separately.

## Current interpretation limits

The floor spacing is dimensioned but design-stage. Published-plan XY scale is
still inferred near 0.10 m/pixel. Detailed stair shop drawings were not recovered.
Hidden lower-stair continuation, exact roof center/orientation, room depths and
some furniture product assignments remain inferred. Only shallow documented
views of laboratories/classrooms are modeled; unknown private interiors are closed.
The mural is reconstructed from an unobstructed detail of the actual reference
photograph, not claimed to be a recovered original artwork file.

## Later geometry and photographic-detail passes

- Material identity was corrected: prefix matching had mistakenly assigned a light
  diffuser material to some white architecture. White paint and luminous optics
  now use exact material identities. Texture coordinates use metres.
- Rebuilt write-up foreground furniture from the photographed shared standing table
  and turquoise stools; added ceiling cloud joints and exposed service channels.
- Extended wood-and-acoustic ceiling fields across end bridges and added the
  photographed rectilinear skylight glazing bars.
- Raised the stair-elevation camera one floor after reading the 401–419 sign in
  its source. Rejected the west/L3 reverse-soffit camera after a large render showed
  it obstructed by the stair; L2 camera tests produce the supported sightline.
- Large Cycles stills (1600 px, 96 samples) exposed open riser gaps left by thin
  prototype tread plates. Closed E31 terrazzo risers now span each complete rise.
- Rail, glass, light and white stair shell now share one deterministic smoothed
  height profile. Removed the unsupported eight-stripe landing pattern.
- Obsolete blockout laboratory back walls and ceilings were removed where they
  intersected the deeper, documented replacement shell.
- Coplanar 3D slab unions left visible diagonal floor cuts. Replaced them with a
  valid single connected 2D union, explicit triangulation and separate flush
  carpet surfaces. Preserved the atrium opening. Added a small western corner
  connection between existing bridge and gallery footprints.
- The L1 plan resolves the auditorium entry: the ground-bearing outer curve stops
  between plan y500 and y569 while an overhead line continues. That interval is
  now raised over a closed recessed wood frontage. The southern return remains
  ground-bearing. The 2.55 m lintel height is inferred from photography.

### Active validation status

The first large twelve-view set is a diagnostic set, not a declaration of final
photorealism. It deliberately records errors subsequently corrected. The latest
small previews are `*_geometry_e.png`; scripts 17–22 postdate the first large set.
The model still has approximate camera calibration, simplified furniture and
unsupported exterior context beyond the glazing. Do not call the reconstruction
an as-built model or the twelve cameras exact photographic registrations.

- Camera-ray inspection distinguished two apparent floor defects: the ground
  "raised inlay" was a real gap from mismatched floor boundaries; the gallery
  green slot was an 80 mm gap below the glass. The ground floor is now a single
  polygon triangulation, and the glass clearance is 16 mm.
- End portals now have actual recessed closed door openings, push hardware,
  narrow vision panels and the photographed 360–379 range label. Other floor
  digits are inferred, explicitly tagged in the Blender objects.

## Source-camera metadata recovered

The original Wausau and university JPEGs retain EXIF. Recorded in
`calibration/photographic_exif.json`: Wausau lower stair65mm, upper reverse24mm,
stair elevation58mm; university overhead18mm, groundwide16mm, glass elevation35mm,
end lounge20mm. These are Nikon full-frame captures. The roof photo records a
manual/unreported lens; its pronounced curvature is approximated with a full-frame
equisolid fisheye, not a rectilinear15mm camera.

The lower-stair camera preserves65mm while fitting approximate first-step and
upper-step vertical anchors. Camera positions and crop/shift remain inferred;
EXIF does not solve full registration. Near-window camera tests exposed clipping
of the front glass surface at the default100mm near plane, corrected with a1mm
near plane for the close58mm view.

One closed, shallow Columbus Avenue residential frontage replaces blank sky in
that documented direction. Five stories and material family are supported by the
university housing page and the actual lounge photo. Probable780Columbus identity,
49m gap, partial eight-bay extent and module sizes remain explicitly inferred.

## Cross-view geometry audit after the second large set (scripts30–38)

The twelve1800px/128-sample images exposed architectural defects that were not
accepted merely because the queue succeeded:

- Ray-cast REF05 at normalized(.5,.335) hit the L2 slab at approximately
  (1.765,-1.892,4.192). The inferred lower flight wrongly ran underneath its
  shared landing. Its upper endpoint is now the annulus mid-radius at-47degrees,
  (1.528,-1.638,H), with matching clockwise tangent. The visible northeast plan
  trace is retained. The lower clear width now matches the1.52m upper annulus.
- Deeper opaque upper-stair sidewall: bottom-.45m, top+.52m relative to the
  smoothed walking profile. This is a cross-photo calibration, not shop-drawing
  evidence. Intermediate landings remain: photographs and Summit confirm them.
- Tested a deeper whole-floor slab and rejected it because it concealed wood
  ceilings. Restored the original slab underside and added only a thin deeper
  perimeter fascia. Small comparison renders preserve both tests.
- Elevator joints and indicators had been modeled on the concealed back face.
  Public-facing hardware is now on+Y; jambs use steel, with sills and call plates.
- Concrete board-to-board definition and longitudinal grain strengthened after
  the large images read as mottled plaster. Texture remains reconstructed.
- Published L4 plan confirms a western closed double-door throat. The initial
  eastern401–419 attribution was rejected by a front-face/occlusion test. The
  western opening is modeled; the uncertain room number is not installed.
- Three southwest hero-camera tests and an intermediate test were rejected for
  losing the upper atrium to ceiling occlusion. Original REF01 retained; the
  foreground rail mismatch remains open instead of falsifying the plan curve.
- Recovered exact plan relationships for the kitchenette: diagonal sink bank,
  closed oval island about1.3x2.4m centered(-.45,-8.05), clear circulation between.
  The former shallow curved bar was replaced. The canopy curve remains a
  photograph-informed approximation; no reflected-ceiling plan was recovered.
- Write-up pendants reoriented across the corridor; bench service uprights,
  outlet plates, mobile drawer hardware and casters follow visible photo detail.

The large directory predates these corrections until explicitly rerendered.
Small latest checks use suffixes`connection32`, `fascia33`, `details37`, `plan38`.
They remain critical validation, not a claim of achieved photorealism.

## Cross-view closure and material corrections (scripts 39–48)

- Filled the kitchenette soffit and closed its returns. A preview exposed a backing
  wall covering the photographed mural plane; that intersection was corrected.
  A ceiling drum was moved clear of the canopy after an explicit overlap check.
- Rebuilt wood ceiling intervals from the continuous public-floor polygons, with
  an inset edge and recessed dark acoustic backing. Extended the roof over the
  actual gallery footprint to close an unintended sky seam in reverse views.
- Replaced the unsuccessful procedural concrete trials with a packed, explicitly
  tagged AI-generated board-formed material reconstruction. Its board scale is
  approximately 145 mm; it is not a measured scan of the actual wall.
- Rebuilt café shell chairs with a continuous seat-to-back surface.
- University photograph 026 and the L2 plan revealed that the region behind the
  auditorium parapet is an occupied terrace. Added its distinct floor footprint,
  closed meeting-room frontage and photographed dark lounge furniture family.
- The first large terrace render exposed coincident floor fascia and concrete,
  creating a false gray stripe. The queue was stopped after that completed frame.
  Insetting the terrace floor 200 mm within the 280 mm wall removed the overlap;
  the corrected preview and post48 full-resolution REF01 confirm the stripe is gone.
- Rebuilt the lower stair at exactly 1.52 m width along its revised centerline,
  replacing the earlier nearest-point deformation. It meets the upper annular
  landing at the previously verified endpoint.
- Curved glass now uses concentric inner/outer surfaces and analytical radial
  corner normals; lower-flight panels follow the full path tangent. Physical
  transmission, IOR and roughness were retained. This improves surface continuity
  but does not by itself resolve the remaining photographic glass differences.
- Added metric, face-oriented oak UVs to align grain with table lengths and vertical
  panels. Shared furniture meshes retain instancing.

Neutral and arbitrary-view checks supplemented the twelve reference cameras.
The scene scan reported 14,929 objects, twelve REF cameras and no nonfinite mesh
coordinates. These are integrity checks, not proof of architectural accuracy.
The post48 queue uses 2048 px maximum dimension and 160 Cycles samples. Earlier
large sets are preserved separately; comparison generation refuses an incomplete
queue to avoid mixing revisions. The remaining realism gap is still documented.

## Full-resolution review corrections (scripts 49–50)

Post48 REF03 exposed visible ceiling blades penetrating the circular pendant
housings. The queue was stopped at a frame boundary. Social and gallery drums,
diffusers and their corresponding light sources were lowered together, leaving
approximately 70 mm clearance beneath the blade field. Thin suspension wires now
connect the housings to the recessed backing. The clearance50 preview shows clean
circular silhouettes without wood notches.

The same source comparison showed that the custom social-chair quilt was too
coarse and inflated. Its relief was reduced from 3.5 mm to 0.8 mm, and diamond
frequency doubled on a denser shared mesh. The source supports fine diamond
quilting; exact stitch dimensions remain inferred.

## Ground frontage and furniture support (scripts 51–52)

The L1 plan resolved four classroom fronts, eight single doors and three explicit
round columns. Replaced the generic twenty-four-bay frontage and four oak leaves
with broad, lightly jointed glass fields, closed charcoal doors, pale oak surrounds
and opaque dividing zones. The frontage follows piecewise straight plan controls
rather than an offset of the upper atrium curve. Three 0.75 m columns replace four
inferred 0.56 m columns. Classroom furnishings now sit in four bounded shallow
rooms. Heights and interior furnishing details remain approximate.

A floor-only BVH ray test confirmed five unsupported magenta chairs, one per
upper-floor social group. The entire three-chair/table groups moved (+0.33,-0.63)
m to preserve spacing and achieve the plan-floor inset. The adjacent groups moved
200 mm inward to clear their nearest chair footprint. The subsequent audit found
no unsupported chair centers or cardinal 320 mm footprint samples among all 45
social bucket chairs. This was a real cross-view defect, not dismissed as camera
perspective or concealed by changing the validation angle.

## Final support checks (scripts 53–55)

The corrected ground columns exposed collisions with legacy standing stools.
Complete standing-table groups shifted 1.4 m along the frontage; the minimum
stool-to-column clearance is now 241 mm. Closed classroom doors now have actual
openings behind their narrow vision panes.

The support audit also found that the original ground slab stopped short beneath
part of the fourth classroom. Unioning the documented shallow classroom envelope
with the existing ground slab added 11.782 square metres and eliminated the gap.
The final finite-coordinate scan covered 13,956 unique meshes. Sampled support
checks covered 153 furniture items, with no unsupported sampled positions. The
scene contains 15,068 objects and twelve REF cameras. Exact audit scope and values
are in calibration/integrity_audit.json; these checks are not exhaustive collision
or code certification. Post54 is the coherent large render revision.

## Classroom furniture completeness (script 56)

Full-resolution REF02 showed that the simplified classroom seat and back pads
lacked supporting frames. Completed the existing 72 chairs with thin connected
steel legs, seat rails and back uprights. The frame is a restrained inference from
the distant photographed furniture family, not an asserted manufacturer model.
This corrects an incomplete object without changing the room layout or expanding
undocumented interiors. The subsequent coherent render revision is post56.

## Local ceiling elevations and overhead calibration (scripts 57–60)

REF09 exposed a remaining 40 mm housing/blade overlap in the ground fixture family.
Its undercroft blades sit lower than the gallery blades. Lowered complete ground
fixture assemblies 110 mm, leaving 70 mm clearance, and added thin suspension wires.
An explicit audit of all 52 circular fixtures against 1,831 ceiling-blade bounding
envelopes reports no remaining intersections. This includes both ceiling heights.

The overhead photograph contains one fewer descending turn than the previous L6
camera. Tested three camera-only candidates, retaining the source's 18 mm focal
length. Accepted an L5 eye at (0.75,-0.75,19.3034), looking at (-0.5,4.1,5.5804),
with shift (0.03,-0.04). Estimated sensor width is 36*5904/7360 mm: the source is
5904 pixels wide while other D810 photographs in the same set are 7360 pixels wide.
This is an inferred crop, not recovered original framing. The accepted view places
the bottom well near the source's lower-left position and removes the extra turn.
Its one-stop exposure compensation better matches the bright photograph; there is
no geometric change or camera-specific object hiding. The well remains slightly
undersized in projection and the match is still approximate.

Final scene audit after these corrections: 15,524 objects, 14,412 unique meshes,
twelve REF cameras, no nonfinite coordinates, and no unsupported sampled furniture
positions. Post60 is the full-resolution validation revision.

## 61 — isolated photometric wood test, rejected

Rendered REF04 in a separate Blender process using ambientCG Wood056 image maps
at the publisher's 40 cm sample scale, with restrained normal and roughness.
No live scene or master save was involved. The remapped candidate lost the
photographed directional grain and looked like flat beige laminate. Independent
visual review agreed: retain the existing material. Post60 remains the accepted
scene and twelve-view render revision.
