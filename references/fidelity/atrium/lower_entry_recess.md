# Lower auditorium entry recess: resolved location

Evidence inspected: Wausau2 frontal stair photo; university Reflections011 ground wide photo; published Payette L1 plan; higher-resolution L1 original (2550×1650) normalized to the shared1600×1035 coordinates. Crops saved as `auditorium_L1_detail.jpg` and `auditorium_L1_grid.jpg`.

## Strong conclusion

The outer auditorium curve is **not floor-bearing throughout its eastern arc**. In L1, the heavy outside wall ends around `(748,500)` and resumes around `(762,569)`. A recessed inner wall and entrance/service-door arrangement lies west of this gap. This matches Wausau2's concrete above a warm wood-lined recess, seen at right under the upper stair. Reflections011 sees the more northerly floor-bearing concrete face; the two photos are consistent with a recess on only the middle/eastern arc.

## Exact change to the current curve

In script06, split `Auditorium board formed concrete east curve` at plan y=500 and y=569. These cut points on the **existing** Catmull-Rom centerline are approximately:

- `(753.388,500)` → world `(-5.261,-2.000)`.
- `(760.170,569)` → world `(-4.583,-8.900)`.

The interval between these points, containing current controls `(759,518)` and `(762,554)`, is the portion to lift above the recess. Use base around2.55m as a photo-based initial estimate, keeping the existing top at H+0.90. Keep the adjacent northern and southern curve portions floor-bearing. The decimal coordinates merely locate the split on the current approximation; they are not exact as-built dimensions. Current endpoint x differs by several pixels from the plan, so eventual local contour refinement is still warranted.

The existing separate raised return `(745,604)→(728,618)→(707,625)` is in the wrong place for this recess. L1 draws that southern outside curve heavy and continuous. Restore it to floor-bearing unless another inspected source supports an opening there.

## Recess backing without invented interior

The plan's inner boundary runs approximately `(711,489)→(729,522)→(738,550)→(738,578)→(734,590)`. A shallow closed warm-wood backing along the relevant inner portion can reproduce the visible recess. Do not model an open accessible room beyond it. Door positions should be taken from the plan, with a simple closed representation when the exact leaf appearance is not visible.

Confidence: high for location of the ground-level opening and the fact that the northern face remains solid; moderate for inferred2.55m underside height and the visible wood material extending along the full recess. Exact hidden backing details remain uncertain.
