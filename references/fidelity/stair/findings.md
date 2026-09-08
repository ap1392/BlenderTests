> CORRECTION AFTER RENDER AUDIT: J outline is NOT established as concrete. Full-height extrusion fails actual photos. Concrete is strongly supported as auditorium east curved boundary. See render_audit_a.md. Earlier wall statements below are superseded.

# Stair fidelity audit — 2026-09-07

No Blender scene or shared script edited. New primary-source manufacturer photographs were downloaded and visually inspected. No dimensioned shop drawing was recovered; existing 0.10 m/pixel and 4.2 m floor rise remain unverified.

## New reference source

https://wausautile.com/Projects/Northeastern-University.cfm
Manufacturer identifies custom precast epoxy terrazzo tread/riser product E-31 and DePaoli Mosaic as installer. It calls the project completed 2018, conflicting with the building's 2017 opening; use for product identification, not building completion chronology.

Downloaded and visually inspected:
- wausau1.jpeg — https://wausautile.com/media/news/terrazo-northeastern-1.jpeg — near-overhead helical tread / glass / handrail detail. Three parallel charcoal strips at every nosing, cream-white terrazzo surface, warm continuous linear light at inner faces of both white stringers. Glass top is ABOVE handrail. Thin vertical panel joints and metal disc fittings.
- wausau2.jpeg — https://wausautile.com/media/news/terrazo-northeastern-2.jpeg — frontal lower stair. Long gently curved initial rise, curls near top. Sidewalls low at bottom (~0.35m estimated relative to tread, not measured); glass extends nearly full guard height. Rail mounted below glass edge with round metal fittings. White terrazzo risers; under stair has open wood-lined recess and doors behind, not solid concrete core. Concrete wall overhead is board-formed with staggered board lengths and tie dots, rather than bold regular black stripes.
- wausau3.jpeg — https://wausautile.com/media/news/terrazo-northeastern-3.jpeg — wide reverse atrium: full repeated spiral, slender ribbon soffit with three flat pauses per turn, matching curtain-wall and roof context. Strong candidate reference camera looking down from upper bridge.
- wausau4.jpeg — https://wausautile.com/media/news/terrazo-northeastern-4.jpeg — elevation close view at L4 (401–419 sign). Upper ribbon depth around ~0.8–1.0m by comparison to estimated guard height; treads stand around mid-depth, glass continues above ribbon top. All dimensional values are photo inferences, not specifications. Upper spiral repeated circular center and no central column. Glass narrower panels on circular runs, joins visible. Rail warm-gray stainless with round clamp discs. Soffit reads continuous smooth white ruled ribbon, with sparse structural/seam changes rather than many obvious radial triangles.

## Plans

Higher-resolution original retrieved:
https://www.payette.com/wp-content/uploads/2019/03/plan_northeastern_level-1-01.png
Saved plan1_original.png, 2550x1650 (existing source was 1600x1035).
plan1_original_crop.jpg is cropped (1150,590,1480,920) at original resolution then scaled 3x with white background. Existing-size crops plan1_crop, plan2_crop, plan4_crop also inspected.

L4 circular stair: outer radius ~30px, inner ~15px at 1600-wide scale. Thus current outer/inner radius ratio 2:1 is defensible. Published graphic shows three groups and three larger level segments. About 10 riser lines per group visually, but low-resolution drawing prevents authoritative count. No scale bar or dimensions.

L1 reveals lower stair is NOT broad half-circle about upper stair center. It is an elongated northeast approach curving southwest into a tighter upper hook. The thick double-line J inside it is a wall, not a filled oval. Current floor-to-L2 solid concrete core is inconsistent with both this plan and wausau2's visible open space below the board-formed wall.

Approximate trace points in **plan1_original_crop.jpg pixels** (image990x990), for reconstructing path shapes; map to original1600-wide coords with x=(1150+cropx/3)*1600/2550, y=(590+cropy/3)*1035/1650. These are visual digitization, not survey:
- stair approach transverse ends: (695,260) to (778,299).
- inner ascending edge: (695,260),(660,345),(605,420),(543,496),(455,515).
- outer edge: (778,299),(738,391),(689,470),(621,550),(535,619),(465,654),(390,670),(331,650),(287,612).
- concrete wall left outline: (686,296),(600,326),(508,369),(421,424),(355,477),(337,507),(334,540),(344,566),(366,584),(391,591),(429,586).
- concrete inner return: (429,579),(446,560),(456,539),(456,515).
Do not simply extrude entire visible plan shape: section cuts and dashed/overhead information are incomplete. Match wausau2 and primary atrium photo before fixing heights.

## Construction cross-check

https://www.payette.com/projects/spiral-stair-northeastern-university-isec/
Confirms built circular plan replaced earlier two-ellipse design, three fabricated segments per full turn, supported at floor landings. https://www.payette.com/wp-content/uploads/archive/blog/2015/august/08-21-15_spiralstair/04.jpg (shop drawing) returned HTTP404, not inspected. Do not present as recovered drawing.

https://www.summitengineeringinc.com/summit-engineering-receives-2017-senh-excellence-in-structural-engineering-award/
Confirms plate stringers, tubular framing beneath treads, A-frame floor supports, radial glass, different lowest-flight geometry. Associated SENH poster URL https://www.senh.org/wp-content/uploads/2017/07/NEU-spiral-POSTER-04.21.17.jpg returned403; not inspected. Summit image links failed tool fetch, not used as geometry evidence.

https://www.lemessurier.com/news/blog-floating-in-air-the-central-staircase-at-northeasterns-exp-by-nick-cordio-pese-3/
Engineer comparison explicitly describes ISEC stringers as several feet deep, consistent with photo-derived ~0.8–1.0m total ribbon depth and possibly deeper local floor junctions. No numeric ISEC diameter or floor rise given. Avoid borrowing EXP stair geometry or hanger rods.

## Prioritized corrections
1. Trace lower stair J shape and spatially open concrete wall from plan and frontal photo, replacing broad circular navigation-driven approximation.
2. Separate upper and lower white-sidewall/guard profiles. Lower first run has tall exposed glass, while upper circular stairs have deeper opaque ribbons.
3. Make truly continuous smooth soffit without striped triangular face shading. Retain large flat intermediate landings, soften transition into slope only as photographed.
4. Terrazzo treads need THREE thin dark strips parallel to radial nosings. Warm LED ribbon inside stringer, metal rail below glass top, minimal circular clamp hardware.
5. Use wausau2 as low frontal registration target, wausau3 as reverse high atrium target, wausau4 as upper staircase-elevation target; compare proportions before small details.
