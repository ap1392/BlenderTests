exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name.startswith('Public gallery roof perimeter closure'))
# Roof cover must extend over the public gallery, not stop at the atrium void edge.
# This closes the exposed sky seam between the original void roof and end ceiling fields.
C='Architecture';data=json.loads((ROOT/'references/fidelity/calibration/public_floor_union.json').read_text())
for part in data['parts']:
 xy=part['vertices'];N=len(xy);vs=[(x,y,ROOF-.421)for x,y in xy]+[(x,y,ROOF+.05)for x,y in xy];fs=[tuple(reversed(f))for f in part['triangles']]+[tuple(i+N for i in f)for f in part['triangles']]
 for ring in part['rings']:
  for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
 finish(mesh('Public gallery roof perimeter closure',vs,fs,black))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
