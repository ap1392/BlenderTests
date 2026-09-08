exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/backups/ISEC_before_planar_floor_repair.blend'),copy=True)
remove_where(lambda o:('continuous public gallery slab'in o.name or ('carpet'in o.name.lower()and'write-up'not in o.name.lower()and o.type=='MESH')))
data=json.loads((ROOT/'references/fidelity/calibration/public_floor_union.json').read_text());C='Architecture'
for lev,z in enumerate(FLOORS[1:],2):
 for part in data['parts']:
  xy=part['vertices'];N=len(xy);vs=[(x,y,z-.42)for x,y in xy]+[(x,y,z)for x,y in xy]
  fs=[tuple(reversed(f))for f in part['triangles']]+[tuple(i+N for i in f)for f in part['triangles']]
  for ring in part['rings']:
   for a,b in zip(ring,ring[1:]+ring[:1]):fs.append((a,b,b+N,a+N))
  ob=mesh(f'L{lev} continuous public gallery slab',vs,fs,white);finish(ob);mod=ob.modifiers.new('Plaster edge radius','BEVEL');mod.width=.012;mod.segments=2;mod.limit_method='ANGLE';mod.angle_limit=.55
  ob=mesh(f'L{lev} continuous public carpet',[(x,y,z+.004)for x,y in xy],part['triangles'],carpet);finish(ob)
# Fitted low-level reverse-soffit seed selected after comparative tests.
cam=bpy.data.objects['REF02_Reverse_soffit'];test=bpy.data.objects['TEST02_2'];cam.location=test.location;cam.rotation_euler=test.rotation_euler;cam.data.lens=22
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Installed triangulated connected planar public floors',len(data['parts']))
