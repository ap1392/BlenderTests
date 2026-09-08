# Architecture A render critique — REF09–12

Compared the actual PNGs in `renders/fidelity` to the photographs listed in `references/fidelity/calibration/camera_register.json`. These are architecture previews; missing furniture and unfinished lighting are recorded as current discrepancies, not assumed final decisions. No scene edits.

## REF09 Ground wide versus Reflections 011

Camera: recognizable direction and broadly useful composition. This is not a registration match yet: real image places the stair farther left, and the public ceiling occupies much more of the upper-right foreground. Avoid scaling the stair just to fix its screen position. The actual photo contains lens distortion, but that does not explain the following architectural discrepancies.

1. **Concrete enclosure geometry:** render has a narrow, tall, nearly flat vertical blade beside the lower stair. Real 011 has a broad curved board-formed volume, spanning from behind the lower flight toward the broad stair. Its silhouette is a major failure at ground level. Match the enclosure's width and rightward sweep before refining its texture.
2. **Left foreground overhang:** render has a huge blank white wedge/underside filling the left edge. The photo has a thinner floor fascia above a dark recessed public frontage, with the glass guard visibly separated. Check the gallery slab/ground junction and camera position; do not merely darken this giant plane.
3. **Public ceiling and lighting:** the real under-lab field extends strongly over the viewer and contains many large white drum fixtures of varied diameters. Render shows a shallow wood strip with little visual structure. Add the actual extent and fixture rhythm; then light the interior through those surfaces.
4. **Ground furnishings and floor:** reference is populated by magenta high-back chairs at the stair, blue/gray wire-base lounge chairs beside oak standing counters, and white café chairs. Render is nearly empty with isolated tables and counters. Broad sweeping pale-gray floor bands are also missing or unreadable.
5. **Roof/stair refinement:** the new cone openings and spiral improve recognizability, but the visible far opening reads too three-lobed rather than smoothly triangular, with a gray cap. Real opening has three softly rounded corners and broad gently bowed sides. Stair soffit panel edges and balustrade proportions still need comparison after the camera shift.

Priority: enclosure + overhang first, then camera and public ceiling. Lighting alone will not fix the silhouette errors.

## REF10 Glass elevation versus Reflections 018

Camera: **failed for the intended reference.** The ray from `(2,-4)` toward `(2,11)` passes through the physical spiral. The reference contains no physical stair in front of the glass; its right-side stair is a reflection. The obstruction invalidates most detailed comparison.

1. **Move camera laterally clear of the stair:** start around x=8–10, maintaining a horizontal view toward the same x on the lab wall; verify the camera stands on a real gallery. Refit after moving. Do not delete or alter the staircase to clear this view.
2. **Layered lab depth:** visible render areas repeat desks and monitors against a nearly blank white rear. Reference shows blue desk dividers, chairs, a second glazed partition, white laboratory bench/shelf systems and green accents. The frontage needs this depth hierarchy.
3. **Ceiling structure:** reference has broad white suspended rafts separated by dark exposed beams and several long thin pendants. Render's ceiling is predominantly featureless white with a few thin lines. These strong horizontal depth cues are absent.
4. **Glass appearance:** reference combines dark, legible reflections with transparent interior views and white horizontal frit. Render is pale and washed out. Check interior/exterior illumination ratios before increasing glass tint; use the real opposite gallery for reflections.
5. **Spandrel and bay check:** revised blue bands are closer to the reference, but their ratio cannot be fairly verified through the obstructing stair. After relocating, measure clear/band heights against the reference's roughly 69/31 ratio and inspect whether the approximately 1.5 m bay rhythm holds.

Priority: camera relocation before further geometry inference from this render.

## REF11 End bridge versus Reflections 023

Camera: correct general corner, but render is closer to the open lounge and lacks the right-hand glazed office frontage/reflection that frames roughly one-third of the real photo. The reference looks obliquely along that glass surface toward the lounge. Move back along the gallery and rotate into the bridge; preserve the visible glass wall at right.

1. **Upper slab silhouette:** render shows a huge blank white overhead plane in the upper left. Real photo shows a curved white fascia with a recessed/chamfered underside and an open upper gallery beyond. Check for an overextended slab or camera tucked beneath the wrong part of the bridge.
2. **Missing right-hand frontage:** the actual close glass wall and dark vertical frame generate a large reflected duplicate of ceiling and lounge. The render's right edge contains a broad opaque oak leaf instead. This could be a wrong camera position or misplaced frontage. Resolve both before material tuning.
3. **Lounge/exit composition:** reference has a bright lime exit wall, glazed exterior behind magenta seating, and no giant dark horizontal band across the exterior windows. Render's heavy gray header and opaque wood inserts make this read as an internal office row. Separate the real exterior lounge glazing from the office fronts.
4. **Balustrade heaviness:** render's guard has a dense sequence of chunky vertical posts; reference mostly reads as clear panels with thin seams and small round standoffs supporting a continuous tubular handrail. Reduce bulky support visibility and refine the slab-edge attachment.
5. **Ceiling/light/furniture:** parallel blades are now appropriate, but their edge is ragged and fixtures are absent. Reference includes drum fixtures, three-head spotlight groups under the upper fascia, magenta lounge chairs and carpet with visible mottling. These are major visual anchors at this distance.

Priority: distinguish exterior lounge from office row and correct camera framing; then rail/ceiling details.

## REF12 Roof reverse versus neu_m0413673f / Reflections 026

Camera: similar elevated direction, but the spiral is too central (render roughly x=0.55 of frame; reference roughly x=0.70), and only two roof apertures are visible instead of three. Try aiming modestly toward the laboratory side (+y) to shift the spiral right, and adjust camera distance/pitch until the near opening enters the upper frame. Do not rotate the actual stair to solve a framing difference. The source also has strong wide-angle distortion.

1. **Office-side massing:** render is a uniform long wall with repetitive oak leaves and glass strips. Real photo has pronounced recessed kitchenette alcoves and curved white volumes behind the stair, with depth and large pale walls. The newly added small kitchenette details are not enough if the surrounding alcove geometry remains hidden behind a generic frontage.
2. **Gallery slab separation:** real floor fascias are crisp white horizontal ribbons with deep dark ceiling recesses above and behind. Render alternates heavy white walls and light wood undersides, making the office side too flat and repetitive. Match the actual setback and dark reveal depth.
3. **Roof placement/silhouette:** cone depth now reads, but the center mouth is angular/three-lobed and its upper aperture exposes a blank gray shape. The reference is a smooth rounded triangle with sky/daylight; three distinct apertures must be registered simultaneously before claiming roof alignment.
4. **Glazing/frontage depth:** render's laboratory side is an overly bright repetitive white grid. Reference has much darker structural bands, reflections of the spiral, and layered lit interiors. Floor-band rhythm improves, but material and interior contrast need substantial work.
5. **Ground level/occupancy:** the broad gray enclosure and bare tables still dominate the bottom. Reference shows a richer curved floor pattern, magenta chair group and white tables; ground furniture helps establish scale. The lower stair/concrete relationship is still visibly different, even allowing for the camera discrepancy.

Priority: camera yaw/pitch and office alcove massing before polishing roof material.

## Overall judgment

This pass is visibly more architectural than the original blockout, particularly the taller stories, deeper skylights and clearer glazing bands. It is still far from a photographically convincing match. The highest-value next changes are spatial: concrete volume, repeated office alcove depth, bridge/exterior glazing distinction, and removing camera obstructions. Material/lighting should follow those corrections rather than be expected to hide them.
