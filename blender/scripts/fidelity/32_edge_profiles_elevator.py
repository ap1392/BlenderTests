exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Cross-view photo comparison supports a deeper opaque steel stringer profile.
for ob in bpy.data.objects:
 if 'smooth spiral white stringer' in ob.name and not ob.get('profile_depth_v32'):
  for i,v in enumerate(ob.data.vertices):
   if i%4 in [0,1]:v.co.z-=.20
  ob['profile_depth_v32']=True;finish(ob,True)
# Continuous white slab-edge fascia shields the blade ends. Preserve walking elevations.
for ob in bpy.data.objects:
 if 'continuous public gallery slab' in ob.name and not ob.get('fascia_depth_v32'):
  bottom=min(v.co.z for v in ob.data.vertices)
  for v in ob.data.vertices:
   if abs(v.co.z-bottom)<.001:v.co.z-=.20
  ob['fascia_depth_v32']=True;finish(ob)
steel=bpy.data.materials['Elevator brushed metal']
for ob in bpy.data.objects:
 if ob.name.startswith(('Elevator central leaf joint','Elevator indicator dark face','Elevator blue indicator')) and not ob.get('public_face_v32'):
  ob.location.y=-12.2-ob.location.y;ob['public_face_v32']=True
 if ob.name.startswith(('Elevator white jamb','Elevator white lintel')):
  ob.data.materials.clear();ob.data.materials.append(steel)
C='Rooms'
for x in [3,5]:
 box('Elevator public sill',(x,-5.99,.012),(1.74,.20,.024),steel)
 box('Elevator call station',(x+.98,-5.975,1.12),(.10,.035,.25),steel)
 for z in [1.07,1.17]:finish(beam('Elevator round call button',(x+.98,-5.948,z),(x+.98,-5.939,z),.018,dark),True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
