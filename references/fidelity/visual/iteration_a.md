# Architecture A — first four camera audits

Visually inspected each architecture_a render against source named in camera_register.json. These frames are not yet reference-matched. Separate camera problems from scene deficiencies; do not score them as geometry validation passes merely because rendering completed.

## REF01_Payette_atrium

1. CAMERA / FOREGROUND OCCLUSION: White gallery soffit covers top ~27% of frame; source exposes roof/skylight and higher stair. Camera is now behind/under foreground gallery construction. Removing lime panel did not remove this separate blocker. Determine whether that gallery actually exists at this depth in the reference plan; then relocate camera to actual gallery rail edge or correct the oversized slab. Do not hide a valid slab solely for a render.
2. CAMERA / FOREGROUND OCCLUSION: Charcoal floor and guard hide bottom~30%, with top rail near normalized y.71. Source foreground rail appears around y.86–.95 and leaves lower stair/ground seating readable. Camera height versus actual edge and its foreground distance need fitting. Combine rail top and lower stair foot landmarks with far bridge points.
3. GEOMETRY: Concrete enclosure still reads a tall close wall rather than broad lower body behind the flight. Because its lower part is occluded, this frame cannot validate last iteration's projected-height problem. Re-evaluate only after framing is repaired.
4. GEOMETRY: Office galleries still repeat glazed door bays without adequate hubs, and lab side is a uniform repetition of desks/monitors over a thin white room. Real photo has more deeply layered labs and varied write-up families. Newly added structure improves legibility, but cannot be validated behind foreground occlusions.
5. MATERIAL / LIGHTING: White shell, glass reflections and upper workspaces are excessively pale and featureless. Gray concrete and white paint merge. Source has steel blue glass/spandrels, dark ceiling service gaps, white satin stair with gray undersides and a textured concrete wall. Preserve controlled highlights rather than indiscriminate fill increases.

## REF02_Reverse_soffit

1. CAMERA LOCATION: Current(-2,-2,L2eye) sits amid the spiral/concrete enclosure. Concrete fills lower~40% and stair cuts the image horizontally. Source shows the ground lounge/classrooms broadly, with stair only in upper-left. Move outside the spiral envelope; test L3 eye as an alternative before fine fitting. The proposed floor is a test, not a known photographed floor.
2. CAMERA AIM / FRAMING: Source looks across the lab wall toward lime end portals; right office gallery is only an edge and the end bridge occupies roughly right quarter. Current right gallery dominates half the frame. Shift viewpoint and yaw to emphasize laboratory elevation and ground undercroft.
3. GEOMETRY: Concrete wall seems massively thick in current close view. Check whether visible thickness is two separate traced surfaces/overlapping caps. Real wall in frontal Wausau shot is a thin board-formed wall over an open wood-lined recess. Current cap needs dedicated section inspection.
4. GEOMETRY: Reference has integrated broad lime recesses/doors, magenta sofas and exterior end glazing. Current lime blocks remain partial portal silhouettes; floor-end bridge/slab thickness and width need matching after camera correction.
5. MATERIAL / LIGHT: Pure-white spiral dominates without sparse soffit seams or subtle curvature shading; spandrels are flat pastel teal. Source allows lab shelving and structure through clear glass, while mullions and spandrels stay dark. Keep glass clear but correct surrounding depth and light contrast.

## REF03_Social_hub

1. CAMERA ORIENTATION: Current view runs lengthwise down gallery. Source faces across a broad social alcove, with full kitchenette right third, foreground chairs left half, and staircase farther across void near center. Move/back into actual hub and aim transversely; current kitchenette clipping is primarily camera failure.
2. CAMERA FOCAL / PITCH: Current spiral occupies almost entire height and several turns; source has about one turn framed below a large ceiling field. After location is fixed, aim nearly horizontally and test tighter24–28mm lens, using ceiling boundary and stair center as anchors. Do not downscale staircase to solve perspective.
3. GEOMETRY: Kitchen/bar is currently a detached-looking white rounded counter at the edge of frame. The actual complete assembly includes dark rounded enclosure, white recessed soffit, cabinets, counter, backsplash artwork, integrated downlights and warm wall wash. Parent detail pass may already be rebuilding; rerender fully framed afterward.
4. GEOMETRY: Ceiling blade field source has broad black open gaps, visible services and thin suspension. Current blade field reads as dense wood skin, with tiny uniform pendants receding in a line. Reference has visibly thick gray cylindrical pendants of several diameters over the whole hub.
5. MATERIAL / FURNITURE: Source carpet mottled charcoal, magenta quilted bucket chairs grouped at white four-star tables, light-oak stools. Current carpet uniform, furniture distant and sparse, stair/glazing washed out. Correct framing first, then modeled furniture profile and arrangement rather than decorative color alone.

## REF04_Writeup

1. CAMERA WRONG END: Reference lab glazing is LEFT, atrium/stair RIGHT. Render has atrium/stairLEFT and labsRIGHT. The initial camera seed supplied in camera_targets was wrong. Place camera near opposite longitudinal end and reverse view direction. Do not mirror the render or swap architecture to fake match.
2. GEOMETRY: Source alternates shared standing-height oak collaboration tables, normal workstations and lounge chairs. Current is an unbroken repeated series of narrow desks and identical monitors. Even after camera correction it will not resemble the reference. Add observed table families at actual interval, retaining corridor circulation.
3. GEOMETRY: Source central gray rectangular column is broad and aligns between desk groups, with visible black skirting. Current small narrow piers and repetitive fixture strips lack structural weight. Fit column width relative to measured-looking table height in source, not arbitrary independent scaling.
4. GEOMETRY: Reference white ceiling rafts have black exposed service slots, visible supports and true hanging linear fixtures below; current is an almost continuous white slab that washes out lighting. Open observed slots and show enough structure to define depth, without inventing hidden MEP complexity.
5. MATERIAL / LIGHT: Reference readable lime lab partitions, white shelving, oak drawers, gray carpet, turquoise stools and transparent glazing. Render pale white lab and identical gray chairs. Use manufacturer-supported casework and limited visible lab layers, keeping closed access. Reduce white clipping so glass boundaries, worktops and task chairs remain legible.

## Next-pass requirement

Fix camera location/occlusions and obtain readable whole frames before spending a high-sample render on these four. Small quick clay/flat lighting previews suffice for camera checks. Record camera-transform changes with each iteration, since viewpoint changes invalidate direct geometry-only before/after comparisons.
