# Ground-level classroom frontage

Evidence: Payette L1 plan https://www.payette.com/wp-content/uploads/2019/03/plan_northeastern_level-1-01.png (local references/fidelity/stair/plan1_original.png), and built photograph https://www.payette.com/wp-content/uploads/2018/10/slide-7-6-1600x900.jpg (existing source for REF02). New crops: `ground_frontage_L1_grid.jpg`, `ground_frontage_REF02_crop.jpg`. University022 provides another built view of the same ground frontage.

The actual frontage has **four classroom glass fields and eight single door openings, two per classroom**, with thicker opaque zones at dividing partitions. The current script02 substitutes 24 regular bays and only four pale-oak leaves. The photo shows **dark gray leaves with narrow light vision panels, pale oak vertical wall/jamb panels, large clear glass fields, and white round columns**. Pale oak is not the finish of the whole door leaf.

The classroom face is piecewise nearly straight, not a uniform offset of the upper atrium glass. Approximate plan control points run (650,330) → (740,311) → (837,297) → (928,294) → (1016,294). Use the actual plan frontage line and interpolate y locally when constructing the aperture edges below. Coordinates are common 1600 px plan coordinates; +/- 1–2 px measurement uncertainty applies.

| Classroom west→east | West door opening, pixels | Main glass field, pixels | East door opening, pixels |
|---|---|---|---|
| 1 | (656,329)→(665,327) | (665,327)→(723,315) | (723,315)→(732,313) |
| 2 | (750,310)→(759,308) | (759,308)→(816,301) | (816,301)→(825,299) |
| 3 | (845,298)→(854,297) | (854,297)→(913,294) | (913,294)→(922,294) |
| 4 | (938,294)→(947,294) | (947,294)→(1005,294) | (1005,294)→(1014,294) |

These glass intervals exclude the door apertures but not every small photo-visible timber reveal. Do not claim the plan separately identifies oak panel width: material and panel extent require inference from the photograph. Each door is roughly 0.9–1.0 m wide by the established scale. The plan door swings project into the atrium-side circulation; a closed leaf preserves the room boundary without inventing accessible interiors.

Opaque front zones between door pairs occur around (732,313)→(750,310), (825,299)→(845,298), and (922,294)→(938,294). They connect to actual classroom partitions. The central partition at x837 is drawn particularly thick. Keep these opaque rather than glazing through the partitions. Their outer portions may be timber-clad rather than raw concrete; the photo supports pale oak beside dark door leaves. End return walls near x650 and x1016 should also remain opaque.

Convert any point by X=(px-806)*0.1, Y=(480-py)*0.1. Example main glass3: (4.8,18.3)→(10.7,18.6); doors3 centers approximately (4.35,18.25) and (11.15,18.6).

## Round columns

Three unequivocal round columns in the published L1 frontage band have centers:
- (745,334) → (-6.1,14.6)
- (837,321) → (3.1,15.9)
- (929,317) → (12.3,16.3)

Their drawn diameter is about 7–8 px, roughly 0.7–0.8 m at the common scale. Photo columns are white/pale concrete. Current script02 generates four columns from resampled offset positions with 0.56 m diameter; those placements and diameter are not faithful to the explicit plan. Check earlier/further-west objects before deleting by count, but these three plan positions should govern the visible frontage.

## Height and interior

Photo REF02 shows a low white soffit/header above the classroom glazing and full-height pale oak panels to that soffit. Exact height is not dimensioned here; current 3.05 m glazed height is plausible but not verified. The broad clear openings reveal ordered classroom table/chair rows. Script03 places generic rows without classroom partition alignment; assign visible furnishing subsets to the four bounded rooms and avoid extending rows through the opaque dividing walls.

Do not add raw-concrete rectangular piers behind every metal glazing mullion. The ground reference uses sparse white circular columns and opaque classroom boundary zones. Metal joints in the clear fields should be much less visually dominant than the upper laboratory curtain-wall grid.
