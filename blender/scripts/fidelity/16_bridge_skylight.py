exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
def cross_intervals(x,pts):
 vals=[]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  if (a[0]<=x<b[0])or(b[0]<=x<a[0]):vals.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
 vals.sort();return[(vals[i],vals[i+1])for i in range(0,len(vals)-1,2)]
C='Ceiling'
remove_where(lambda o:o.name.startswith(('End bridge parallel oak','End bridge acoustic field','Skylight rectilinear glazing bar')))
for lev,z in enumerate(FLOORS[1:],2):
 for path,width in [([(-20.1,7.1),(-17.9,-.7)],3.3),([(18.8,12.3),(19,5)],-4.0)]:
  outline=path+offset(path,width)[::-1]
  poly('End bridge acoustic field',outline,z+H-.20,.04,black,False)
  for i in range(228):
   x=-24+i*.21
   for a,b in cross_intervals(x,outline):
    if b-a>.03:box('End bridge parallel oak blade',(x,(a+b)/2,z+H-.46),(.038,b-a,.23),wood)
for ob in list(bpy.data.objects):
 if ob.name.startswith('Skylight upper glass'):
  verts=[v.co for v in ob.data.vertices];top=max(v.z for v in verts);path=[(v.x,v.y)for v in verts if abs(v.z-top)<.001]
  for i in range(int(min(p[0]for p in path)/.95)-1,int(max(p[0]for p in path)/.95)+2):
   x=i*.95
   for a,b in cross_intervals(x,path):box('Skylight rectilinear glazing bar',(x,(a+b)/2,top+.026),(.045,b-a,.065),white)
  swapped=[(y,x)for x,y in path]
  for i in range(int(min(p[0]for p in swapped)/1.5)-1,int(max(p[0]for p in swapped)/1.5)+2):
   y=i*1.5
   for a,b in cross_intervals(y,swapped):box('Skylight rectilinear glazing bar',((a+b)/2,y,top+.027),(b-a,.045,.065),white)
# Faceted rectangular tongue was a separate early blockout object. Union into its floor.
for lev in range(2,7):
 slab=bpy.data.objects.get(f'L{lev} continuous public gallery slab');tongue=bpy.data.objects.get(f'L{lev} stair landing connection')
 if slab and tongue:
  mod=slab.modifiers.new('Integrated stair landing connection','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=tongue
  bpy.context.view_layer.objects.active=slab;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(tongue,do_unlink=True)
  finish(slab)
  mod=slab.modifiers.new('Small plaster arris radius','BEVEL');mod.width=.025;mod.segments=3;mod.limit_method='ANGLE';mod.angle_limit=.6
# Higher reference level is supported by the 401–419 sign in Wausau4.
ob=bpy.data.objects['REF07_Stair_elevation'];ob.location.z+=H
ob=bpy.data.objects['REF11_End_bridge'];ob.location=(13,0,2*H+1.6);ob.rotation_euler=(Vector((23.3,8,2*H+2.0))-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=23
# Reduce concrete board-to-board contrast; retain physical grain and shallow form joints.
nt=concrete.node_tree;brick=next(n for n in nt.nodes if n.type=='TEX_BRICK');brick.inputs['Color1'].default_value=(.21,.22,.21,1);brick.inputs['Color2'].default_value=(.255,.26,.245,1);brick.inputs['Mortar'].default_value=(.19,.20,.19,1)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('End ceiling fields, skylight glazing bars and integrated stair tongues saved')
