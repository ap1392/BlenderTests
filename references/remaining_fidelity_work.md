# Remaining fidelity work — after the Blender refinement pass

The Blender master is substantially revised from the prototype. The browser is
still the earlier prototype and was intentionally not regenerated in this phase.
The current Blender result remains a reference-constrained reconstruction, not
an as-built survey or an exact photographic match.

## Resolved from stronger evidence

- Floor spacing changed from 4.2 m to 4.4196 m, using the explicit 14 ft 6 in
  dimension in the BCDC 2013 section. It is design-stage evidence.
- Corrected upper-helix handedness, closed terrazzo risers, smooth white shell,
  shared rail/glass/light profiles and three-strip nosing detail.
- Reoriented the broad stair; retraced the lower approach and corrected its landing
  endpoint after ray-casting an actual slab obstruction in REF05.
- Identified the prominent concrete as the auditorium wall. Restored its elevated
  entry segment where the L1 plan and Wausau photo agree.
- Restored the occupied L2 terrace behind the auditorium parapet, including its
  distinct floor footprint, closed meeting frontage and lounge seating.
- Replaced the repeated ground frontage with four plan-aligned classroom fields,
  eight closed doors, opaque partitions and three explicitly located columns.
- Corrected bridge offsets, public slab intersections, and a ground-floor gap
  between mismatched straight and curved floor boundaries.
- Rebuilt layered lab glazing, spandrels, frit, write-up strip, documented bench
  depth, ground classroom glazing and undercroft ceiling.
- Replaced roof ellipses with three tapered rounded triangular lightwells and
  glazing grids; changed gallery slats to parallel ceiling fields.
- Added photographed furniture families, shared standing table, kitchenette,
  recessed lime portals, room-range labels and actual fixture types.
- Corrected ceiling/fixture intersections and five unsupported chairs found in
  full-resolution and floor-support audits; complete seating groups moved inward.
- Created twelve comparison cameras and repeated Cycles validation at small and
  larger resolutions. Failed camera seeds and intermediate defects are retained
  in the discrepancy history rather than described as successful matches.

## Remaining fidelity limitations

1. Published-plan XY scale is inferred near 0.10 m/pixel. No as-built stair shop
   drawings or survey dimensions were recovered. Roof centers, taper and some
   hidden lower-stair curvature remain approximate; its landing endpoint now follows
   the upper annulus connectivity constraint.
2. Camera matches are approximate. Reference subjects include cropped photographs
   and a strongly distorted/fisheye roof view. Similar framing is not a solved
   camera calibration; source/render comparisons remain the test.
3. Furniture uses manually reconstructed silhouettes and manufacturer dimensional
   candidates, not verified project-specific CAD. Upholstery, table proportions
   and some layouts still differ from the photographs.
4. Exterior context remains partial. One shallow Columbus Avenue frontage follows
   photographed character; exact placement and module dimensions are inferred.
5. Office alcove curves, exact room frontage divisions, rail-to-slab junctions,
   detailed mullions, service fixtures and finish textures can be refined further.
   Concrete now uses a tagged AI-generated texture, not a scanned site material.
6. The mural uses an unobstructed photographic crop; its original artwork file was
   not recovered. Unknown room interiors remain bounded and closed.

See `fidelity/iteration_register.md`, the three independent audit folders and
`fidelity/calibration/camera_register.json`. Large stills are validation artifacts;
render success alone does not establish the requested photographic fidelity.
