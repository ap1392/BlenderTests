exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
d=json.loads((ROOT/'references/fidelity/calibration/ground_floor_classroom_union.json').read_text());remove_where(lambda o:o.name=='L1 unified terrazzo floor')
C='Architecture';xy=d['vertices'];N=len(xy);vs=[(x,y,-.28)for x,y in xy]+[(x,y,0)for x,y in xy];fs=[tuple(reversed(f))for f in d['triangles']]+[tuple(i+N for i in f)for f in d['triangles']]
for ring in d['rings']:
 for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
finish(mesh('L1 unified terrazzo floor',vs,fs,floor))
bpy.context.scene['ground_floor_v54']='Extended the continuous ground floor beneath the plan-aligned classroom envelope; floor-support checks caught the legacy floor stopping short beneath part of the fourth room.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Ground classroom floor support corrected; added',d['added_area'],'square metres')
