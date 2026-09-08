exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
remove_where(lambda o:o.name in ['L1 atrium terrazzo','L1 public undercroft beneath labs','Extended ground public undercroft','Classroom observed floor','L1 unified terrazzo floor'])
C='Atrium';p=json.loads((ROOT/'references/fidelity/calibration/ground_floor_union.json').read_text());xy=p['vertices'];N=len(xy);vs=[(x,y,-.28)for x,y in xy]+[(x,y,0)for x,y in xy];fs=[tuple(reversed(f))for f in p['triangles']]+[tuple(i+N for i in f)for f in p['triangles']]
for ring in p['rings']:
 for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
ob=mesh('L1 unified terrazzo floor',vs,fs,floor);finish(ob)
# The old gallery glass started80mm above floor, revealing lowerfloor througha large slot.
# Reference glass base is close to slab; retain16mm clearance and original guardtop.
for ob in bpy.data.objects:
 if ob.type=='MESH'and 'office gallery'in ob.name and 'glass'in ob.name:
  low=min(v.co.z for v in ob.data.vertices)
  for v in ob.data.vertices:
   if abs(v.co.z-low)<.002:v.co.z=round(low/H)*H+.016
  finish(ob)
# Keep curved glass sides smooth but cap faces flat; avoid averaged normals at thin glass edges.
for ob in bpy.data.objects:
 if ob.type!='MESH'or not ob.name.startswith(('Radial stair glass panel','Lower stair clear glass panel')):continue
 for i,f in enumerate(ob.data.polygons):f.use_smooth=i>=2 and (i-2)%4 in [1,3]
# REF07 source background is office/core wall rather than distant atrium end glazing.
ob=bpy.data.objects['REF07_Stair_elevation'];ob.location=(9,10,3*H+1.65);ob.rotation_euler=(Vector((0,0,3*H+.65))-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=33
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Ground void seam closed, guard base corrected, stair glass normals separated')
