import bpy,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
floors=[o for o in bpy.data.objects if o.name=='L1 unified terrazzo floor' or 'continuous public gallery slab' in o.name]
vs=[];fs=[]
for o in floors:
 off=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend(tuple(i+off for i in f.vertices)for f in o.data.polygons)
tree=BVHTree.FromPolygons(vs,fs);bad=[];checked=0
for o in bpy.data.objects:
 if o.type!='MESH':continue
 if 'Magenta social bucket shell' in o.name:
  p=o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8);z=round((p.z-.65)/4.4196)*4.4196;offsets=[(0,0),(.32,0),(-.32,0),(0,.32),(0,-.32)]
 elif o.name.startswith(('L1 documented classroom row table','L1 documented classroom teal seat','Tall stool white seat')):
  p=o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8);z=0;offsets=[(0,0)]
 else:continue
 checked+=1
 for dx,dy in offsets:
  if tree.ray_cast(Vector((p.x+dx,p.y+dy,z+.1)),Vector((0,0,-1)),.6)[0]is None:bad.append(o.name);break
nonfinite=[];seen=set()
for o in bpy.data.objects:
 if o.type!='MESH'or o.data in seen:continue
 seen.add(o.data)
 if any(not all(math.isfinite(c)for c in v.co)for v in o.data.vertices):nonfinite.append(o.name)
columns=[(-6.1,14.6),(3.1,15.9),(12.3,16.3)];stool_clear=[]
for o in bpy.data.objects:
 if o.name.startswith('Tall stool white seat'):
  p=o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)
  stool_clear.append(min(math.hypot(p.x-x,p.y-y)for x,y in columns)-.375-.18)
report={'revision':'post60','objects':len(bpy.data.objects),'reference_cameras':len([o for o in bpy.data.objects if o.type=='CAMERA'and o.name.startswith('REF')]),'unique_meshes_scanned':len(seen),'nonfinite_meshes':nonfinite,'furniture_support_items_checked':checked,'unsupported_sampled_items':bad,'minimum_stool_to_column_clearance_m':min(stool_clear),'scope':'Sampled support and finite-coordinate checks, not exhaustive collision or code compliance.'}
(root/'references/fidelity/calibration/integrity_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
assert not bad and not nonfinite and min(stool_clear)>0
