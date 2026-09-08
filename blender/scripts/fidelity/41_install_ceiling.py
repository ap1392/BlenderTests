exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:('parallel gallery oak blade'in o.name or o.name.startswith(('End bridge parallel oak blade','Social alcove parallel oak blade','Social pod rear straight oak blade','End bridge acoustic field','Social pod overhead acoustic plane','Unified gallery recessed oak blade','Unified gallery dark backing'))))
d=json.loads((ROOT/'references/fidelity/calibration/ceiling_intervals.json').read_text());C='Ceiling'
for z in FLOORS[1:]+[ROOF]:
 for x,a,b in d['intervals']:box('Unified gallery recessed oak blade',(x,(a+b)/2,z-.54),(.038,b-a,.20),wood)
 for rings in d['parts']:
  # The clipped public-floor polygon has no interior rings in the current plan.
  if len(rings)>1:raise RuntimeError('Unexpected ceiling interior requires explicit triangulation')
  poly('Unified gallery dark backing',rings[0],z-.421,.012,black,False)
bpy.context.scene['gallery_ceiling_construction']='Slat fields clipped to actual unified floor outline with80mm edge recess; dark backing below structural slab,20cm blades, stair tongue excluded. Gallery ceiling also restored below L2.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
