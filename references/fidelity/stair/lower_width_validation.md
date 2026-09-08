# Lower stair width check — current large validation

Read-only visual measurements, approximate ±4 source pixels / ±10 render pixels. Sources Wausau2 (467x700) and current REF05 (1200x1800), same aspect ratio.

| Landmark | Wausau2 | Current REF05 | Normalized comparison |
|---|---:|---:|---|
| Lowest visible tread inner span | x134–320 (~186px) | x239–929 (~690px) | 39.8% versus57.5% width |
| Top visible tread span | x180–258 (~78px) | x470–760 (~290px) | 16.7% versus24.2% width |
| Flight vertical extent | y231–641 (~410px) | y~640–1610 (~970px) | 58.6% versus53.9% height |

The source bottom width is about40% of image width, NOT13%. Current is about58%, NOT46%, when measuring the clear tread span rather than unrelated silhouette points. Exact edge selection changes a few percent but does not remove the discrepancy.

Both top and bottom widths are enlarged by approximately1.44–1.45. Bottom/top width ratio is almost identical (~2.38): perspective depth taper is already fairly close. The height is close after two-anchor fit. Therefore further fitting ONLY the two vertical anchors cannot resolve the consistent horizontal oversizing. Add left/right endpoints as constraints and test width; don't keep changing focal length and shift alone.

At fixed camera, photo-matching width is1.92/1.44≈1.33m. This is an IMAGE-derived diagnostic, not a recovered physical measurement. The plan approach endpoints(866.93,424.45)→(884.29,432.61) imply19.2pixels, or1.92m ONLY under unverified0.10m/pixel. Thus publishedplan constrains footprint shape and relative width but does NOT independently prove1.92m.

Bounded suggested test: render lower width1.50m first (-22%), keeping centerline, rise and camera stable; compare BOTH REF05 and hero before permanent adoption. A1.30–1.35m diagnostic would test the full observed REF05 discrepancy, but should not be treated as surveyed truth. Do not globally scale the upper stair or building based on this one photo.

Hero cross-check: lower flight also reads broad/heavy, but near-camera geometry and different framing make the apparent excess less dramatic than REF05. It does not support a precise43% correction independently. Keep the adjustment local and label it photo-fitted with unresolved metric scale.

## Elevator bank

L1 plan bank lies southeast of stair, fronts the atrium from the north/northwest. Existing script13 leaves at y=-6.1 with backingy=-6.28 indeed face positiveY toward public atrium. Joint/indicator meshes at y-.038/y-.151 are on the wrong side. Move visible leaf seam and hardware to+Y offsets, ensure backing remains behind, and use actual brushed metal jambs. Bank should be oriented along the diagonal plan pod rather than globally horizontal for ultimate accuracy; its exact plan center sequence lies around(836,531)→(866,514)→(894,498), inferred from the original L1 image. Current worldx3/5,y-6.1 correspondsplan836/856,541, so bank is too far south and insufficiently diagonal. Do not shift all doors blindly; trace pod edge from original plan before final placement.

## Intermediate landings / apparent wavy rail

Keep intermediate flat landings. Summit's primary structural account explicitly confirms them, and Wausau1 / university004-1 clearly show broad unstepped trapezoidal sectors. Upper L4 plan also shows three segmented groups. A constant-pitch full-turn helix would contradict evidence.

Exact16degree pauses and10.4degree treads are inferred, not dimensioned. Current regular wave can be excessive because triangular smoothing spreads each pause over15 samples while preserving a broad flat center, and camera magnifies the effect. First compare angular positions and extent of actual flat sectors using overhead photo. Preserve landings; if smoothing is changed, use a shorter monotone transition at each edge, with no local oscillation and no spline overshoot. The common profile should remain identical for white skins, rail, glass and LED.

## Subsequent raycast/connectivity correction — takes priority

Parent raycast found REF05 upper-flight blockage is L2 slab near(1.765,-1.892,z4.19). Script02 lowerendpoint(1.3,-3) passes under the shared L2 landing before reachingH. This was an incorrect inferred hidden continuation, not evidence to cut the slab.

Independent geometric calculation agrees with parent: lower must finish at upper annulus radial start section, midpoint r2.24, angle-47deg = **(1.528,-1.638,H)**. Last visible traced control(835,484)=(2.9,-.4) to this endpoint has normalized direction(-.742,-.670), nearly identical to upper clockwise tangent(-.731,-.682). This is a coherent shared stair landing, not the more distant gallery outer edge.

Redistribute existing30risers to finish atH on that annular section; retain original visible NE approach centerline. Width1.52m at top exactly matches annulus width3.0-1.48 and is a defensible first revised test (parent integrating). Re-render this connectivity correction before refining width or camera. Earlier top-width landmark in current render was affected by blockage; the nominal1.33m image-only width correction must NOT be accepted blindly.
