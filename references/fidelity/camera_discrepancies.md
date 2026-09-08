# Twelve-camera discrepancy register

These are comparison cameras, not claims of exact photographic registration.
The current transforms and EXIF constraints are in `calibration/camera_register.json`.
The first larger diagnostic renders are retained in `renders/fidelity/large_initial`;
`renders/fidelity/large` is the later coherent set. Small named iterations retain
failed tests and subsequent corrections.

| Camera | Important corrections made | Five largest remaining comparison issues |
|---|---|---|
| REF01 Payette atrium | Clockwise helix; dimensioned story spacing; lower stair; auditorium identity/recess and occupied L2 terrace; continuous floors; parallel ceilings | Exact balcony curvature; near/far camera registration; roof aperture calibration; simplified lab furnishing; incomplete opposite-end context |
| REF02 reverse soffit | Rejected obstructed west/L3 camera; stair-side viewpoint and vertical framing shift; closed risers; four plan-aligned classroom fronts with eight doors and three columns | Soffit panel joints; precise crop/shift; ground seating layout; undercroft frontage detail; photographic contrast/depth |
| REF03 social hub | Plan-correct diagonal sink bank and closed oval island; deeper canopy; actual mural crop; specific furniture; fixture/blade clearance; finer quilting; supported seating groups | Partial original artwork; canopy curve and exact island dimensions; chair shell fidelity; office-pod enclosure shapes; exact camera position |
| REF04 write-up | Correct viewing direction; shared oak standing table; turquoise stools; closed second glazing; deeper benches | Exact structural bay registration; repetitive workstation modules; detailed task chairs; ceiling plenum/services; glass reflection strength |
| REF05 lower stair | 65 mm source lens; corrected annular landing endpoint; 1.52 m clear width; closed risers; raised concrete entry; public-facing elevator hardware | Exact lower run curvature; elevator bank proportions; generated concrete texture interpretation; recessed entry finish/hardware; full 3D camera fit beyond two anchors |
| REF06 upper reverse | 24 mm source lens; narrower framing; corrected helix and story rise | Precise camera elevation; roof crop; adjacent pod walls; ground seating density; repeated mural visibility |
| REF07 stair elevation | 58 mm source lens; higher-floor view; coherent skin/rail/glass profile; stale landing wedges integrated | Unverified beside-stair room-number attribution; background pod topology; remaining fabrication seams; room-front detail; precise camera position at glazing plane |
| REF08 overhead | 18 mm source lens; corrected L5 eye height; inferred source crop; exposure match; three nosing strips | Residual well size/position; inferred nearest-ring crop; landing angles without shop drawings; exact glass fixing layout; ground-well contour |
| REF09 ground wide | 16 mm source lens; undercroft-edge camera; closed risers; repaired ground gap; photographed cluster arrangement | Exact eye/pitch/roll; furniture silhouettes; concrete material interpretation; remaining drum grouping/scale; roof-to-stair projected relationship |
| REF10 glass elevation | 35 mm source lens; clearer southern gallery sightline; spandrel/vision/frit layers; exposed ceiling channels | Repeated rather than varied write-up stations; precise pier layout; lab service detail; reflection/contrast match; exact frontal camera registration |
| REF11 end lounge | Supported gallery camera; connected floor; corrected glass base; oak ceiling; recessed labeled portal; tall chairs/sofa | Partial exterior facade placement/extent; foreground curvature; door/room alignment; upholstered chair silhouette; fixture grouping |
| REF12 roof reverse | Fisheye projection; higher-level view; tapered triangular apertures with glazing grids | Unreported source lens/projection; exact lightwell positions; roof edge joins; adjacent pod curvature; lower-floor composition |

The major geometric failures found during this pass were corrected rather than
concealed with lighting or camera-specific object hiding. Remaining uncertainties
include inferred measurements and bounded simplifications; the renderer succeeding
is not evidence that those uncertainties have disappeared.
