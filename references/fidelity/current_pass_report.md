# ISEC Blender fidelity pass

The subsequent finite cinematic polish is documented in
[cinematic_polish_report.md](cinematic_polish_report.md), with a separate
[confidence map](cinematic_confidence_map.md). The report below and the twelve
post60 comparison boards describe the architectural baseline; the current master
also contains the accepted material, chair-shell and cinematic-camera refinements.

The existing master was selectively rebuilt and repeatedly compared with built
photographs. This is a substantial architectural refinement, with remaining
limitations documented below. It is not a surveyed as-built model or an exact
photographic match. The browser was intentionally left at its earlier revision.

## Architectural corrections

- **Vertical scale:** 4.4196 m floor spacing, based on the explicit 14 ft 6 in
  dimension in the 2013 BCDC section. This is design-stage evidence.
- **Staircase:** clockwise upper ascent, closed terrazzo risers, intermediate
  landings, deeper white sidewalls, coordinated glass and handrail profiles, and
  three traction strips. The lower flight now reaches the shared annular landing
  instead of passing beneath the floor slab. Its clear width is 1.52 m.
- **Auditorium and terrace:** the concrete wall is correctly identified as the
  auditorium boundary. Its raised entrance segment follows the L1 plan. The area
  behind the parapet is now an occupied L2 terrace, supported by the L2 plan and
  university photograph 026. This fixed a substantial missing floor region.
- **Public floors:** continuous triangulated floor unions replace mismatched slabs
  and open seams. L2 has its distinct terrace footprint and meeting-room frontage.
- **Ceilings:** three tapered rounded triangular lightwells, parallel oak blades,
  clipped ceiling fields, recessed acoustic backing, deeper perimeter fascias,
  and roof coverage over the end galleries. Slat ends no longer pierce the fascia.
  Circular fixtures now clear the blades, with fine suspension cables.
- **Frontages:** layered laboratory glazing, spandrels and frit; a bounded write-up
  strip; closed meeting-room glazing; recessed portals; corrected elevator-facing
  hardware; and visible service uprights and cross-corridor lighting.
- **Ground classrooms:** four plan-aligned glazed fields, eight closed charcoal
  doors with oak surrounds, opaque partitions and three correctly located round
  columns replace the regular placeholder bays. Legacy standing furniture was
  moved clear of these columns; door vision strips have actual openings.
- **Social hub:** the plan-correct diagonal sink bank and closed oval island replace
  the earlier shallow curved bar. The canopy remains photographically inferred.

## Materials and specific details

Architectural glass, white steel/plaster, oak, terrazzo, carpet, metal and upholstery
were revised. Curved glass has concentric surfaces and radial shading normals;
oak grain follows the table and panel orientation. Social-chair quilting was
reduced to fine, shallow relief after full-resolution comparison. The concrete bitmap is an **AI-generated material reconstruction**
using the Wausau wall photograph as a visual reference. It is tagged in the master
and packed from `blender/assets/textures`; it is not an original scan or manufacturer
texture. The mural uses an unobstructed crop of a published photograph.

Furniture follows photographed families and layouts, including tall magenta chairs,
social buckets, turquoise stools, molded café chairs and dark terrace lounge chairs.
Two social seating groups were moved inward after a floor-support audit,
preserving their table/chair arrangement. These are custom reconstructions, not verified project-specific manufacturer CAD.
One shallow partial Columbus Avenue frontage supplies the documented exterior
character; its exact placement and building identification remain inferred.

## Validation performed

Twelve reference cameras cover the atrium, lower and upper stair, social hub,
write-up area, glass frontage, end lounge and roof. Original JPEG EXIF constrains
several lenses; positions, shifts and crops are still approximate. The overhead
camera was moved one story lower to match the visible turn count, with an inferred
sensor crop and one-stop exposure compensation for its bright source photograph. Small Cycles
iterations were compared before generating the completed post60 set: twelve
2048-pixel-maximum images at 160 Cycles samples, with denoising and per-camera
exposure. All twelve source/render comparison boards were regenerated from that
single revision and checked for dimensions and nonblank image content. Rejected camera
and geometry experiments remain available for comparison.

Neutral viewport inspection and three additional rendered viewpoints checked the
lower-stair approach, a middle-floor return and an end-to-core sightline. These
checks exposed the lower landing obstruction, ceiling-edge defects and missing L2
terrace; those defects were corrected. The final scan covered 14,412 unique meshes and found no nonfinite coordinates.
Support checks covered 153 furniture items with no unsupported sampled positions;
the closest standing-stool clearance to a corrected column is 241 mm. A separate
audit checks all 52 circular fixtures against 1,831 nearby ceiling-blade envelopes
and reports no intersections. The fourth
classroom also received the missing continuation of the ground slab.
This is not exhaustive collision or building-code certification.

## Remaining differences

- Foreground gallery curvature and complete camera registration still differ from
  the photographs, particularly in the hero view.
- Roof aperture dimensions, some office curves, mullion details and hidden stair
  fabrication dimensions remain inferred.
- Laboratory/workstation detail is intentionally bounded but visually repetitive.
- Furniture surfaces, exact fixture layouts and exterior context remain simplified.
- Texture, lighting and reflections improve architectural readability, but the
  result should still be described as a reconstruction rather than passed off as
  photography of the actual building.

The per-camera five-issue register is `camera_discrepancies.md`. Exact camera data
is in `calibration/camera_register.json`; source-specific research is retained in
`atrium`, `stair` and `visual`. Incremental scripts are a change history and should
not be indiscriminately rerun: several are intentionally one-time scene edits.

## Latest review

The completed twelve-view set was visually reviewed as a contact sheet, with
individual large views inspected during generation. No new broken landing or
fixture intersection was identified. A separate scanned-wood material trial was
rejected because its calibrated result lost the directional grain visible in the
source; it never changed the live master. The current geometry/material revision
remains post60.

The user's photographic definition of done is **not yet met**. The matched views
show substantial spatial improvement, but simplified workstation and furniture
detail, incomplete exterior context, residual camera mismatch, and uncertain
roof/balcony geometry remain visible. Those differences are listed explicitly
rather than treating successful renders or valid meshes as proof of fidelity.
