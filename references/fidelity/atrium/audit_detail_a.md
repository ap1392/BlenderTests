# Detail A critique: REF09–12

Compared `renders/fidelity/REF09_Ground_wide_detail_a.png` through `REF12_Roof_reverse_detail_a.png` with the same source photographs as architecture A. This pass improves color, occupancy and the bridge geometry. It still has significant spatial and material discrepancies. No scene edits.

## REF09 Ground wide / Reflections 011

Usability: useful architectural comparison, but not a matched camera yet. The reference sees the stair farther away and farther left, with a large public ceiling overhead on the right. Render puts the stair and magenta chairs much closer to the viewer, and most of the public ceiling is a distant strip.

1. **Camera position is outside the intended public-ceiling viewpoint.** The camera should be farther toward the laboratory side and farther from the stair. As a seed, try moving from `(16,8,1.4)` toward `(20–22,12–14,1.2–1.4)` and refit target/lens using the lower stair foot and far bridge. This is an untested seed, not a measured solution. Do not shrink the stair or furniture to compensate for the current screen-size mismatch.
2. **Oversized/floating drum fixture.** A huge white disk appears suspended in the atrium near the curtainwall, around the upper-right middle of the frame. It has no counterpart there in the reference. Check whether a lounge/ceiling lamp was placed in the void or scaled much too large. Real large drums belong below the public ceiling and appear mostly at the upper-right foreground. Relocate erroneous fixtures before lighting adjustments.
3. **Lower stair/concrete silhouette remains wrong.** The curved concrete volume is now broader, but its smooth near-horizontal top and regular gray board pattern read as a low cylindrical screen. The real volume has a more asymmetric sweep and rougher board-formed surface; its relationship to the broad stair and lower flight is distinctive. Trace its visible left and right edges against the source after fitting the camera. Keep concrete grain subtle, irregular and less uniformly tiled.
4. **Chair shape/color.** Magenta high-back chairs are much too light pink and have a conspicuous hard seam/cut across their necks. Real chairs are deep burgundy-magenta with a continuous organic shell, pinched waist, broad upper ears and an integrated pedestal. The blue/gray wire-base chairs also need smoother upholstered transitions and thin metal rods. Change material to a darker red-magenta and inspect normals/shell intersections before adding more chairs.
5. **Blank left-side architecture and flat illumination.** The unbroken white wedge and dark stripe at lower left remain far simpler than the recessed frontages in the real photograph. Bright white surfaces lack the dark ceiling cavities and restrained glossy floor reflections that establish depth. Correct the façade recesses and boundaries first, then reduce uniform fill relative to daylight and local fixtures.

## REF10 Glass elevation / Reflections 018

Usability: now unobstructed and one of the best diagnostic views. It can become a convincing reference view if the visible laboratory frontage is completed. Camera placement still needs a small framing/scale fit but is no longer the main failure.

1. **The entire rear layer is missing.** Render contains repeated computer desks against mostly blank white surfaces. The source has a clear write-up strip, another glass partition, then dense white bench frames/shelves and green doors/panels. Build a shallow but convincing second laboratory layer. It need not become an accessible interior, but it must be visible through this glass.
2. **Desk population and partitions are too regular.** Every bay repeats a monitor, pale desk and nearly invisible chair. Source has taller blue/gray dividers, grouped workstations, round tables, chairs and occasional open gaps. Use fewer distinct desk groups with actual reference proportions; do not fill every glazing bay with an identical monitor.
3. **Missing frit.** The source has clearly visible fine horizontal white lines over the lower part of each clear pane. Render does not show this pattern at preview scale. Add a measured, semi-transparent frit band that remains legible without becoming an opaque white strip. The spandrel is separately blue-gray.
4. **Ceiling geometry still weak.** Source white rafts sit between dark beams and rows of thin hanging linear lights; render is a broad flat ceiling interrupted by isolated overbright rectangles. Separate the rafts from the backing, add the dark structural gaps and make pendants read as long objects, not glowing ceiling patches.
5. **Glass contrast/reflection.** Render blue bands are now recognizable, but the glass is comparatively clear and pale. Source reflects the stair and white galleries strongly, with darker mullions and lower interior zones. Verify the camera actually sees the opposite geometry in reflection, then adjust lighting balance and roughness. Do not solve this by making all glazing more opaque.

## REF11 End bridge / Reflections 023

Usability: geometry is substantially improved. The bridge now reads as a real floor around the void, and the previously giant overhead plane is gone. Still not a matched frame: source includes the right-hand office glass and its reflection, and the viewer stands farther back along that wall.

1. **Camera/right glass context.** Reposition along the corridor so a close right-hand glazed frontage occupies roughly the right third of the frame. Keep the lime end wall and exterior glazing ahead. This will recreate the source's reflected ceiling and lounge rather than a view directly across the void.
2. **Guard system too heavy.** Numerous thick vertical posts and a chunky bottom rail dominate the render. Source uses clear panels with fine seams and small circular standoffs under a slender tubular handrail. Thin/remove redundant vertical supports and make the glass edge run cleanly into the curved landing.
3. **Faceted slab and ceiling perimeter.** The curved edge visibly kinks, and blade ends form a stepped sawtooth underside. Source has a smooth white fascia/chamfer that masks most blade ends. Increase the edge curve sampling and use a continuous finish/recess strip at the perimeter; avoid exposed jagged tips.
4. **Exterior background is a black horizon band.** Source shows a nearby building through the full-height glazing. Render's very dark horizontal strip and empty sky make the lounge look unfinished and distort the interior exposure. Replace the placeholder horizon with a simple, photo-supported façade at a believable distance, or frame so the existing contextual massing covers the view. Do not add invented architecture inside the lounge to hide it.
5. **Fixtures, lime wall and furniture detail.** Drum lights look flat and faceted, and there is no three-head spotlight cluster under the upper fascia. Source exit wall is a more vivid lime with a full-size door assembly; render's door/exit sign are underscaled and sparse. Magenta seating is a small generic cluster. Correct these near-field elements because this view depends on them more than the distant atrium.

## REF12 Roof reverse / neu_m0413673f and Reflections 026

Usability: a useful overall inspection view, but the spiral is too central and only two roof openings are visible. Reference has the stair closer to the right third and three apertures. A camera correction remains necessary before inferring roof placement from this render.

1. **Office side lacks the enclosing architecture.** The render exposes bright white rectangles and broad black exterior gaps behind kitchenettes. Real image has substantial curved white volumes and deeply recessed alcoves, with dark ceilings and defined entrance openings. The mural/counter additions help identify the use but cannot replace the missing enclosure. Add the visible side returns and upper/lower boundaries of each alcove; eliminate accidental sky/horizon views through supposed walls.
2. **Camera and roof registration.** Aim slightly toward the laboratory side to move the spiral right, and adjust position/pitch to include the near aperture. Fit all three mouths to the reference simultaneously. The current central mouth reads as a lopsided three-lobed oval; smooth the three corners/side transitions only after its projected outline is registered.
3. **Laboratory depth and reflections.** The long glass façade remains a repetition of bright desk rooms. In the real view it is darker, layered and strongly reflective. Implement the corrections from REF10, then use this view to verify the cumulative effect along the full façade.
4. **Overpopulated exposed gallery edge.** Pink chairs and spot fixtures repeat along nearly every visible bay. Source seating is concentrated into specific end lounges and kitchenette hubs, leaving substantial circulation space clear. Consolidate furniture into reference-supported groups and keep the curved gallery ribbon visually legible.
5. **Material scale and lighting.** Carpet reads as coarse gray mottling at this distance; real carpet is darker and finer. White walls are clipped/featureless while ceiling wood is uniformly brown. Reduce carpet texture contrast, introduce softer occlusion in recessed areas and rebalance daylight against interior luminaires. Preserve the crisp white stair without flattening its soffit.

## Suggested order

1. Fix the floating/oversized fixture and accidental openings to the black exterior horizon.
2. Correct camera framing for REF09, REF11 and REF12; REF10 is already usable.
3. Complete shallow visible laboratory layers and office alcove enclosure.
4. Refine guardrails, smooth curved edges and correct magenta chair seams/color.
5. Re-render these same four cameras to assess improvement before adding further detail.

These four views can support the requested 8–12-view set, but only REF10 currently has a sufficiently clear framing relationship for close component comparison. REF09 and REF12 are useful broad spatial checks; REF11 needs the right-hand glass context to match its photograph.
