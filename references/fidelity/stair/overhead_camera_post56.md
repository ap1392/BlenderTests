# REF08 post56 camera-only diagnosis

Compared current large validation with exact university004-1 source. No Blender changes or render interruption.

Current shows nearest white band plus roughlythree inner bands; source nearest white band plustwo inner bands. This strongly supports photographing one level lower, L5 instead of L6. Relative helical phase can be preserved by subtracting exactlyH=4.4196 from both camera and aimpoint. No geometric alteration justified.

Keep18mm, current1.498aspect, existing sensor settings.

**CandidateA — isolated floor-height test**
- eye(.75,-.75,19.3034)
- target(-.8,1.5,5.5804)
- lens18mm

This is current camera minus one floor in both eye and target. Nearest-band projection should remain approximately equivalent because helix repeats each floor; one innermost turn disappears and the ground well becomes larger. This is the preferred first test.

**CandidateB — one floor lower plus oblique framing**
- eye(.75,-.75,19.3034)
- target(-.5,4.1,5.5804)
- lens18mm

Source bottom well center approximately43%image width,74%height; current approximately50%,61%. TargetB shifts the aim toward camera-right/up relative toA, moving deep well lower-left and increasing obliquity. This is an unrendered bounded candidate, not a solved calibration. Compare afterA; do not automatically replaceA.

Approximate source bottom-well width is noticeably larger than current. One floor lower resolves count and part of scale; residual size differences must be judged afterA. Two floors lower would probably remove too many visible turns, so is not recommended as first candidate.

Pass criteria: near-band framing comparable to source, two nested inner sweeps rather thanthree, bottom well aroundlower-left, limited surrounding gallery visible. Do not change physical stair radii to solve this camera discrepancy.

## Preview selection after camera59

Inspected A,B,C and C+1stop previews. **SelectC with the exposure-only+1stop preview** as the best bounded match. C's bottom well center about45%width/71%height is near source43%/74%; A remainednear50%/58%, Bnear47%/72% but showedtoo much surrounding gallery. C's nearer-band crop and three-turn count agree best.

C uses18mm with inferred crop-equivalent sensor width36*5904/7360≈28.88mm, shiftx.03, shifty-.04, Bpose. Crop inference is plausible from source pixel dimensions, not directly verified sensor/crop metadata. Preserve that distinction in camera notes.

Residual bottom-well diameter still about15–16%framewidth versus source19–20%. Accept as residual for now; no physical stair changes justified. +1stop exposure moves diffuse white/terrazzo closer to source while retaining detail, though inner band remains grayer than the very bright professional photograph. Keep exposure correction scoped to this camera comparison.
